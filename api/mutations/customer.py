from sqlalchemy import select, delete
from sqlalchemy.orm.exc import NoResultFound
from db import session
from db.models import Customer

from .errors import NotFoundError, AlreadyInUseError

def is_name_in_use(name: str) -> bool:
    try:
        customer = session.execute(
            select(Customer).where(Customer.name == name)
        ).scalar_one()
    except NoResultFound:
        return False
    raise AlreadyInUseError(f"the name '{name}' is already in use")

def resolve_create_customer(obj, info, name):
    try:
        # First check to see if the name is already in use
        is_name_in_use(name)
        # Create the new customer and save.
        customer = Customer(name = name)
        session.add(customer)
        session.commit()
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

def resolve_update_customer(obj, info, id, name):
    try:
        # First lookup the customer
        customer = session.execute(
            select(Customer).where(Customer.id == id)
        ).scalar_one()
        # Second check if name is already in use
        is_name_in_use(name)
        # Update the customer and save.
        customer.name = name
        session.add(customer)
        session.commit()
        payload = {
            "success": True,
            "result": customer
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The customer id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload

def resolve_delete_customer(obj, info, id):
    try:
        # First lookup the customer
        customer = session.execute(
            select(Customer).where(Customer.id == id)
        ).scalar_one()
        # Delete the customer
        session.execute(
            delete(Customer).where(Customer.id == customer.id)
        )
        session.commit()
        payload = {
            "success": True
        }
    except Exception as error:
        if (error.__class__.__name__ == 'NoResultFound'):
            error = f"The customer id '{id}' was not found"
        payload = {
            "success": False,
            "error": str(error)
        }
    return payload
