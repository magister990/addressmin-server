from sqlalchemy import select, delete
from sqlalchemy.orm.exc import NoResultFound
from db import session
from db.models import Subnet

from .errors import NotFoundError, AlreadyInUseError

# TODO This one need much more logic around smaller and larger networks
# overlaping. For now were only doing exact match.
# TODO include validation that checks if the subnet is actually part of the supernet

def resolve_create_subnet(
    obj,
    info,
    network,
    mask,
    customer_id,
    supernet_id,
    advertised_from,
    reserve_network_and_broadcast = True):
    try:
        # Create the new subnet and save.
        subnet = Subnet(
            mask = mask,
            network = network,
            customer_id = customer_id,
            supernet_id = supernet_id,
            advertised_from = advertised_from,
            reserve_network_and_broadcast = reserve_network_and_broadcast)
        session.add(subnet)
        session.commit()
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

def resolve_update_subnet(obj, info, id, customer_id, advertised_from, reserve_network_and_broadcast = None):
    try:
        # First lookup the subnet
        subnet = session.execute(
            select(Subnet).where(Subnet.id == id)
        ).scalar_one()
        # Update the subnet and save.
        subnet.customer_id = customer_id
        subnet.advertised_from = advertised_from
        if reserve_network_and_broadcast:
            subnet.reserve_network_and_broadcast = reserve_network_and_broadcast
        session.validate_object(subnet)
        session.add(subnet)
        session.commit()
        payload = {
            "success": True,
            "result": subnet
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The subnet id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_delete_subnet(obj, info, id):
    try:
        # First lookup the subnet
        subnet = session.execute(
            select(Subnet).where(Subnet.id == id)
        ).scalar_one()
        # Delete the subnet
        session.execute(
            delete(Subnet).where(Subnet.id == subnet.id)
        )
        session.commit()
        payload = {
            "success": True
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The subnet id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
