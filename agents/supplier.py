from langchain_core.prompts import ChatPromptTemplate
from config import llm_light
from schemas import SupplierResponse, SupplierOffer
from state import AgentState
from tools import query_supplier_api

supplier_prompt = ChatPromptTemplate.from_template(
    """
    You are **SupplierAgent**. You aggregate API results into a procurement plan.
    
    INPUT:
    - API Results: {api_results}
    
    TASK:
    - Sum total costs.
    - Assess risk: If any item has 'available' < 'requested', Risk = High.
    - If ETA > 24h, Risk = Medium.
    
    OUTPUT: Strict JSON (SupplierResponse).
    """
)

def supplier_node(state: AgentState):
    print("--- SUPPLIER AGENT (OpenAI) ---")
    plan = state["pharmacy_plan"]
    
    if not plan or not plan.items_to_reorder:
        # No reorders needed
        return {"supplier_response": None, "messages": ["Supplier: No orders needed."]}

    # Simulate calling external APIs for each item
    api_results = []
    for item in plan.items_to_reorder:
        data = query_supplier_api(item.medicine_id, item.quantity_needed)
        # In a real app, this data processing would be in Python, 
        # but we use LLM to summarize/format the risk assessment
        data['requested_id'] = item.medicine_id
        data['requested_qty'] = item.quantity_needed
        api_results.append(data)

    chain = supplier_prompt | llm_light.with_structured_output(SupplierResponse)
    result = chain.invoke({"api_results": str(api_results)})
    
    return {"supplier_response": result, "messages": [f"Supplier: Cost calculated {result.total_procurement_cost}"]}