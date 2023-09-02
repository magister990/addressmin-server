from sqlalchemy import select
from db import session
from db.models import Customer

def resolve_customers(obj, info):
    try:
        customers = session.execute(
            select(Customer)
        ).scalars().all()
        payload = {
            "success": True,
            "list": customers
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_customer(obj, info, id):
    try:
        customer = session.execute(
            select(Customer).where(Customer.id == id)
        ).scalar_one()
        payload = {
            "success": True,
            "result": customer
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_customers_by_name(obj, info, name):
    try:
        customers = session.execute(
            select(Customer).where(Customer.name.contains(name))
        ).scalars().all()
        if (customers):
            payload = {
                "success": True,
                "list": customers
            }
        else:
            payload = {
                "success": False,
                "error": f"No matching customers with the name '{name}'"
            }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
