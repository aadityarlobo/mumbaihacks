from enum import Enum

class PaymentErrorCode(str, Enum):
    """Standardized error codes for AP2 protocol"""
    
    # Validation Errors (4xx equivalent)
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    INVALID_AMOUNT = "INVALID_AMOUNT"
    AMOUNT_EXCEEDS_LIMIT = "AMOUNT_EXCEEDS_LIMIT"
    MISSING_APPROVAL = "MISSING_APPROVAL"
    SUPPLIER_NOT_FOUND = "SUPPLIER_NOT_FOUND"
    SUPPLIER_INACTIVE = "SUPPLIER_INACTIVE"
    PO_NOT_FOUND = "PO_NOT_FOUND"
    PO_ALREADY_PAID = "PO_ALREADY_PAID"
    INVALID_REQUEST = "INVALID_REQUEST"
    DUPLICATE_IDEMPOTENCY_KEY = "DUPLICATE_IDEMPOTENCY_KEY"
    
    # Processing Errors (5xx equivalent)
    PROCESSING_ERROR = "PROCESSING_ERROR"
    PROCESSING_FAILED = "PROCESSING_FAILED"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    BANK_ERROR = "BANK_ERROR"
    TIMEOUT = "TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"
    
    # System Errors
    DATABASE_ERROR = "DATABASE_ERROR"
    REDIS_ERROR = "REDIS_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    
    # Retry Errors
    MAX_RETRIES_EXCEEDED = "MAX_RETRIES_EXCEEDED"
    RETRY_NOT_ALLOWED = "RETRY_NOT_ALLOWED"

ERROR_MESSAGES = {
    PaymentErrorCode.INVALID_SIGNATURE: "Agent signature validation failed",
    PaymentErrorCode.INVALID_AMOUNT: "Payment amount is invalid",
    PaymentErrorCode.AMOUNT_EXCEEDS_LIMIT: "Payment amount exceeds maximum transaction limit",
    PaymentErrorCode.MISSING_APPROVAL: "High-risk transaction requires approval",
    PaymentErrorCode.SUPPLIER_NOT_FOUND: "Supplier not found in system",
    PaymentErrorCode.SUPPLIER_INACTIVE: "Supplier account is inactive",
    PaymentErrorCode.PO_NOT_FOUND: "Purchase order not found",
    PaymentErrorCode.PO_ALREADY_PAID: "Purchase order has already been paid",
    PaymentErrorCode.PROCESSING_FAILED: "Payment processing failed",
    PaymentErrorCode.INSUFFICIENT_FUNDS: "Insufficient funds in account",
    PaymentErrorCode.MAX_RETRIES_EXCEEDED: "Maximum retry attempts exceeded",
}

def get_error_message(code: PaymentErrorCode) -> str:
    """Get human-readable error message for error code"""
    return ERROR_MESSAGES.get(code, "Unknown error occurred")
