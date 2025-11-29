from langgraph.graph import StateGraph, END
from state import AgentState
from tools import retrieve_rag_context

# Import all agents
from agents.doctor import doctor_node
from agents.pharmacy import pharmacy_node
from agents.supplier import supplier_node
from agents.operations import operations_node
from agents.public_health import public_health_node
from agents.orchestrator import orchestrator_node
from agents.payment import payment_node
from agents.infographic import infographic_node
from agents.telegram_bot import telegram_node

def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("doctor", doctor_node)
    workflow.add_node("pharmacy", pharmacy_node)
    workflow.add_node("supplier", supplier_node)
    workflow.add_node("operations", operations_node)
    workflow.add_node("public_health", public_health_node)
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("payment", payment_node)
    workflow.add_node("infographic", infographic_node)
    workflow.add_node("telegram", telegram_node)

    # 2. Set Entry Point
    workflow.set_entry_point("doctor")

    # 3. Define Sequential Flow
    # Doctor -> Public Health -> Operations -> Pharmacy -> Supplier -> Orchestrator
    workflow.add_edge("doctor", "public_health")
    workflow.add_edge("public_health", "operations")
    workflow.add_edge("operations", "pharmacy")
    workflow.add_edge("pharmacy", "supplier")
    workflow.add_edge("supplier", "orchestrator")

    # 4. Post-Orchestration Flow
    # Orchestrator -> Payment -> Infographic -> Telegram
    workflow.add_edge("orchestrator", "payment")
    workflow.add_edge("payment", "infographic")
    workflow.add_edge("infographic", "telegram")
    workflow.add_edge("telegram", END)

    return workflow.compile()

if __name__ == "__main__":
    app = build_graph()
    
    initial_state = {
        "location_zone": "Mumbai-West",
        "current_time": "2025-11-28T10:00:00",
        "rag_context": retrieve_rag_context("Mumbai-West"),
        "messages": []
    }
    
    print("### RUNNING HEALTHCARE SURGE GRAPH ###\n")
    
    try:
        result = app.invoke(initial_state)
        
        dec = result['final_decision']
        print("\n\n=== ORCHESTRATOR REPORT ===")
        print(f"Risk Level: {dec.risk_level.upper()}")
        print(f"Human Approval Required: {dec.human_approval_required}")
        print(f"Execution Plan: {dec.execution_plan}")
        
        if result['public_advisory']:
            print(f"Public Advisory: {result['public_advisory'].title}")
            
        if result.get('payment_status'):
            print(f"Payments Processed: ₹{result['payment_status'].total_paid}")
            
        if result.get('telegram_status') and result['telegram_status'].sent:
            print("Telegram Alert: SENT")
            
    except Exception as e:
        print(f"Graph execution failed: {e}")