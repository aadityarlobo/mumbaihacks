# import psycopg2
# from psycopg2.extras import RealDictCursor, Json
from contextlib import contextmanager
from typing import Dict, Any, Optional
# from ap2_gateway.config import config
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

# In-memory store to simulate database for this session
_transactions = {}
_idempotency_keys = {}

class DatabaseClient:
    def __init__(self):
        logger.warning("DatabaseClient is running in in-memory simulation mode. No data will be persisted.")
        self.conn_params = {}
    
    @contextmanager
    def get_connection(self):
        # This is a no-op context manager
        logger.info("DB Task: Skipped (in-memory mode)")
        yield None
    
    def create_transaction(self, payment_request: Dict[str, Any]) -> str:
        """Simulate creating a new payment transaction record in-memory"""
        logger.info("DB Task: Simulating transaction creation (in-memory)")
        
        transaction_id = str(uuid.uuid4())
        idempotency_key = payment_request['idempotency_key']

        if idempotency_key in _idempotency_keys:
             logger.warning(f"Idempotency key {idempotency_key} already exists.")
             # Returning existing transaction id
             return _idempotency_keys[idempotency_key]
        
        record = {
            'transaction_id': transaction_id,
            'agent_id': payment_request['agent_identity']['agent_id'],
            'agent_type': payment_request['agent_identity']['agent_type'],
            'purchase_order_id': payment_request['payment_details']['purchase_order_id'],
            'supplier_id': payment_request['payment_details']['supplier_id'],
            'amount': payment_request['payment_details']['amount'],
            'currency': payment_request['payment_details']['currency'],
            'idempotency_key': idempotency_key,
            'payment_method': payment_request['payment_details']['payment_method'],
            'status': 'pending',
            'metadata': payment_request['metadata'],
            'callback_url': payment_request['callback']['url'],
            'requested_at': datetime.utcnow(),
            'processed_at': None,
            'completed_at': None,
            'error_code': None,
            'error_message': None,
            'retry_count': 0,
            'callback_status': 'pending',
            'callback_attempts': 0,
            'updated_at': datetime.utcnow()
        }
        
        _transactions[transaction_id] = record
        _idempotency_keys[idempotency_key] = transaction_id

        logger.info(f"Created simulated transaction: {transaction_id}")
        return transaction_id
    
    def update_transaction_status(
        self, 
        transaction_id: str, 
        status: str,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        """Simulate updating transaction status in-memory"""
        logger.info(f"DB Task: Simulating update status for {transaction_id} to {status} (in-memory)")
        if transaction_id in _transactions:
            record = _transactions[transaction_id]
            record['status'] = status
            record['updated_at'] = datetime.utcnow()
            
            if status == 'processing':
                record['processed_at'] = datetime.utcnow()
            elif status == 'completed':
                record['completed_at'] = datetime.utcnow()
            elif status == 'failed':
                record['error_code'] = error_code
                record['error_message'] = error_message
                record['retry_count'] += 1
            
            logger.info(f"Updated simulated transaction {transaction_id} to {status}")
        else:
            logger.error(f"Transaction {transaction_id} not found in in-memory store.")

    def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Simulate getting transaction details from in-memory store"""
        logger.info(f"DB Task: Getting simulated transaction {transaction_id} (in-memory)")
        return _transactions.get(transaction_id)
    
    def check_idempotency(self, idempotency_key: str) -> Optional[str]:
        """Simulate checking if idempotency key already exists in-memory"""
        logger.info(f"DB Task: Checking idempotency for {idempotency_key} (in-memory)")
        return _idempotency_keys.get(idempotency_key)
    
    def update_callback_status(self, transaction_id: str, status: str):
        """Simulate updating webhook callback status in-memory"""
        logger.info(f"DB Task: Simulating update callback status for {transaction_id} to {status} (in-memory)")
        if transaction_id in _transactions:
            _transactions[transaction_id]['callback_status'] = status
            _transactions[transaction_id]['callback_attempts'] += 1
        else:
            logger.error(f"Transaction {transaction_id} not found in in-memory store.")

db_client = DatabaseClient()