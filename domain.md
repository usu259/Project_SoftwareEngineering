```mermaid
classDiagram
 
%% ─── VALUE OBJECTS ───────────────────────────────────────────
class Address {
    <<value object>>
    +street : str
    +city : str
    +zip_code : str
    +country : str
}
 
%% ─── PERSONS ──────────────────────────────────────────────────
class Person {
    <<abstract>>
    #_first_name : str
    #_last_name : str
    #_email : str
    +first_name() str
    +last_name() str
    +email() str
    +full_name() str
    +update_name(first_name, last_name) None
    +update_email(email) None
    #_validate_name(value, field) str
    #_validate_email(value) str
}
 
class Customer {
    -_phone : str
    -_address : Address
    -_id : int | None
    +phone() str
    +address() Address
    +id() int | None
    +update_contact(email, phone) None
    +update_address(address) None
    #_validate_phone(value) str
    #_validate_address(value) Address
}
 
class Employee {
    -_role : EmployeeRole
    -_id : int | None
    +role() EmployeeRole
    +id() int | None
    +update_role(role) None
    #_validate_role(value) EmployeeRole
}
 
class EmployeeRole {
    <<enumeration>>
    GARDENER
    BRICKLAYER
    OWNER
}
 
Person <|-- Customer
Person <|-- Employee
Employee --> EmployeeRole
Customer --> Address
 
%% ─── CATALOGUE ENTITIES ──────────────────────────────────────
class Material {
    -_id : int | None
    -_name : str
    -_unit : str
    -_cost_per_unit : float
    +id() int | None
    +name() str
    +unit() str
    +cost_per_unit() float
    +update_price(cost_per_unit) None
}
 
class Work {
    -_id : int | None
    -_name : str
    -_cost_per_hour : float
    -_employee : Employee
    +id() int | None
    +name() str
    +cost_per_hour() float
    +update_price(cost_per_hour) None
}
 
Work --> Employee
 
%% ─── POSITIONS (Strategy pattern) ───────────────────────────
class Position {
    <<abstract>>
    +type() PositionType
    +name() str
    +description() str
    +cost() float
}
 
class PositionType {
    <<enumeration>>
    MATERIAL
    WORK
    TEXT
}
 
class MaterialPosition {
    -_material : Material
    -_cost_per_unit_at_entry : float
    -_number_units : float
    +cost() float
}
 
class WorkPosition {
    -_work : Work
    -_cost_per_hour_at_entry : float
    -_number_hours : float
    +cost() float
}
 
class TextPosition {
    -_name : str
    -_description : str
    -_total_cost : float
    +cost() float
}
 
Position <|-- MaterialPosition
Position <|-- WorkPosition
Position <|-- TextPosition
Position --> PositionType
MaterialPosition --> Material
WorkPosition --> Work
 
%% ─── WORK REPORT ─────────────────────────────────────────────
class WorkReport {
    -_id : int | None
    -_customer_id : int
    -_invoice_id : int | None
    -_employee_id : int
    -_title : str
    -_description : str
    -_execution_date : date
    -_deleted : bool
    +id() int | None
    +locked() bool
    +assigned_to_invoice() bool
    +add_position(position) None
    +remove_position(position) None
    +get_total_cost() float
    +change_title(title) None
    +change_description(description) None
    +mark_deleted() None
}
 
WorkReport "1" --> "0..*" Position : contains
 
%% ─── INVOICE (Aggregate Root) ────────────────────────────────
class Invoice {
    -_id : int | None
    -_customer_id : int
    -_title : str
    -_description : str
    -_creation_date : date
    -_status : InvoiceStatus
    -_deleted : bool
    +id() int | None
    +locked() bool
    +get_total_cost() float
    +add_work_report(work_report) None
    +remove_work_report(work_report) None
    +change_status(status) None
    +change_title(title) None
    +mark_deleted() None
}
 
class InvoiceStatus {
    <<enumeration>>
    CREATED
    SENT
    PAID
}
 
Invoice --> InvoiceStatus
Invoice --> Customer : billed to
Invoice "1" --> "1..*" WorkReport : groups
 
%% ─── OWNERSHIP NOTE ──────────────────────────────────────────
Customer "1" --> "0..*" WorkReport : owns
Customer "1" --> "0..*" Invoice : owns