from ariadne import ObjectType
from .customer import resolve_customers, resolve_customer, resolve_customers_by_name
from .supernet import resolve_supernets, resolve_supernet, resolve_supernets_by_network
from .subnet import resolve_subnets, resolve_subnet, resolve_subnets_by_network
from .assignment import resolve_assignments, resolve_assignment, resolve_assignments_by_address

query = ObjectType("Query")

query.set_field("customers", resolve_customers)
query.set_field("customer", resolve_customer)
query.set_field("customersByName", resolve_customers_by_name)

query.set_field("supernets", resolve_supernets)
query.set_field("supernet", resolve_supernet)
query.set_field("supernetsByNetwork", resolve_supernets_by_network)

query.set_field("subnets", resolve_subnets)
query.set_field("subnet", resolve_subnet)
query.set_field("subnetsByNetwork", resolve_subnets_by_network)

query.set_field("assignments", resolve_assignments)
query.set_field("assignment", resolve_assignment)
query.set_field("assignmentsByAddress", resolve_assignments_by_address)
