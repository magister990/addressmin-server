from sqlalchemy import select, delete
from sqlalchemy.orm.exc import NoResultFound
from db import session
from db.models import Subnet

from .errors import NotFoundError, AlreadyInUseError

# TODO This one need much more logic around smaller and larger networks
# overlaping. For now were only doing exact match.
def is_network_in_use(network: str) -> bool:
    try:
        subnet = session.execute(
            select(Subnet).where(Subnet.network == network)
        ).scalar_one()
    except NoResultFound:
        return False
    raise NetworkInUseError(f"the network '{network}' is already in use")

# TODO include validation that the customer exists
# TODO include validation that the supernet exists
# TODO include validation that checks if the subnet is actually part of the supernet

def resolve_create_subnet(obj, info, network, mask, supernet_id):
    try:
        # First check to see if the name is already in use
        is_network_in_use(name)
        # Create the new subnet and save.
        subnet = Subnet(network = network, mask = mask, supernet_id = supernet_id)
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

def resolve_update_subnet(obj, info, id, network, mask, subnet_id, customer_id):
    try:
        # First lookup the subnet
        subnet = session.execute(
            select(Subnet).where(Subnet.id == id)
        ).scalar_one()
        # Second check if name is already in use
        is_network_in_use(name)
        # Update the subnet and save.
        subnet.network = network
        subnet.mask = mask
        subnet.supernet_id = supernet_id
        subnet.customer_id = customer_id
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
