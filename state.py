from typing import TypedDict, List, Annotated, Optional
import operator
from schemas import (
    SurgeForecast, PharmacyPlan, StaffingPlan, 
    SupplierResponse, PublicAdvisory, FinalDecision,
    PaymentStatus, InfographicContent, TelegramStatus
)

class AgentState(TypedDict):
    # --- Inputs ---
    location_zone: str
    current_time: str
    rag_context: str 
    
    # --- Agent Outputs ---
    forecast: Optional[SurgeForecast]
    pharmacy_plan: Optional[PharmacyPlan]
    staffing_plan: Optional[StaffingPlan]
    supplier_response: Optional[SupplierResponse]
    public_advisory: Optional[PublicAdvisory]
    
    # --- Final Output ---
    final_decision: Optional[FinalDecision]
    
    # --- Post-Decision Outputs ---
    payment_status: Optional[PaymentStatus]
    infographic: Optional[InfographicContent]
    telegram_status: Optional[TelegramStatus]
    
    # --- Chat History / Debug Log ---
    messages: Annotated[List[str], operator.add]