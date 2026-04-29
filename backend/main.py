from datetime import datetime
from typing import Any, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = FastAPI(title="My AWS ERP Test Platform API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Pydantic Models
# =========================

class EmployeeCreate(BaseModel):
    full_name: str
    role: str
    department: str
    active: bool = True


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    active: Optional[bool] = None


class InventoryCreate(BaseModel):
    sku: str
    item_name: str
    quantity: int = 0
    unit_cost: float


class InventoryUpdate(BaseModel):
    sku: Optional[str] = None
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    unit_cost: Optional[float] = None


class OrderCreate(BaseModel):
    order_number: str
    customer_name: str
    total_amount: float
    status: str = "PENDING"


class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    customer_name: Optional[str] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None


# =========================
# Database Helpers
# =========================

def fetch_rows(query: str, params: dict | None = None) -> list[dict[str, Any]]:
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(query), params or {}).mappings().all()
            return [dict(r) for r in rows]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database read error: {str(e)}")


def execute_query(query: str, params: dict | None = None):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            conn.commit()
            return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database write error: {str(e)}")


# =========================
# Health Check
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }


# =========================
# Employees
# =========================

@app.get("/employees", tags=["Employees"])
def get_employees():
    data = fetch_rows(
        "SELECT id, full_name, role, department, active FROM employees ORDER BY id"
    )
    return {"module": "employees", "count": len(data), "items": data}


@app.post("/employees", status_code=201, tags=["Employees"])
def create_employee(employee: EmployeeCreate):
    query = """
    INSERT INTO employees (full_name, role, department, active)
    VALUES (:full_name, :role, :department, :active)
    RETURNING id, full_name, role, department, active
    """
    result = execute_query(query, employee.dict())
    row = result.mappings().first()
    return {"message": "Employee created", "data": dict(row)}


@app.put("/employees/{employee_id}", tags=["Employees"])
def update_employee(employee_id: int, employee: EmployeeUpdate):
    update_data = employee.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    set_clause = ", ".join([f"{k} = :{k}" for k in update_data])
    update_data["id"] = employee_id

    query = f"""
    UPDATE employees
    SET {set_clause}
    WHERE id = :id
    RETURNING id, full_name, role, department, active
    """

    result = execute_query(query, update_data)
    row = result.mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee updated", "data": dict(row)}


@app.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: int):
    query = "DELETE FROM employees WHERE id = :id"
    execute_query(query, {"id": employee_id})
    return {"message": f"Employee {employee_id} deleted"}


# =========================
# Inventory
# =========================

@app.get("/inventory", tags=["Inventory"])
def get_inventory():
    data = fetch_rows(
        "SELECT id, sku, item_name, quantity, unit_cost FROM inventory ORDER BY id"
    )
    return {"module": "inventory", "count": len(data), "items": data}


@app.post("/inventory", status_code=201, tags=["Inventory"])
def create_inventory(item: InventoryCreate):
    query = """
    INSERT INTO inventory (sku, item_name, quantity, unit_cost)
    VALUES (:sku, :item_name, :quantity, :unit_cost)
    RETURNING id, sku, item_name, quantity, unit_cost
    """
    result = execute_query(query, item.dict())
    row = result.mappings().first()
    return {"message": "Inventory item created", "data": dict(row)}


@app.put("/inventory/{item_id}", tags=["Inventory"])
def update_inventory(item_id: int, item: InventoryUpdate):
    update_data = item.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    set_clause = ", ".join([f"{k} = :{k}" for k in update_data])
    update_data["id"] = item_id

    query = f"""
    UPDATE inventory
    SET {set_clause}
    WHERE id = :id
    RETURNING id, sku, item_name, quantity, unit_cost
    """

    result = execute_query(query, update_data)
    row = result.mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    return {"message": "Inventory item updated", "data": dict(row)}


@app.delete("/inventory/{item_id}", tags=["Inventory"])
def delete_inventory(item_id: int):
    query = "DELETE FROM inventory WHERE id = :id"
    execute_query(query, {"id": item_id})
    return {"message": f"Inventory item {item_id} deleted"}


# =========================
# Orders
# =========================

@app.get("/orders", tags=["Orders"])
def get_orders():
    data = fetch_rows(
        "SELECT id, order_number, customer_name, total_amount, status FROM orders ORDER BY id"
    )
    return {"module": "orders", "count": len(data), "items": data}


@app.post("/orders", status_code=201, tags=["Orders"])
def create_order(order: OrderCreate):
    query = """
    INSERT INTO orders (order_number, customer_name, total_amount, status)
    VALUES (:order_number, :customer_name, :total_amount, :status)
    RETURNING id, order_number, customer_name, total_amount, status
    """
    result = execute_query(query, order.dict())
    row = result.mappings().first()
    return {"message": "Order created", "data": dict(row)}


@app.put("/orders/{order_id}", tags=["Orders"])
def update_order(order_id: int, order: OrderUpdate):
    update_data = order.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    set_clause = ", ".join([f"{k} = :{k}" for k in update_data])
    update_data["id"] = order_id

    query = f"""
    UPDATE orders
    SET {set_clause}
    WHERE id = :id
    RETURNING id, order_number, customer_name, total_amount, status
    """

    result = execute_query(query, update_data)
    row = result.mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order updated", "data": dict(row)}


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: int):
    query = "DELETE FROM orders WHERE id = :id"
    execute_query(query, {"id": order_id})
    return {"message": f"Order {order_id} deleted"}


# =========================
# Reports
# =========================

@app.get("/reports", tags=["Reports"])
def reports():
    data = fetch_rows(
        """
        SELECT 'open_orders' AS metric, COUNT(*)::int AS value FROM orders WHERE status <> 'DELIVERED'
        UNION ALL
        SELECT 'active_employees', COUNT(*)::int FROM employees WHERE active = TRUE
        UNION ALL
        SELECT 'inventory_skus', COUNT(*)::int FROM inventory
        """
    )
    return {
        "module": "reports",
        "generated_at": datetime.utcnow().isoformat(),
        "items": data,
    }


