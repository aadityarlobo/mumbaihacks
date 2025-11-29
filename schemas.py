from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime

# --- 1. FORECASTING (Doctor) ---
class SurgeForecast(BaseModel):
    zone: str
    predicted_patients: int
    severity_breakdown: Dict[str, int] = Field(description="mild, moderate, severe counts")
    confidence: float
    reasoning: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

# --- 2. INVENTORY (Pharmacy) ---
class MedicineItem(BaseModel):
    medicine_id: str
    name: str
    quantity_needed: int
    urgency: Literal["normal", "critical"]

class PharmacyPlan(BaseModel):
    items_to_reorder: List[MedicineItem]
    estimated_internal_cost: float
    status: Literal["adequate", "shortage"]

# --- 3. SUPPLY CHAIN (Supplier) ---
class SupplierOffer(BaseModel):
    medicine_id: str
    supplier_name: str
    quantity_available: int
    cost: float
    delivery_eta_hours: int
    expedite_available: bool
    expedite_cost: float

class SupplierResponse(BaseModel):
    offers: List[SupplierOffer]
    total_procurement_cost: float
    logistics_risk: Literal["low", "medium", "high"]

# --- 4. STAFFING (Operations) ---
class ShiftDetail(BaseModel):
    role: Literal["doctor", "nurse"]
    count_needed: int
    shift_period: str

class StaffingPlan(BaseModel):
    shifts: List[ShiftDetail]
    total_labor_cost: float
    gap_analysis: str

# --- 5. PUBLIC HEALTH (PublicHealth) ---
class PublicAdvisory(BaseModel):
    alert_level: Literal["info", "warning", "critical"]
    title: str
    message_body: str
    target_channels: List[str]
    draft_status: Literal["draft", "ready"]

# --- 6. ORCHESTRATION & AUDIT ---
class AuditLog(BaseModel):
    action_type: str
    agent_name: str
    reasoning: str
    cost_impact: float
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class FinalDecision(BaseModel):
    approved: bool
    execution_plan: str
    risk_level: Literal["low", "medium", "high"]
    human_approval_required: bool
    audit_trail: List[AuditLog]

# --- 7. PAYMENTS (Agent-to-Payment) ---
class PaymentTransaction(BaseModel):
    transaction_id: str
    recipient: str
    amount: float
    status: Literal["pending", "completed", "failed"]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class PaymentStatus(BaseModel):
    transactions: List[PaymentTransaction]
    total_paid: float
    status: Literal["processing", "completed", "failed"]

# --- 8. COMMUNICATIONS (Infographic & Telegram) ---
class InfographicContent(BaseModel):
    title: str
    key_stats: List[str]
    visual_description: str
    image_path: Optional[str] = None

class TelegramStatus(BaseModel):
    sent: bool
    message_id: Optional[str]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())