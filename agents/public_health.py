from langchain_core.prompts import ChatPromptTemplate
from config import llm_heavy
from schemas import PublicAdvisory
from state import AgentState

health_prompt = ChatPromptTemplate.from_template(
    """
    You are **PublicHealthAgent**. Draft a public advisory if the situation warrants it.
    
    CONTEXT:
    - Forecast: {forecast}
    - Zone: {zone}
    
    TASK:
    - If severe patients > 10 OR total > 100: Issue Warning.
    - Else: Issue Info.
    - Write a clear, empathetic title and message.
    - Select channels (SMS, App, Social).
    
    OUTPUT: Strict JSON (PublicAdvisory).
    """
)

def public_health_node(state: AgentState):
    print("--- PUBLIC HEALTH AGENT (Gemini) ---")
    chain = health_prompt | llm_heavy.with_structured_output(PublicAdvisory)
    result = chain.invoke({
        "forecast": state["forecast"].model_dump_json(),
        "zone": state["location_zone"]
    })
    return {"public_advisory": result, "messages": ["PublicHealth: Advisory drafted."]}