from langchain_core.prompts import ChatPromptTemplate
from config import llm_heavy
from schemas import FinalDecision, AuditLog
from state import AgentState

orch_prompt = ChatPromptTemplate.from_template(
    """
    You are **OrchestratorAgent**. Review all sub-agent plans and make a GO/NO-GO decision.
    
    INPUTS:
    1. Forecast: {forecast}
    2. Supplier Plan: {supplier}
    3. Staffing Plan: {staffing}
    4. Advisory: {advisory}
    
    RULES:
    - If Total Cost > 50,000 (INR) OR Supplier Risk is High -> Require Human Approval.
    - If Forecast Confidence < 0.7 -> Require Human Approval.
    - Generate an Audit Log entry explaining the decision.
    
    OUTPUT: Strict JSON (FinalDecision).
    """
)

def orchestrator_node(state: AgentState):
    print("--- ORCHESTRATOR (Gemini) ---")
    print(f"State keys: {list(state.keys())}")
    
    # Handle None types safely
    supplier_resp = state.get("supplier_response")
    supplier_dump = supplier_resp.model_dump_json() if supplier_resp else "No Orders"
    
    chain = orch_prompt | llm_heavy.with_structured_output(FinalDecision)
    result = chain.invoke({
        "forecast": state["forecast"].model_dump_json(),
        "supplier": supplier_dump,
        "staffing": state["staffing_plan"].model_dump_json(),
        "advisory": state["public_advisory"].model_dump_json()
    })
    return {"final_decision": result, "messages": ["Orchestrator: Final decision logged."]}