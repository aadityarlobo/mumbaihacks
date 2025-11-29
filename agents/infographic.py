import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas import InfographicContent
from state import AgentState

# Using the specific model requested by the user
llm_nano = ChatGoogleGenerativeAI(
    model="models/nano-banana-pro-preview", # Or fallback to gemini-2.0-flash if this fails
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

infographic_prompt = ChatPromptTemplate.from_template(
    """
    You are **InfographicAgent**. Create content for a public health infographic.
    
    INPUT:
    - Advisory: {advisory}
    - Forecast: {forecast}
    
    TASK:
    1. Create a catchy Title.
    2. Extract 3 Key Stats (e.g., "High Risk", "AQI 300+").
    3. Describe a visual for the infographic (e.g., "Red background with mask icon").
    
    OUTPUT: Strict JSON (InfographicContent).
    """
)

def infographic_node(state: AgentState):
    print("--- INFOGRAPHIC AGENT (Nano Banana) ---")
    
    advisory = state.get("public_advisory")
    if not advisory:
        return {"messages": ["Infographic: Skipped (No Advisory)"]}
        
    try:
        chain = infographic_prompt | llm_nano.with_structured_output(InfographicContent)
        result = chain.invoke({
            "advisory": advisory.model_dump_json(),
            "forecast": state["forecast"].model_dump_json()
        })
    except Exception as e:
        print(f"Nano model failed, falling back to standard: {e}")
        # Fallback logic if the specific model isn't available or fails
        from config import llm_light
        chain = infographic_prompt | llm_light.with_structured_output(InfographicContent)
        result = chain.invoke({
            "advisory": advisory.model_dump_json(),
            "forecast": state["forecast"].model_dump_json()
        })

    # In a real app, we would generate the image here using PIL/Matplotlib based on result.visual_description
    # For now, we just return the content.
    result.image_path = "/tmp/infographic_placeholder.png" 
    
    return {"infographic": result, "messages": ["Infographic: Content generated."]}
