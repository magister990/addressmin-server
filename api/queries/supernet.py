from sqlalchemy import select
from db import session
from db.models import Supernet

def resolve_supernets(obj, info):
    try:
        supernets = session.execute(
            select(Supernet)
        ).scalars().all()
        payload = {
            "success": True,
            "list": supernets
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_supernet(obj, info, id):
    try:
        supernet = session.execute(
            select(Supernet).where(Supernet.id == id)
        ).scalar_one()
        payload = {
            "success": True,
            "result": supernet
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_supernets_by_network(obj, info, network):
    try:
        supernets = session.execute(
            select(Supernet).where(Supernet.network.contains(network))
        ).scalars().all()
        if (supernets):
            payload = {
                "success": True,
                "list": supernets
            }
        else:
            payload = {
                "success": False,
                "error": f"No matching supernets with the network '{network}'"
            }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
