def retrieve_rag_context(zone: str) -> str:
    """Simulates RAG retrieval from Vector DB (Chroma/Weaviate)"""
    return f"""
    [SOCIAL] Twitter/Reddit in {zone}: 300% spike in 'difficulty breathing' keywords.
    [ENV] AQI: 310 (Hazardous). Pollen count: High.
    [ER_STATS] Yesterday: 120 patients. Trend: +15% per hour.
    [SOP_CLINICAL] Respiratory Distress Protocol v2.1: 
       - 1 Doctor per 10 Severe patients.
       - Steroids and Inhalers prioritized.
    [SOP_SUPPLY] Auto-approve orders < 5000 INR.
    """

def get_inventory_snapshot(zone: str):
    """Simulates DB Read: Inventory"""
    return [
        {"id": "med_1", "name": "Salbutamol Inhaler", "stock": 40, "min_level": 100},
        {"id": "med_2", "name": "Prednisolone", "stock": 500, "min_level": 200}
    ]

def query_supplier_api(medicine_id: str, quantity: int):
    """Simulates External Supplier API"""
    # Simulate a partial shortage for realism
    if medicine_id == "med_1": # Inhaler
        return {
            "supplier": "MedCorp India Pvt Ltd",
            "available": min(quantity, 50), # Cap at 50
            "unit_cost": 350.0, # INR
            "eta_hours": 24,
            "expedite_cost": 2500.0 # INR
        }
    return {
        "supplier": "PharmaFast India",
        "available": quantity,
        "unit_cost": 15.0, # INR
        "eta_hours": 48,
        "expedite_cost": 800.0 # INR
    }

def get_roster(zone: str):
    """Simulates DB Read: Staff"""
    return {"doctors_on_call": 5, "nurses_on_call": 12}