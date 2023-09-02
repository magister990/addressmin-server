from sqlalchemy import select, delete
from sqlalchemy.orm.exc import NoResultFound
from db import session
from db.models import Supernet

from .errors import NotFoundError, AlreadyInUseError

# TODO This one need much more logic around smaller and larger networks
# overlaping. For now were only doing exact match.
def is_network_in_use(network: str) -> bool:
    try:
        supernet = session.execute(
            select(Supernet).where(Supernet.network == network)
        ).scalar_one()
    except NoResultFound:
        return False
    raise NetworkInUseError(f"the network '{network}' is already in use")

# TODO include validation that the customer exists

def resolve_create_supernet(obj, info, network, mask, customer_id):
    try:
        # First check to see if the name is already in use
        is_network_in_use(name)
        # Create the new supernet and save.
        supernet = Supernet(network = network, mask = mask, customer_id = customer_id)
        session.add(supernet)
        session.commit()
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

def resolve_update_supernet(obj, info, id, network, mask, customer_id):
    try:
        # First lookup the supernet
        supernet = session.execute(
            select(Supernet).where(Supernet.id == id)
        ).scalar_one()
        # Second check if network is already in use
        is_network_in_use(network)
        # Update the supernet and save.
        supernet.network = network
        supernet.mask = mask
        supernet.customer_id = supernet.customer_id
        session.add(supernet)
        session.commit()
        payload = {
            "success": True,
            "result": supernet
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The supernet id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_delete_supernet(obj, info, id):
    try:
        # First lookup the supernet
        supernet = session.execute(
            select(Supernet).where(Supernet.id == id)
        ).scalar_one()
        # Delete the supernet
        session.execute(
            delete(Supernet).where(Supernet.id == supernet.id)
        )
        session.commit()
        payload = {
            "success": True
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The supernet id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
