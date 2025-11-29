from langchain_core.prompts import ChatPromptTemplate
from config import llm_light
from schemas import StaffingPlan
from state import AgentState
from tools import get_roster

ops_prompt = ChatPromptTemplate.from_template(
    """
    You are **OperationsAgent**. Calculate staffing needs.
    
    INPUT:
    - Forecast: {forecast}
    - Roster: {roster}
    
    RULES:
    - 1 Doctor per 20 Mild patients.
    - 1 Doctor per 5 Severe patients.
    - 1 Nurse per 10 patients (any severity).
    - Cost: Doctor 2500/hr, Nurse 800/hr (INR). Shift = 8hrs.
    
    OUTPUT: Strict JSON (StaffingPlan).
    """
)

def operations_node(state: AgentState):
    print("--- OPERATIONS AGENT (OpenAI) ---")
    chain = ops_prompt | llm_light.with_structured_output(StaffingPlan)
    result = chain.invoke({
        "forecast": state["forecast"].model_dump_json(),
        "roster": str(get_roster(state["location_zone"]))
    })
    return {"staffing_plan": result, "messages": ["Operations: Staffing calculated."]}