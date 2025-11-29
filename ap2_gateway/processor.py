import asyncio
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ap2_gateway.models import (
    PaymentRequest, PaymentResponse, PaymentCallback,
    PaymentStatus, ProcessingInfo, PollingInfo,
    PaymentProof, Reconciliation
)
from ap2_gateway.db_client import db_client
from ap2_gateway.redis_client import redis_client
from ap2_gateway.validator import validator
from ap2_gateway.config import config
import logging

logger = logging.getLogger(__name__)

class PaymentProcessor:
    """
    Core payment processing engine for AP2 protocol
    
    Handles:
    - Idempotency checks
    - Transaction creation
    - Simulated payment processing
    - Status updates
    - Callback generation
    """
    
    def __init__(self):
        self.config = config
        self.processing_tasks = {}  # Track ongoing processing tasks
    
    async def initiate_payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiate payment processing
        
        Steps:
        1. Check idempotency
        2. Validate request
        3. Create transaction record
        4. Publish to Redis
        5. Start async processing
        6. Return immediate response
        """
        
        logger.info(f"Initiating payment: {request.request_id}")
        
        # Step 1: Idempotency check
        existing_txn = db_client.check_idempotency(request.idempotency_key)
        
        if existing_txn:
            logger.info(f"Idempotent request detected: {request.idempotency_key}")
            
            # Return existing transaction
            transaction = db_client.get_transaction(existing_txn)
            
            return PaymentResponse(
                request_id=request.request_id,
                transaction_id=existing_txn,
                status=PaymentStatus(transaction['status']),
                payment_details=request.payment_details,
                processing_info=ProcessingInfo(
                    estimated_completion=transaction['requested_at'] + timedelta(seconds=5),
                    queue_position=0,
                    retry_count=transaction['retry_count']
                ),
                polling=PollingInfo(
                    status_url=f"http://payment-gateway:{config.GATEWAY_PORT}/api/status/{existing_txn}",
                    poll_interval_seconds=5
                )
            )
        
        # Step 2: Validate request
        is_valid, error_msg = validator.validate_request(request)
        
        if not is_valid:
            logger.error(f"Validation failed: {error_msg}")
            raise ValueError(error_msg)
        
        # Step 3: Create transaction record
        transaction_id = db_client.create_transaction(request.dict(exclude_none=True))
        
        logger.info(f"Created transaction: {transaction_id}")
        
        # Step 4: Publish to Redis for async processing
        redis_client.publish_payment_request({
            'transaction_id': transaction_id,
            'request': request.dict(exclude_none=True)
        })
        
        # Step 5: Start async processing (fire and forget)
        asyncio.create_task(self._process_payment(transaction_id, request))
        
        # Step 6: Return immediate response
        estimated_completion = datetime.utcnow() + timedelta(
            seconds=random.randint(
                config.PROCESSING_TIME_MIN_SECONDS,
                config.PROCESSING_TIME_MAX_SECONDS
            )
        )
        
        response = PaymentResponse(
            request_id=request.request_id,
            transaction_id=transaction_id,
            status=PaymentStatus.PROCESSING,
            payment_details=request.payment_details,
            processing_info=ProcessingInfo(
                estimated_completion=estimated_completion,
                queue_position=len(self.processing_tasks),
                retry_count=0
            ),
            polling=PollingInfo(
                status_url=f"http://payment-gateway:{config.GATEWAY_PORT}/api/status/{transaction_id}",
                poll_interval_seconds=5
            )
        )
        
        logger.info(f"Payment initiated: {transaction_id}")
        return response
    
    async def _process_payment(self, transaction_id: str, request: PaymentRequest):
        """
        Internal async payment processing
        
        Simulates real payment gateway behavior:
        - Processing delay
        - Success/failure randomization
        - Status updates
        - Callback dispatch
        """
        
        logger.info(f"Processing payment: {transaction_id}")
        
        try:
            # Update status to processing
            db_client.update_transaction_status(transaction_id, 'processing')
            
            redis_client.publish_processing_update(transaction_id, {
                'status': 'processing',
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Simulate processing time
            processing_time = random.uniform(
                config.PROCESSING_TIME_MIN_SECONDS,
                config.PROCESSING_TIME_MAX_SECONDS
            )
            
            logger.info(f"Processing time: {processing_time}s for {transaction_id}")
            await asyncio.sleep(processing_time)
            
            # Simulate success/failure based on configured success rate
            success = random.random() < config.SUCCESS_RATE
            
            if success:
                await self._complete_payment(transaction_id, request)
            else:
                await self._fail_payment(transaction_id, request)
        
        except Exception as e:
            logger.error(f"Error processing payment {transaction_id}: {e}")
            await self._fail_payment(
                transaction_id, 
                request,
                error_code="PROCESSING_ERROR",
                error_message=str(e)
            )
    
    async def _complete_payment(self, transaction_id: str, request: PaymentRequest):
        """Complete successful payment"""
        
        logger.info(f"Completing payment: {transaction_id}")
        
        # Update transaction status
        db_client.update_transaction_status(transaction_id, 'completed')
        
        # Calculate fees (1% of amount)
        amount = request.payment_details.amount
        fees = round(amount * 0.01, 2)
        net_amount = amount - fees
        
        # Generate payment proof
        payment_proof = PaymentProof(
            transaction_reference=f"BANK-REF-{uuid.uuid4().hex[:8].upper()}",
            completed_at=datetime.utcnow(),
            receipt_url=f"http://payment-gateway:{config.GATEWAY_PORT}/receipts/{transaction_id}.pdf"
        )
        
        # Generate reconciliation data
        reconciliation = Reconciliation(
            amount_debited=amount,
            fees=fees,
            net_amount=net_amount,
            currency=request.payment_details.currency
        )
        
        # Create callback payload
        callback = PaymentCallback(
            event_type="payment.completed",
            transaction_id=transaction_id,
            request_id=request.request_id,
            final_status=PaymentStatus.COMPLETED,
            payment_proof=payment_proof,
            reconciliation=reconciliation
        )
        
        # Publish completion to Redis
        redis_client.publish_completion(transaction_id, callback.dict(exclude_none=True))
        
        # Send webhook callback
        await self._send_callback(request.callback.url, callback)
        
        # Update purchase order status
        # self._update_purchase_order_status(
        #     request.payment_details.purchase_order_id,
        #     'paid',
        #     transaction_id
        # )
        
        logger.info(f"Payment completed: {transaction_id}")
    
    async def _fail_payment(
        self, 
        transaction_id: str, 
        request: PaymentRequest,
        error_code: str = "PROCESSING_FAILED",
        error_message: str = "Payment processing failed"
    ):
        """Handle failed payment"""
        
        logger.error(f"Payment failed: {transaction_id} - {error_message}")
        
        # Update transaction status
        db_client.update_transaction_status(
            transaction_id, 
            'failed',
            error_code=error_code,
            error_message=error_message
        )
        
        # Create callback payload
        callback = PaymentCallback(
            event_type="payment.failed",
            transaction_id=transaction_id,
            request_id=request.request_id,
            final_status=PaymentStatus.FAILED,
            error_code=error_code,
            error_message=error_message
        )
        
        # Publish failure to Redis (for retry logic)
        redis_client.publish_failure(transaction_id, {
            'callback': callback.dict(exclude_none=True),
            'request': request.dict(exclude_none=True)
        })
        
        # Send webhook callback
        await self._send_callback(request.callback.url, callback)
        
        logger.info(f"Payment failure processed: {transaction_id}")
    
    async def _send_callback(self, callback_url: str, callback: PaymentCallback):
        """Send webhook callback to agent"""
        
        logger.info(f"Sending callback to: {callback_url}")
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    callback_url,
                    json=callback.dict(exclude_none=True),
                    timeout=aiohttp.ClientTimeout(total=config.WEBHOOK_TIMEOUT_SECONDS)
                ) as response:
                    
                    if response.status == 200:
                        logger.info(f"Callback sent successfully: {callback.transaction_id}")
                        db_client.update_callback_status(callback.transaction_id, 'sent')
                    else:
                        logger.warning(f"Callback failed with status {response.status}")
                        db_client.update_callback_status(callback.transaction_id, 'failed')
        
        except asyncio.TimeoutError:
            logger.error(f"Callback timeout: {callback_url}")
            db_client.update_callback_status(callback.transaction_id, 'failed')
        
        except Exception as e:
            logger.error(f"Callback error: {e}")
            db_client.update_callback_status(callback.transaction_id, 'failed')
    
    def _update_purchase_order_status(
        self, 
        po_id: str, 
        payment_status: str,
        payment_reference: str
    ):
        """Update purchase order payment status"""
        
        try:
            with db_client.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE purchase_orders
                        SET payment_status = %s,
                            payment_reference = %s,
                            confirmed_at = NOW()
                        WHERE po_id = %s
                    """, (payment_status, payment_reference, po_id))
            
            logger.info(f"Updated PO {po_id} to {payment_status}")
        
        except Exception as e:
            logger.error(f"Error updating PO status: {e}")
    
    def get_transaction_status(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get current transaction status"""
        
        transaction = db_client.get_transaction(transaction_id)
        
        if not transaction:
            return None
        
        return {
            'transaction_id': str(transaction['transaction_id']),
            'status': transaction['status'],
            'amount': float(transaction['amount']),
            'currency': transaction['currency'],
            'requested_at': transaction['requested_at'].isoformat(),
            'processed_at': transaction['processed_at'].isoformat() if transaction['processed_at'] else None,
            'completed_at': transaction['completed_at'].isoformat() if transaction['completed_at'] else None,
            'error_code': transaction['error_code'],
            'error_message': transaction['error_message'],
            'retry_count': transaction['retry_count']
        }
    
    async def retry_failed_payment(self, transaction_id: str) -> bool:
        """Retry a failed payment"""
        
        transaction = db_client.get_transaction(transaction_id)
        
        if not transaction:
            logger.error(f"Transaction not found: {transaction_id}")
            return False
        
        if transaction['status'] != 'failed':
            logger.error(f"Transaction not in failed state: {transaction_id}")
            return False
        
        if transaction['retry_count'] >= transaction['max_retries']:
            logger.error(f"Max retries exceeded: {transaction_id}")
            return False
        
        logger.info(f"Retrying payment: {transaction_id}")
        
        # Reconstruct request from metadata
        request_dict = {
            'request_id': str(uuid.uuid4()),
            'idempotency_key': f"{transaction['idempotency_key']}-retry-{transaction['retry_count']}",
            'agent_identity': {
                'agent_id': transaction['agent_id'],
                'agent_type': transaction['agent_type'],
                'signature': 'retry-signature'  # Skip validation for retries
            },
            'payment_details': {
                'amount': float(transaction['amount']),
                'currency': transaction['currency'],
                'payment_method': transaction['payment_method'],
                'supplier_id': str(transaction['supplier_id']),
                'purchase_order_id': str(transaction['purchase_order_id'])
            },
            'metadata': transaction['metadata'],
            'callback': {
                'url': transaction['callback_url'],
                'method': 'POST',
                'timeout_seconds': 30
            },
            'risk_assessment': {
                'cost_threshold_exceeded': False,
                'approval_required': False
            }
        }
        
        request = PaymentRequest(**request_dict)
        
        # Start new processing attempt
        await self._process_payment(transaction_id, request)
        
        return True

processor = PaymentProcessor()
