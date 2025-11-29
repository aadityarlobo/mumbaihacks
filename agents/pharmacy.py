import json
from langchain_core.prompts import ChatPromptTemplate
from config import llm_light
from schemas import PharmacyPlan
from state import AgentState
from tools import get_inventory_snapshot

pharmacy_prompt = ChatPromptTemplate.from_template(
    """
    You are **PharmacyAgent**. Calculate inventory gaps.
    
    INPUT:
    - Forecast: {forecast}
    - Inventory: {inventory}
    
    RULES:
    - Severe patients need 1 Inhaler (med_1).
    - All patients need 2 tablets of Prednisolone (med_2).
    - If Stock < (Demand + 10% Buffer), mark for reorder.
    
    OUTPUT: Strict JSON (PharmacyPlan).
    """
)

def pharmacy_node(state: AgentState):
    print("--- PHARMACY AGENT (OpenAI) ---")
    forecast = state["forecast"]
    inv = get_inventory_snapshot(state["location_zone"])
    
    chain = pharmacy_prompt | llm_light.with_structured_output(PharmacyPlan)
    result = chain.invoke({
        "forecast": forecast.model_dump_json(),
        "inventory": json.dumps(inv)
    })
    return {"pharmacy_plan": result, "messages": [f"Pharmacy: Need to reorder {len(result.items_to_reorder)} items."]}