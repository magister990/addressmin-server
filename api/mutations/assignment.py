from sqlalchemy import select, delete
from sqlalchemy.orm.exc import NoResultFound
from db import session
from db.models import Assignment

from .errors import NotFoundError, AlreadyInUseError

def is_address_in_use(network: str) -> bool:
    try:
        assignment = session.execute(
            select(Assignment).where(Assignment.address == address)
        ).scalar_one()
    except NoResultFound:
        return False
    raise NetworkInUseError(f"the address '{address}' is already in use")

# TODO include validation that the subnet exists

def resolve_create_assignment(obj, info, address, hostname, subnet_id):
    try:
        # First check to see if the name is already in use
        is_address_in_use(name)
        # Create the new assignment and save.
        assignment = Assignment(address = address, hostname = hostname, subnet_id = subnet_id)
        session.add(assignment)
        session.commit()
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

def resolve_update_assignment(obj, info, id, address, hostname, subnet_id):
    try:
        # First lookup the assignment
        assignment = session.execute(
            select(Assignment).where(Assignment.id == id)
        ).scalar_one()
        # Second check if name is already in use
        is_address_in_use(name)
        # Update the assignment and save.
        assignment.address = address
        assignment.hostname = hostname
        assignment.subnet_id = subnet_id
        session.add(assignment)
        session.commit()
        payload = {
            "success": True,
            "result": assignment
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The assignment id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_delete_assignment(obj, info, id):
    try:
        # First lookup the assignment
        assignment = session.execute(
            select(Assignment).where(Assignment.id == id)
        ).scalar_one()
        # Delete the assignment
        session.execute(
            delete(Assignment).where(Assignment.id == assignment.id)
        )
        session.commit()
        payload = {
            "success": True
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The assignment id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
