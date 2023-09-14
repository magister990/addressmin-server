from sqlalchemy import select, delete
from sqlalchemy.orm.exc import NoResultFound
from db import session
from db.models import Supernet

from .errors import NotFoundError, AlreadyInUseError

# TODO This one need much more logic around smaller and larger networks
# overlaping. For now were only doing exact match.

def resolve_create_supernet(obj, info, network, mask, customer_id):
    try:
        # Create the new supernet and save.
        supernet = Supernet(mask = mask, network = network, customer_id = customer_id)
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
        # Update the supernet and save.
        supernet.customer_id = customer_id
        session.validate_object(supernet)
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
