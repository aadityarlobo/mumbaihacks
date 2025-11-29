import strawberry
from typing import Optional
from datetime import datetime
from backend.schemas.graphql_types import (
    Patient, ERVisit, Inventory, PatientInput, 
    ERVisitInput, InventoryUpdateInput
)
from backend.database import db

@strawberry.type
class Mutation:
    
    # Patient Mutations
    @strawberry.mutation
    def add_patient(self, patient: PatientInput) -> Patient:
        query = """
            INSERT INTO patients 
            (first_name, last_name, date_of_birth, gender, blood_type, phone, 
             email, address, emergency_contact, medical_history, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (
            patient.first_name, patient.last_name, patient.date_of_birth,
            patient.gender, patient.blood_type, patient.phone, patient.email,
            patient.address, patient.emergency_contact, patient.medical_history,
            datetime.now().isoformat()
        )
        row = db.execute_query(query, params, fetch="one")
        return Patient(**dict(row))
    
    @strawberry.mutation
    def update_patient(
        self, 
        patient_id: int, 
        patient: PatientInput
    ) -> Optional[Patient]:
        query = """
            UPDATE patients SET
                first_name = %s, last_name = %s, date_of_birth = %s,
                gender = %s, blood_type = %s, phone = %s, email = %s,
                address = %s, emergency_contact = %s, medical_history = %s
            WHERE patient_id = %s
            RETURNING *
        """
        params = (
            patient.first_name, patient.last_name, patient.date_of_birth,
            patient.gender, patient.blood_type, patient.phone, patient.email,
            patient.address, patient.emergency_contact, patient.medical_history,
            patient_id
        )
        row = db.execute_query(query, params, fetch="one")
        return Patient(**dict(row)) if row else None
    
    @strawberry.mutation
    def delete_patient(self, patient_id: int) -> bool:
        query = "DELETE FROM patients WHERE patient_id = %s"
        db.execute_query(query, (patient_id,), fetch=None)
        return True
    
    # ER Visit Mutations
    @strawberry.mutation
    def add_er_visit(self, visit: ERVisitInput) -> ERVisit:
        query = """
            INSERT INTO er_visits 
            (patient_id, arrival_time, triage_level, chief_complaint, 
             vitals, treatment_summary, discharge_time, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (
            visit.patient_id, visit.arrival_time, visit.triage_level,
            visit.chief_complaint, visit.vitals, visit.treatment_summary,
            visit.discharge_time, datetime.now().isoformat()
        )
        row = db.execute_query(query, params, fetch="one")
        return ERVisit(**dict(row))
    
    @strawberry.mutation
    def update_er_visit_discharge(
        self, 
        visit_id: int, 
        discharge_time: str
    ) -> Optional[ERVisit]:
        query = """
            UPDATE er_visits SET discharge_time = %s 
            WHERE visit_id = %s
            RETURNING *
        """
        row = db.execute_query(query, (discharge_time, visit_id), fetch="one")
        return ERVisit(**dict(row)) if row else None
    
    # Inventory Mutations
    @strawberry.mutation
    def update_inventory(
        self, 
        update: InventoryUpdateInput
    ) -> Optional[Inventory]:
        query = """
            UPDATE inventory SET quantity_in_stock = %s 
            WHERE inventory_id = %s
            RETURNING *
        """
        row = db.execute_query(
            query, 
            (update.quantity_in_stock, update.inventory_id), 
            fetch="one"
        )
        return Inventory(**dict(row)) if row else None
    
    @strawberry.mutation
    def restock_inventory(
        self, 
        inventory_id: int, 
        quantity: int
    ) -> Optional[Inventory]:
        query = """
            UPDATE inventory 
            SET quantity_in_stock = quantity_in_stock + %s,
                last_restocked = %s
            WHERE inventory_id = %s
            RETURNING *
        """
        row = db.execute_query(
            query, 
            (quantity, datetime.now().isoformat(), inventory_id), 
            fetch="one"
        )
        return Inventory(**dict(row)) if row else None