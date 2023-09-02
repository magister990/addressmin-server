from ariadne import ObjectType

from .customer import resolve_create_customer, resolve_update_customer, resolve_delete_customer
from .supernet import resolve_create_supernet, resolve_update_supernet, resolve_delete_supernet
from .subnet import resolve_create_subnet, resolve_update_subnet, resolve_delete_subnet
from .assignment import resolve_create_assignment, resolve_update_assignment, resolve_delete_assignment

mutation = ObjectType("Mutation")

mutation.set_field("createCustomer", resolve_create_customer)
mutation.set_field("updateCustomer", resolve_update_customer)
mutation.set_field("deleteCustomer", resolve_delete_customer)

mutation.set_field("createSupernet", resolve_create_supernet)
mutation.set_field("updateSupernet", resolve_update_supernet)
mutation.set_field("deleteSupernet", resolve_delete_supernet)

mutation.set_field("createSubnet", resolve_create_subnet)
mutation.set_field("updateSubnet", resolve_update_subnet)
mutation.set_field("deleteSubnet", resolve_delete_subnet)

mutation.set_field("createAssignment", resolve_create_assignment)
mutation.set_field("updateAssignment", resolve_update_assignment)
mutation.set_field("deleteAssignment", resolve_delete_assignment)
