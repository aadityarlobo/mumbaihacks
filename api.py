"""
FastAPI Backend for HealthForce Goa
Connects the React UI with the LangGraph Multi-Agent System
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import asyncio

from langgraph.graph import StateGraph, END
from state import AgentState
from tools import retrieve_rag_context, get_inventory_snapshot, get_roster
from schemas import (
    SurgeForecast, PharmacyPlan, StaffingPlan, 
    SupplierResponse, PublicAdvisory, FinalDecision,
    PaymentStatus, InfographicContent, TelegramStatus
)

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

app = FastAPI(
    title="HealthForce Goa API",
    description="Multi-Agent Healthcare Surge Management System",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for surge runs (in production, use Redis/DB)
surge_runs: Dict[str, Dict[str, Any]] = {}


# ============== REQUEST/RESPONSE MODELS ==============

class SurgeRequest(BaseModel):
    location_zone: str = Field(default="Mumbai-West", description="Zone to analyze")
    current_time: Optional[str] = Field(default=None, description="ISO timestamp")

class SurgeResponse(BaseModel):
    run_id: str
    status: str
    message: str

class SurgeStatusResponse(BaseModel):
    run_id: str
    status: str  # pending, running, completed, failed
    progress: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class DemoRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    organization_type: str
    interest_areas: List[str] = []

class LoginRequest(BaseModel):
    role: str  # hospital, pharmacy, patient
    identifier: str  # employee ID, mobile, etc.
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    role: str
    message: str

class ApproveActionRequest(BaseModel):
    run_id: str
    approved: bool
    modified_plan: Optional[str] = None


# ============== GRAPH BUILDER ==============

def build_graph():
    """Build the LangGraph workflow"""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("doctor", doctor_node)
    workflow.add_node("pharmacy", pharmacy_node)
    workflow.add_node("supplier", supplier_node)
    workflow.add_node("operations", operations_node)
    workflow.add_node("public_health", public_health_node)
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("payment", payment_node)
    workflow.add_node("infographic", infographic_node)
    workflow.add_node("telegram", telegram_node)

    # Set Entry Point
    workflow.set_entry_point("doctor")

    # Define Sequential Flow
    workflow.add_edge("doctor", "public_health")
    workflow.add_edge("public_health", "operations")
    workflow.add_edge("operations", "pharmacy")
    workflow.add_edge("pharmacy", "supplier")
    workflow.add_edge("supplier", "orchestrator")

    # Post-Orchestration Flow
    workflow.add_edge("orchestrator", "payment")
    workflow.add_edge("payment", "infographic")
    workflow.add_edge("infographic", "telegram")
    workflow.add_edge("telegram", END)

    return workflow.compile()


# ============== HELPER FUNCTIONS ==============

def serialize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize pydantic models in result to dict"""
    serialized = {}
    for key, value in result.items():
        if hasattr(value, 'model_dump'):
            serialized[key] = value.model_dump()
        elif isinstance(value, list):
            serialized[key] = [
                item.model_dump() if hasattr(item, 'model_dump') else item 
                for item in value
            ]
        else:
            serialized[key] = value
    return serialized


async def run_surge_analysis(run_id: str, location_zone: str, current_time: str):
    """Background task to run the full surge analysis"""
    try:
        surge_runs[run_id]["status"] = "running"
        surge_runs[run_id]["progress"] = "Initializing agents..."
        
        # Build the graph
        graph = build_graph()
        
        # Initial state
        initial_state = {
            "location_zone": location_zone,
            "current_time": current_time,
            "rag_context": retrieve_rag_context(location_zone),
            "messages": []
        }
        
        surge_runs[run_id]["progress"] = "Running Doctor Agent..."
        
        # Run the graph
        result = graph.invoke(initial_state)
        
        # Serialize and store result
        surge_runs[run_id]["status"] = "completed"
        surge_runs[run_id]["result"] = serialize_result(result)
        surge_runs[run_id]["progress"] = "Analysis complete"
        
    except Exception as e:
        surge_runs[run_id]["status"] = "failed"
        surge_runs[run_id]["error"] = str(e)


# ============== API ENDPOINTS ==============

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "HealthForce Goa API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "operational",
        "agents": {
            "doctor": "ready",
            "pharmacy": "ready",
            "supplier": "ready",
            "operations": "ready",
            "public_health": "ready",
            "orchestrator": "ready",
            "payment": "ready",
            "infographic": "ready",
            "telegram": "ready"
        },
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/surge/run", response_model=SurgeResponse)
async def run_surge(request: SurgeRequest, background_tasks: BackgroundTasks):
    """
    Start a new surge analysis run.
    This triggers the full multi-agent pipeline in the background.
    """
    run_id = f"SURGE-{uuid.uuid4().hex[:8].upper()}"
    current_time = request.current_time or datetime.now().isoformat()
    
    # Initialize run tracking
    surge_runs[run_id] = {
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "location_zone": request.location_zone,
        "progress": "Queued",
        "result": None,
        "error": None
    }
    
    # Start background task
    background_tasks.add_task(
        run_surge_analysis, 
        run_id, 
        request.location_zone, 
        current_time
    )
    
    return SurgeResponse(
        run_id=run_id,
        status="pending",
        message=f"Surge analysis started for {request.location_zone}"
    )


