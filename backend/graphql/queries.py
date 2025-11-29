import strawberry
from typing import List, Optional
from backend.schemas.graphql_types import (
    EnvironmentalData, ERVisit, Inventory, Medicine,
    Patient, Schedule, Staff, Supplier, SupplierMedicine
)
from backend.database import db

@strawberry.type
class Query:
    
    # Medicine Queries
    @strawberry.field
    def medicines(self) -> List[Medicine]:
        query = """
            SELECT medicine_id, name, category, unit_price, manufacturer, 
                   description, requires_prescription, storage_conditions, 
                   created_at, updated_at
            FROM medicines ORDER BY name
        """
        rows = db.execute_query(query)
        return [Medicine(**dict(row)) for row in rows]
    
    @strawberry.field
    def medicine_by_id(self, medicine_id: int) -> Optional[Medicine]:
        query = """
            SELECT medicine_id, name, category, unit_price, manufacturer, 
                   description, requires_prescription, storage_conditions, 
                   created_at, updated_at
            FROM medicines WHERE medicine_id = %s
        """
        row = db.execute_query(query, (medicine_id,), fetch="one")
        return Medicine(**dict(row)) if row else None
    
    # Inventory Queries
    @strawberry.field
    def inventory(self) -> List[Inventory]:
        query = """
            SELECT inventory_id, medicine_id, current_stock, reorder_level,
                   maximum_stock, location, batch_number, expiry_date,
                   last_restocked_date, last_updated
            FROM inventory ORDER BY inventory_id
        """
        rows = db.execute_query(query)
        return [Inventory(**dict(row)) for row in rows]
    
    @strawberry.field
    def inventory_by_id(self, inventory_id: int) -> Optional[Inventory]:
        query = """
            SELECT inventory_id, medicine_id, current_stock, reorder_level,
                   maximum_stock, location, batch_number, expiry_date,
                   last_restocked_date, last_updated
            FROM inventory WHERE inventory_id = %s
        """
        row = db.execute_query(query, (inventory_id,), fetch="one")
        return Inventory(**dict(row)) if row else None
    
    @strawberry.field
    def low_stock_medicines(self) -> List[Inventory]:
        query = """
            SELECT inventory_id, medicine_id, current_stock, reorder_level,
                   maximum_stock, location, batch_number, expiry_date,
                   last_restocked_date, last_updated
            FROM inventory WHERE current_stock <= reorder_level
        """
        rows = db.execute_query(query)
        return [Inventory(**dict(row)) for row in rows]
    
    # Patient Queries
    @strawberry.field
    def patients(self, limit: Optional[int] = 100) -> List[Patient]:
        query = """
            SELECT patient_id, name, age, gender, contact_number, email,
                   address, blood_group, emergency_contact, created_at, updated_at
            FROM patients ORDER BY patient_id LIMIT %s
        """
        rows = db.execute_query(query, (limit,))
        return [Patient(**dict(row)) for row in rows]
    
    @strawberry.field
    def patient_by_id(self, patient_id: int) -> Optional[Patient]:
        query = """
            SELECT patient_id, name, age, gender, contact_number, email,
                   address, blood_group, emergency_contact, created_at, updated_at
            FROM patients WHERE patient_id = %s
        """
        row = db.execute_query(query, (patient_id,), fetch="one")
        return Patient(**dict(row)) if row else None
    
    # ER Visits Queries
    @strawberry.field
    def er_visits(self, limit: Optional[int] = 100) -> List[ERVisit]:
        query = """
            SELECT visit_id, patient_id, visit_datetime, chief_complaint,
                   severity, wait_time_minutes, treatment_duration_minutes,
                   attending_staff_id, outcome, medicines_prescribed,
                   total_cost, created_at, updated_at
            FROM er_visits ORDER BY visit_datetime DESC LIMIT %s
        """
        rows = db.execute_query(query, (limit,))
        return [ERVisit(**dict(row)) for row in rows]
    
    @strawberry.field
    def er_visit_by_id(self, visit_id: int) -> Optional[ERVisit]:
        query = """
            SELECT visit_id, patient_id, visit_datetime, chief_complaint,
                   severity, wait_time_minutes, treatment_duration_minutes,
                   attending_staff_id, outcome, medicines_prescribed,
                   total_cost, created_at, updated_at
            FROM er_visits WHERE visit_id = %s
        """
        row = db.execute_query(query, (visit_id,), fetch="one")
        return ERVisit(**dict(row)) if row else None
    
    # Staff Queries
    @strawberry.field
    def staff(self) -> List[Staff]:
        query = """
            SELECT staff_id, name, role, department, contact_number, email,
                   qualification, experience_years, shift_preference,
                   hourly_rate, is_active, hired_date, created_at, updated_at
            FROM staff ORDER BY name
        """
        rows = db.execute_query(query)
        return [Staff(**dict(row)) for row in rows]
    
    @strawberry.field
    def staff_by_id(self, staff_id: int) -> Optional[Staff]:
        query = """
            SELECT staff_id, name, role, department, contact_number, email,
                   qualification, experience_years, shift_preference,
                   hourly_rate, is_active, hired_date, created_at, updated_at
            FROM staff WHERE staff_id = %s
        """
        row = db.execute_query(query, (staff_id,), fetch="one")
        return Staff(**dict(row)) if row else None
    
    # Schedule Queries
    @strawberry.field
    def schedules(self, limit: Optional[int] = 100) -> List[Schedule]:
        query = """
            SELECT schedule_id, staff_id, shift_date, shift_type,
                   start_time, end_time, status, created_at, updated_at
            FROM schedules ORDER BY shift_date DESC LIMIT %s
        """
        rows = db.execute_query(query, (limit,))
        return [Schedule(**dict(row)) for row in rows]
    
    # Supplier Queries
    @strawberry.field
    def suppliers(self) -> List[Supplier]:
        query = """
            SELECT supplier_id, name, contact_person, phone, email,
                   address, city, state, pincode, rating, payment_terms,
                   created_at, updated_at
            FROM suppliers ORDER BY name
        """
        rows = db.execute_query(query)
        return [Supplier(**dict(row)) for row in rows]
    
    @strawberry.field
    def supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        query = """
            SELECT supplier_id, name, contact_person, phone, email,
                   address, city, state, pincode, rating, payment_terms,
                   created_at, updated_at
            FROM suppliers WHERE supplier_id = %s
        """
        row = db.execute_query(query, (supplier_id,), fetch="one")
        return Supplier(**dict(row)) if row else None
    
    # Supplier Medicine Queries
    @strawberry.field
    def supplier_medicines(self) -> List[SupplierMedicine]:
        query = """
            SELECT supplier_medicine_id, supplier_id, medicine_id,
                   supply_price, lead_time_days, minimum_order_quantity,
                   is_preferred, last_supplied_date, created_at
            FROM supplier_medicines ORDER BY supplier_medicine_id
        """
        rows = db.execute_query(query)
        return [SupplierMedicine(**dict(row)) for row in rows]
    
    # Environmental Data Queries
    @strawberry.field
    def environmental_data(self, limit: Optional[int] = 100) -> List[EnvironmentalData]:
        query = """
            SELECT env_data_id, recorded_at, temperature_celsius,
                   humidity_percent, air_quality_index, precipitation_mm,
                   wind_speed_kmh, pressure_hpa, location, source, created_at
            FROM environmental_data ORDER BY recorded_at DESC LIMIT %s
        """
        rows = db.execute_query(query, (limit,))
        return [EnvironmentalData(**dict(row)) for row in rows]