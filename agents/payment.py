import uuid
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from config import llm_light
from schemas import PaymentStatus, PaymentTransaction
from state import AgentState
from ap2_gateway.models import PaymentRequest, AgentIdentity, PaymentDetails, Metadata, CallbackConfig, RiskAssessment, PaymentMethod
from ap2_gateway.signature_utils import generate_payment_signature
from ap2_gateway.processor import processor
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

payment_prompt = ChatPromptTemplate.from_template(
    """
    You are **PaymentAgent**. You execute payments for approved plans.
    
    INPUTS:
    - Supplier Cost: {supplier_cost}
    - Staffing Cost: {staffing_cost}
    - Decision: {decision}
    
    TASK:
    - If decision is APPROVED, generate transaction records.
    - Create a transaction for 'MedSupplier_Inc' and 'Hospital_Staff_Fund'.
    
    OUTPUT: Strict JSON (PaymentStatus).
    """
)

def payment_node(state: AgentState):
    print("--- PAYMENT AGENT (A2P) ---")
    
    decision = state.get("final_decision")
    if not decision or not decision.approved:
        return {"messages": ["Payment: Skipped (Not Approved)"]}

    transactions = []
    total_paid = 0.0

    # Group supplier offers by supplier name
    supplier_costs = {}
    if state["supplier_response"]:
        for offer in state["supplier_response"].offers:
            if offer.supplier_name not in supplier_costs:
                supplier_costs[offer.supplier_name] = 0.0
            supplier_costs[offer.supplier_name] += offer.cost

    # Create payment requests for each supplier
    for supplier_name, amount in supplier_costs.items():
        if amount > 0:
            logger.info(f"Processing payment for {supplier_name} for amount {amount}")
            # This is a mock PO ID. In a real system, this would come from the procurement process.
            po_id = uuid.uuid4()
            
            # This is a mock supplier ID. In a real system, this would be retrieved from a supplier database.
            supplier_id = uuid.uuid4()

            idempotency_key = f"agent-payment-{po_id}-{datetime.utcnow().timestamp()}"
            agent_id = "PaymentAgent_001"
            signature = generate_payment_signature(agent_id, idempotency_key, amount)

            payment_details = PaymentDetails(
                amount=amount,
                currency="INR",
                payment_method=PaymentMethod.BANK_TRANSFER,
                supplier_id=str(supplier_id),
                purchase_order_id=str(po_id)
            )

            # Create a simplified metadata object.
            # In a real scenario, we'd populate this from the offers.
            medicine_items = []
            if state["supplier_response"]:
                for offer in state["supplier_response"].offers:
                    if offer.supplier_name == supplier_name:
                        # Assuming the ap2_gateway.models.MedicineItem is compatible with schemas.MedicineItem
                        # If not, we would need to map the fields. For now, let's assume they are compatible
                        # and that we have a way to create the AP2MedicineItem from the offer.
                        # Since `ap2_gateway.models.MedicineItem` has `name`, `quantity` and `unit_price`, 
                        # and `schemas.SupplierOffer` has `cost` and `quantity_available`,
                        # we can create a simple mapping.
                        pass


            metadata = Metadata(
                medicine_items=[],
                urgency="critical", # This would come from the forecast or pharmacy plan.
                zone=state.get("forecast", {}).get("zone", "unknown"),
            )

            request = PaymentRequest(
                request_id=str(uuid.uuid4()),
                idempotency_key=idempotency_key,
                agent_identity=AgentIdentity(agent_id=agent_id, agent_type="BillingAgent", signature=signature),
                payment_details=payment_details,
                metadata=metadata,
                callback=CallbackConfig(url="http://localhost:8000/callback"), # Dummy callback URL
                risk_assessment=RiskAssessment(cost_threshold_exceeded=False, approval_required=False)
            )

            try:
                # Directly call the payment processor
                payment_response = asyncio.run(processor.initiate_payment(request))
                
                transactions.append(PaymentTransaction(
                    transaction_id=payment_response.transaction_id,
                    recipient=supplier_name,
                    amount=amount,
                    status="pending" # The gateway response is "processing", we'll consider it pending until callback.
                ))
                total_paid += amount
                logger.info(f"Payment initiated for {supplier_name}. Transaction ID: {payment_response.transaction_id}")

            except Exception as e:
                logger.error(f"Error processing payment for {supplier_name}: {e}")
                transactions.append(PaymentTransaction(
                    transaction_id=f"FAILED-{uuid.uuid4().hex[:8]}",
                    recipient=supplier_name,
                    amount=amount,
                    status="failed"
                ))


    staffing_cost = state["staffing_plan"].total_labor_cost if state["staffing_plan"] else 0.0
    if staffing_cost > 0:
        # Similar payment logic for staffing would go here.
        # For now, we'll keep the old mock logic for staffing.
        transactions.append(PaymentTransaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:8]}",
            recipient="Hospital_Staff_Fund",
            amount=staffing_cost,
            status="completed"
        ))
        total_paid += staffing_cost

    result = PaymentStatus(
        transactions=transactions,
        total_paid=total_paid,
        status="processing" if total_paid > 0 else "completed"
    )
    
    return {"payment_status": result, "messages": [f"Payment: Processed ₹{result.total_paid}"]}