@app.get("/api/surge/status/{run_id}", response_model=SurgeStatusResponse)
async def get_surge_status(run_id: str):
    """Get the status of a surge analysis run"""
    if run_id not in surge_runs:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run = surge_runs[run_id]
    return SurgeStatusResponse(
        run_id=run_id,
        status=run["status"],
        progress=run.get("progress"),
        result=run.get("result"),
        error=run.get("error")
    )


@app.get("/api/surge/list")
async def list_surge_runs():
    """List all surge analysis runs"""
    return {
        "runs": [
            {
                "run_id": run_id,
                "status": run["status"],
                "created_at": run["created_at"],
                "location_zone": run["location_zone"]
            }
            for run_id, run in surge_runs.items()
        ]
    }


@app.post("/api/surge/approve")
async def approve_action(request: ApproveActionRequest):
    """Approve or reject an orchestrator's recommended action"""
    if request.run_id not in surge_runs:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run = surge_runs[request.run_id]
    if run["status"] != "completed":
        raise HTTPException(status_code=400, detail="Run not yet completed")
    
    # In a real implementation, this would trigger payment/execution
    return {
        "run_id": request.run_id,
        "approved": request.approved,
        "message": "Action approved and payments initiated" if request.approved else "Action rejected",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/demo/book")
async def book_demo(request: DemoRequest):
    """Book a demo request"""
    # In production, this would save to a database and send emails
    demo_id = f"DEMO-{uuid.uuid4().hex[:8].upper()}"
    
    return {
        "success": True,
        "demo_id": demo_id,
        "message": f"Demo scheduled successfully for {request.first_name} {request.last_name}",
        "email": request.email,
        "organization": request.organization_type,
        "interests": request.interest_areas
    }


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate a user based on their role.
    In production, this would verify against a real auth system.
    """
    # Demo authentication - accepts any credentials
    # In production, verify against real auth system
    token = f"TOKEN-{uuid.uuid4().hex}"
    
    return LoginResponse(
        success=True,
        token=token,
        role=request.role,
        message=f"Successfully logged in as {request.role}"
    )


@app.get("/api/dashboard/{role}")
async def get_dashboard_data(role: str):
    """Get role-specific dashboard data"""
    
    base_alerts = {
        "hospital": {
            "alerts": [
                {
                    "type": "critical",
                    "message": "Predicted surge of +420 patients in next 48h. Staffing shortage detected.",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "stats": {
                "predicted_patients": 420,
                "current_staff": 17,
                "recommended_staff": 25,
                "risk_level": "high"
            }
        },
        "pharmacy": {
            "alerts": [
                {
                    "type": "warning",
                    "message": "Paracetamol stock below safety buffer (15%). Auto-reorder pending approval.",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "stats": {
                "items_low_stock": 3,
                "pending_orders": 2,
                "total_inventory_value": 125000
            }
        },
        "patient": {
            "alerts": [
                {
                    "type": "advisory",
                    "message": "Air Quality Index is 'Severe' (450+). Respiratory cases rising. Wear a mask.",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "stats": {
                "aqi": 450,
                "risk_level": "severe",
                "nearest_hospital_wait": "15 mins"
            }
        }
    }
    
    if role not in base_alerts:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    return base_alerts[role]


@app.get("/api/inventory/{zone}")
async def get_inventory(zone: str):
    """Get current inventory snapshot for a zone"""
    inventory = get_inventory_snapshot(zone)
    roster = get_roster(zone)
    
    return {
        "zone": zone,
        "inventory": inventory,
        "roster": roster,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/forecast/{zone}")
async def get_forecast(zone: str):
    """Get the latest forecast for a zone"""
    # Check if there's a recent completed run for this zone
    recent_runs = [
        run for run_id, run in surge_runs.items()
        if run["location_zone"] == zone and run["status"] == "completed"
    ]
    
    if recent_runs:
        latest = recent_runs[-1]
        return {
            "zone": zone,
            "forecast": latest["result"].get("forecast"),
            "source": "live_analysis"
        }
    
    # Return simulated forecast if no runs exist
    return {
        "zone": zone,
        "forecast": {
            "zone": zone,
            "predicted_patients": 420,
            "severity_breakdown": {"mild": 280, "moderate": 100, "severe": 40},
            "confidence": 0.85,
            "reasoning": "Based on Twitter signals and ER log trends",
            "timestamp": datetime.now().isoformat()
        },
        "source": "simulated"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
