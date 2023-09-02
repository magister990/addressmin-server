from sqlalchemy import select
from db import session
from db.models import Subnet

def resolve_subnets(obj, info):
    try:
        subnets = session.execute(
            select(Subnet)
        ).scalars().all()
        payload = {
            "success": True,
            "list": subnets
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_subnet(obj, info, id):
    try:
        subnet = session.execute(
            select(Subnet).where(Subnet.id == id)
        ).scalar_one()
        payload = {
            "success": True,
            "result": subnet
        }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_subnets_by_network(obj, info, network):
    try:
        subnets = session.execute(
            select(Subnet).where(Subnet.network.contains(network))
        ).scalars().all()
        if (subnets):
            payload = {
                "success": True,
                "list": subnets
            }
        else:
            payload = {
                "success": False,
                "error": f"No matching subnets with the network '{network}'"
            }
    except Exception as error:
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
