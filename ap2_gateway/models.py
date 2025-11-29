from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    NEFT = "neft"
    RTGS = "rtgs"

class MedicineItem(BaseModel):
    medicine_id: str
    name: str
    quantity: int
    unit_price: float

class AgentIdentity(BaseModel):
    agent_id: str
    agent_type: str
    signature: str

class PaymentDetails(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(default="INR")
    payment_method: PaymentMethod
    supplier_id: str
    purchase_order_id: str

class Metadata(BaseModel):
    medicine_items: List[MedicineItem]
    urgency: str
    forecast_id: Optional[str] = None
    zone: str

class CallbackConfig(BaseModel):
    url: str
    method: str = "POST"
    timeout_seconds: int = 30

class RiskAssessment(BaseModel):
    cost_threshold_exceeded: bool
    approval_required: bool
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

class PaymentRequest(BaseModel):
    protocol_version: str = "AP2-v1.0"
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    idempotency_key: str
    
    agent_identity: AgentIdentity
    payment_details: PaymentDetails
    metadata: Metadata
    callback: CallbackConfig
    risk_assessment: RiskAssessment
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('protocol_version')
    def check_protocol_version(cls, v):
        if v != "AP2-v1.0":
            raise ValueError("Unsupported protocol version")
        return v

class ProcessingInfo(BaseModel):
    estimated_completion: datetime
    queue_position: int
    retry_count: int = 0

class PollingInfo(BaseModel):
    status_url: str
    poll_interval_seconds: int = 5

class PaymentResponse(BaseModel):
    protocol_version: str = "AP2-v1.0"
    request_id: str
    transaction_id: str
    status: PaymentStatus
    
    payment_details: PaymentDetails
    processing_info: ProcessingInfo
    polling: PollingInfo
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PaymentProof(BaseModel):
    transaction_reference: str
    completed_at: datetime
    receipt_url: str

class Reconciliation(BaseModel):
    amount_debited: float
    fees: float
    net_amount: float
    currency: str = "INR"

class PaymentCallback(BaseModel):
    protocol_version: str = "AP2-v1.0"
    event_type: str
    transaction_id: str
    request_id: str
    
    final_status: PaymentStatus
    payment_proof: Optional[PaymentProof] = None
    reconciliation: Optional[Reconciliation] = None
    
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
