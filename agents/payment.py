import uuid
from langchain_core.prompts import ChatPromptTemplate
from config import llm_light
from schemas import PaymentStatus, PaymentTransaction
from state import AgentState

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

    supplier_cost = state["supplier_response"].total_procurement_cost if state["supplier_response"] else 0.0
    staffing_cost = state["staffing_plan"].total_labor_cost if state["staffing_plan"] else 0.0
    
    # In a real scenario, we would call the Google A2P API here.
    # For now, we simulate the transaction generation via LLM or logic.
    
    transactions = []
    if supplier_cost > 0:
        transactions.append(PaymentTransaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:8]}",
            recipient="MedSupplier_Inc",
            amount=supplier_cost,
            status="completed"
        ))
    
    if staffing_cost > 0:
        transactions.append(PaymentTransaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:8]}",
            recipient="Hospital_Staff_Fund",
            amount=staffing_cost,
            status="completed"
        ))
        
    result = PaymentStatus(
        transactions=transactions,
        total_paid=supplier_cost + staffing_cost,
        status="completed"
    )
    
    return {"payment_status": result, "messages": [f"Payment: Processed ₹{result.total_paid}"]}
