import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class Medicine:
    medicine_id: int = strawberry.field(name="medicineId")
    name: str
    category: str
    unit_price: float = strawberry.field(name="unitPrice")
    manufacturer: str
    description: str
    requires_prescription: bool = strawberry.field(name="requiresPrescription")
    storage_conditions: str = strawberry.field(name="storageConditions")
    created_at: str = strawberry.field(name="createdAt")
    updated_at: str = strawberry.field(name="updatedAt")

@strawberry.type
class Inventory:
    inventory_id: int = strawberry.field(name="inventoryId")
    medicine_id: int = strawberry.field(name="medicineId")
    current_stock: int = strawberry.field(name="currentStock")
    reorder_level: int = strawberry.field(name="reorderLevel")
    maximum_stock: int = strawberry.field(name="maximumStock")
    location: str
    batch_number: str = strawberry.field(name="batchNumber")
    expiry_date: str = strawberry.field(name="expiryDate")
    last_restocked_date: str = strawberry.field(name="lastRestockedDate")
    last_updated: str = strawberry.field(name="lastUpdated")

@strawberry.type
class Patient:
    patient_id: int = strawberry.field(name="patientId")
    name: str
    age: int
    gender: str
    contact_number: str = strawberry.field(name="contactNumber")
    email: str
    address: str
    blood_group: str = strawberry.field(name="bloodGroup")
    emergency_contact: str = strawberry.field(name="emergencyContact")
    created_at: str = strawberry.field(name="createdAt")
    updated_at: str = strawberry.field(name="updatedAt")

@strawberry.type
class ERVisit:
    visit_id: int = strawberry.field(name="visitId")
    patient_id: int = strawberry.field(name="patientId")
    visit_datetime: str = strawberry.field(name="visitDatetime")
    chief_complaint: str = strawberry.field(name="chiefComplaint")
    severity: str
    wait_time_minutes: int = strawberry.field(name="waitTimeMinutes")
    treatment_duration_minutes: int = strawberry.field(name="treatmentDurationMinutes")
    attending_staff_id: int = strawberry.field(name="attendingStaffId")
    outcome: str
    medicines_prescribed: str = strawberry.field(name="medicinesPrescribed")
    total_cost: float = strawberry.field(name="totalCost")
    created_at: str = strawberry.field(name="createdAt")
    updated_at: str = strawberry.field(name="updatedAt")

@strawberry.type
class Staff:
    staff_id: int = strawberry.field(name="staffId")
    name: str
    role: str
    department: str
    contact_number: str = strawberry.field(name="contactNumber")
    email: str
    qualification: str
    experience_years: int = strawberry.field(name="experienceYears")
    shift_preference: str = strawberry.field(name="shiftPreference")
    hourly_rate: float = strawberry.field(name="hourlyRate")
    is_active: bool = strawberry.field(name="isActive")
    hired_date: str = strawberry.field(name="hiredDate")
    created_at: str = strawberry.field(name="createdAt")
    updated_at: str = strawberry.field(name="updatedAt")

@strawberry.type
class Schedule:
    schedule_id: int = strawberry.field(name="scheduleId")
    staff_id: int = strawberry.field(name="staffId")
    shift_date: str = strawberry.field(name="shiftDate")
    shift_type: str = strawberry.field(name="shiftType")
    start_time: str = strawberry.field(name="startTime")
    end_time: str = strawberry.field(name="endTime")
    status: str
    created_at: str = strawberry.field(name="createdAt")
    updated_at: str = strawberry.field(name="updatedAt")

@strawberry.type
class Supplier:
    supplier_id: int = strawberry.field(name="supplierId")
    name: str
    contact_person: str = strawberry.field(name="contactPerson")
    phone: str
    email: str
    address: str
    city: str
    state: str
    pincode: str
    rating: float
    payment_terms: str = strawberry.field(name="paymentTerms")
    created_at: str = strawberry.field(name="createdAt")
    updated_at: str = strawberry.field(name="updatedAt")

@strawberry.type
class SupplierMedicine:
    supplier_medicine_id: int = strawberry.field(name="supplierMedicineId")
    supplier_id: int = strawberry.field(name="supplierId")
    medicine_id: int = strawberry.field(name="medicineId")
    supply_price: float = strawberry.field(name="supplyPrice")
    lead_time_days: int = strawberry.field(name="leadTimeDays")
    minimum_order_quantity: int = strawberry.field(name="minimumOrderQuantity")
    is_preferred: bool = strawberry.field(name="isPreferred")
    last_supplied_date: Optional[str] = strawberry.field(default=None, name="lastSuppliedDate")
    created_at: str = strawberry.field(name="createdAt")

@strawberry.type
class EnvironmentalData:
    env_data_id: int = strawberry.field(name="envDataId")
    recorded_at: str = strawberry.field(name="recordedAt")
    temperature_celsius: float = strawberry.field(name="temperatureCelsius")
    humidity_percent: float = strawberry.field(name="humidityPercent")
    air_quality_index: int = strawberry.field(name="airQualityIndex")
    precipitation_mm: float = strawberry.field(name="precipitationMm")
    wind_speed_kmh: float = strawberry.field(name="windSpeedKmh")
    pressure_hpa: float = strawberry.field(name="pressureHpa")
    location: str
    source: str
    created_at: str = strawberry.field(name="createdAt")

# Input types for mutations
@strawberry.input
class PatientInput:
    name: str
    age: int
    gender: str
    contact_number: str = strawberry.field(name="contactNumber")
    email: str
    address: str
    blood_group: str = strawberry.field(name="bloodGroup")
    emergency_contact: str = strawberry.field(name="emergencyContact")
    telegram_chat_id: str = strawberry.field(name="chatId")

@strawberry.input
class ERVisitInput:
    patient_id: int = strawberry.field(name="patientId")
    visit_datetime: str = strawberry.field(name="visitDatetime")
    chief_complaint: str = strawberry.field(name="chiefComplaint")
    severity: str
    wait_time_minutes: int = strawberry.field(name="waitTimeMinutes")
    treatment_duration_minutes: int = strawberry.field(name="treatmentDurationMinutes")
    attending_staff_id: int = strawberry.field(name="attendingStaffId")
    outcome: str
    medicines_prescribed: str = strawberry.field(name="medicinesPrescribed")
    total_cost: float = strawberry.field(name="totalCost")

@strawberry.input
class InventoryUpdateInput:
    inventory_id: int = strawberry.field(name="inventoryId")
    current_stock: int = strawberry.field(name="currentStock")