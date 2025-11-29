import redis
import json
from typing import Dict, Any, Optional
from ap2_gateway.config import config
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True
        )
        self._ensure_streams()
        self._ensure_consumer_groups()
    
    def _ensure_streams(self):
        """Create streams if they don't exist"""
        streams = [
            "payment:requests",
            "payment:processing",
            "payment:completed",
            "payment:failed",
            "payment:callbacks"
        ]
        
        for stream in streams:
            try:
                # Try to create stream by adding a dummy message
                if not self.client.exists(stream):
                    self.client.xadd(stream, {"_init": "true"}, maxlen=1)
                    logger.info(f"Stream created: {stream}")
            except redis.ResponseError:
                pass  # Stream already exists
    
    def _ensure_consumer_groups(self):
        """Create consumer groups for each stream"""
        groups = {
            "payment:requests": ["payment-processor"],
            "payment:completed": ["payment-notifier", "audit-logger"],
            "payment:failed": ["retry-handler"]
        }
        
        for stream, group_list in groups.items():
            for group in group_list:
                try:
                    self.client.xgroup_create(
                        stream, 
                        group, 
                        id='0', 
                        mkstream=True
                    )
                    logger.info(f"Consumer group created: {group} on {stream}")
                except redis.ResponseError as e:
                    if "BUSYGROUP" not in str(e):
                        logger.error(f"Error creating group {group}: {e}")
    
    def publish_payment_request(self, request: Dict[str, Any]) -> str:
        """Publish payment request to stream"""
        message_id = self.client.xadd(
            "payment:requests",
            {"payload": json.dumps(request, default=str)},
            maxlen=10000  # Keep last 10k messages
        )
        logger.info(f"Published payment request: {message_id}")
        return message_id
    
    def publish_processing_update(self, transaction_id: str, data: Dict[str, Any]) -> str:
        """Publish processing status update"""
        message_id = self.client.xadd(
            "payment:processing",
            {
                "transaction_id": transaction_id,
                "payload": json.dumps(data, default=str)
            }
        )
        return message_id
    
    def publish_completion(self, transaction_id: str, callback_data: Dict[str, Any]) -> str:
        """Publish payment completion"""
        message_id = self.client.xadd(
            "payment:completed",
            {
                "transaction_id": transaction_id,
                "payload": json.dumps(callback_data, default=str)
            }
        )
        logger.info(f"Published completion for {transaction_id}")
        return message_id
    
    def publish_failure(self, transaction_id: str, error_data: Dict[str, Any]) -> str:
        """Publish payment failure for retry logic"""
        message_id = self.client.xadd(
            "payment:failed",
            {
                "transaction_id": transaction_id,
                "payload": json.dumps(error_data, default=str)
            }
        )
        logger.error(f"Published failure for {transaction_id}")
        return message_id
    
    def consume_payment_requests(self, consumer_name: str, block: int = 5000):
        """Consume payment requests (for worker)"""
        try:
            messages = self.client.xreadgroup(
                groupname="payment-processor",
                consumername=consumer_name,
                streams={"payment:requests": ">"},
                count=1,
                block=block
            )
            
            if messages:
                for stream, message_list in messages:
                    for message_id, data in message_list:
                        yield message_id, json.loads(data['payload'])
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
    
    def ack_message(self, stream: str, group: str, message_id: str):
        """Acknowledge message processing"""
        self.client.xack(stream, group, message_id)
    
    def get_idempotency_check(self, idempotency_key: str) -> Optional[str]:
        """Check if idempotency key exists"""
        return self.client.get(f"idempotency:{idempotency_key}")
    
    def set_idempotency_check(self, idempotency_key: str, transaction_id: str, ttl_hours: int = 24):
        """Store idempotency key"""
        self.client.setex(
            f"idempotency:{idempotency_key}",
            ttl_hours * 3600,
            transaction_id
        )

redis_client = RedisClient()
