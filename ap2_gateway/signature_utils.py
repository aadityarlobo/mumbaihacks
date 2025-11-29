import hmac
import hashlib
from ap2_gateway.config import config

def generate_payment_signature(agent_id: str, idempotency_key: str, amount: float) -> str:
    """
    Generate HMAC signature for payment request
    
    This function should be used by agents (SupplierAgent, PharmacyAgent)
    to create valid signatures before sending payment requests.
    
    Args:
        agent_id: Unique identifier for the agent
        idempotency_key: Unique key for this payment request
        amount: Payment amount
    
    Returns:
        HMAC-SHA256 signature as hex string
    
    Example:
        >>> signature = generate_payment_signature(
        ...     "SupplierAgent-Delhi-South",
        ...     "agent-123-po-456-20251128",
        ...     1650.00
        ... )
        >>> print(signature)
        'a1b2c3d4e5f6...'
    """
    
    payload = f"{agent_id}:{idempotency_key}:{amount}"
    
    signature = hmac.new(
        config.HMAC_SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return signature

def verify_payment_signature(
    agent_id: str, 
    idempotency_key: str, 
    amount: float, 
    provided_signature: str
) -> bool:
    """
    Verify payment signature
    
    Args:
        agent_id: Agent identifier
        idempotency_key: Request idempotency key
        amount: Payment amount
        provided_signature: Signature to verify
    
    Returns:
        True if signature is valid, False otherwise
    """
    
    expected_signature = generate_payment_signature(agent_id, idempotency_key, amount)
    
    return hmac.compare_digest(expected_signature, provided_signature)
