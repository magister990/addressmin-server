from sqlalchemy import select
from db import session
from db.models import Assignment

def resolve_assignments(obj, info):
    try:
        assignments = session.execute(
            select(Assignment)
        ).scalars().all()
        payload = {
            "success": True,
            "list": assignments
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_assignment(obj, info, id):
    try:
        assignment = session.execute(
            select(Assignment).where(Assignment.id == id)
        ).scalar_one()
        payload = {
            "success": True,
            "result": assignment
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_assignments_by_address(obj, info, address):
    try:
        assignments = session.execute(
            select(Assignment).where(Assignment.address.contains(address))
        ).scalars().all()
        if (assignments):
            payload = {
                "success": True,
                "list": assignments
            }
        else:
            payload = {
                "success": False,
                "error": f"No matching assignments with the address '{address}'"
            }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
