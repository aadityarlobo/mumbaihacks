from langchain_core.prompts import ChatPromptTemplate
from config import llm_heavy
from schemas import SurgeForecast
from state import AgentState

doctor_prompt = ChatPromptTemplate.from_template(
    """
    You are **DoctorAgent**. Forecast patient demand based on clinical signals.
    
    CONTEXT:
    Zone: {zone} | Time: {time}
    Evidence: {rag_data}
    
    TASK:
    1. Estimate total patient volume for next 48h.
    2. Categorize by severity (Mild/Moderate/Severe).
    3. Provide confidence score (0.0-1.0).
    
    OUTPUT: Strict JSON (SurgeForecast).
    """
)

def doctor_node(state: AgentState):
    print("--- DOCTOR AGENT (Gemini) ---")
    chain = doctor_prompt | llm_heavy.with_structured_output(SurgeForecast)
    result = chain.invoke({
        "zone": state["location_zone"],
        "time": state["current_time"],
        "rag_data": state["rag_context"]
    })
    return {"forecast": result, "messages": [f"Doctor: Predicted {result.predicted_patients} patients."]}