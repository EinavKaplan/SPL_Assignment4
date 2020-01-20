# file: initiate.py
from Persistence import *
import sys


repo.create_tables()
args = sys.argv
config_file = args[1]
with open(config_file) as data:
    for rec in data:
        row = rec.split(', ')
        row[len(row)-1] = row[len(row)-1].replace("\n", "")
        if row[0] == 'E':
            repo.employees.insert(Employee(row[1], row[2], row[3], row[4]))
        elif row[0] == 'S':
            repo.suppliers.insert(Supplier(row[1], row[2], row[3]))
        elif row[0] == 'P':
            repo.products.insert(Product(row[1], row[2], row[3],0))
        elif row[0] == 'C':
            repo.coffee_stands.insert(Coffee_stand(row[1], row[2], row[3]))
