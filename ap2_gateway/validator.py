import hmac
import hashlib
from typing import Dict, Any, Tuple
from ap2_gateway.models import PaymentRequest
from ap2_gateway.config import config
import logging

logger = logging.getLogger(__name__)

class RequestValidator:
    """Validates incoming payment requests for AP2 protocol compliance"""
    
    def __init__(self):
        self.secret_key = config.HMAC_SECRET_KEY.encode()
    
    def validate_signature(self, request: PaymentRequest) -> Tuple[bool, str]:
        """
        Validate HMAC signature from agent
        
        In production, this would verify the agent's identity.
        For hackathon, we'll do a simple HMAC check.
        """
        try:
            # Create signature payload
            payload = f"{request.agent_identity.agent_id}:{request.idempotency_key}:{request.payment_details.amount}"
            
            # Calculate expected signature
            expected_signature = hmac.new(
                self.secret_key,
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare with provided signature
            provided_signature = request.agent_identity.signature
            
            if hmac.compare_digest(expected_signature, provided_signature):
                logger.info(f"Signature valid for agent: {request.agent_identity.agent_id}")
                return True, "Signature valid"
            else:
                logger.warning(f"Signature mismatch for agent: {request.agent_identity.agent_id}")
                return False, "Invalid signature"
        
        except Exception as e:
            logger.error(f"Signature validation error: {e}")
            return False, f"Signature validation error: {str(e)}"
    
    def validate_amount(self, request: PaymentRequest) -> Tuple[bool, str]:
        """Validate payment amount against limits"""
        
        amount = request.payment_details.amount
        
        # Check minimum amount
        if amount <= 0:
            return False, "Amount must be positive"
        
        # Check maximum transaction limit
        # In production, fetch this from payment_gateway_config table
        max_amount = 100000.00  # ₹1 lakh
        
        if amount > max_amount:
            return False, f"Amount exceeds maximum limit of {max_amount}"
        
        logger.info(f"Amount validation passed: {amount}")
        return True, "Amount valid"
    
    def validate_approval(self, request: PaymentRequest) -> Tuple[bool, str]:
        """Validate that high-value transactions have approval"""
        
        # Check if approval is required
        if not request.risk_assessment.approval_required:
            return True, "Approval not required"
        
        # Verify approval details exist
        if not request.risk_assessment.approved_by:
            return False, "Missing approval for high-risk transaction"
        
        if not request.risk_assessment.approved_at:
            return False, "Missing approval timestamp"
        
        logger.info(f"Approval valid: {request.risk_assessment.approved_by}")
        return True, "Approval verified"
    
    def validate_supplier(self, supplier_id: str) -> Tuple[bool, str]:
        """Validate supplier exists and is active"""
        from ap2_gateway.db_client import db_client
        
        try:
            with db_client.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT active FROM suppliers
                        WHERE supplier_id = %s
                    """, (supplier_id,))
                    
                    result = cur.fetchone()
                    
                    if not result:
                        return False, "Supplier not found"
                    
                    if not result[0]:
                        return False, "Supplier is inactive"
                    
                    logger.info(f"Supplier validation passed: {supplier_id}")
                    return True, "Supplier valid"
        
        except Exception as e:
            logger.error(f"Supplier validation error: {e}")
            return False, f"Supplier validation error: {str(e)}"
    
    def validate_purchase_order(self, po_id: str) -> Tuple[bool, str]:
        """Validate purchase order exists"""
        from ap2_gateway.db_client import db_client
        
        try:
            with db_client.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT payment_status FROM purchase_orders
                        WHERE po_id = %s
                    """, (po_id,))
                    
                    result = cur.fetchone()
                    
                    if not result:
                        return False, "Purchase order not found"
                    
                    payment_status = result[0]
                    
                    if payment_status == 'paid':
                        return False, "Purchase order already paid"
                    
                    logger.info(f"Purchase order validation passed: {po_id}")
                    return True, "Purchase order valid"
        
        except Exception as e:
            logger.error(f"Purchase order validation error: {e}")
            return False, f"PO validation error: {str(e)}"
    
    def validate_request(self, request: PaymentRequest) -> Tuple[bool, str]:
        """
        Complete request validation
        Returns: (is_valid, error_message)
        """
        
        # 1. Validate signature
        valid, msg = self.validate_signature(request)
        if not valid:
            return False, f"Signature validation failed: {msg}"
        
        # 2. Validate amount
        valid, msg = self.validate_amount(request)
        if not valid:
            return False, f"Amount validation failed:. {msg}"
        
        # 3. Validate approval if required
        valid, msg = self.validate_approval(request)
        if not valid:
            return False, f"Approval validation failed: {msg}"
        
        # 4. Validate supplier
        # valid, msg = self.validate_supplier(request.payment_details.supplier_id)
        # if not valid:
        #     return False, f"Supplier validation failed: {msg}"
        
        # 5. Validate purchase order
        # valid, msg = self.validate_purchase_order(request.payment_details.purchase_order_id)
        # if not valid:
        #     return False, f"Purchase order validation failed: {msg}"
        
        logger.info(f"Request validation passed for: {request.request_id}")
        return True, "All validations passed"

validator = RequestValidator()
