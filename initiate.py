# file: initiate.py
from Persistence import *
import sys

repo.create_tables()
config_file = sys.argv
with open(config_file):
    for rec in config_file:
        if rec[0] == 'E':
            repo.employees.insert(Employee(*rec[1:]))
        elif rec[0] == 'S':
            repo.suppliers.insert(Supplier(*rec[1:]))
        elif rec[0] == 'P':
            repo.products.insert(Product(*rec[1:], 0))
        elif rec[0] == 'C':
            repo.coffee_stands.insert(Coffee_stand(*rec[1:]))
