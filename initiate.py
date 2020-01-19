# file: initiate
from persistence import *
import sqlite3
import os
import sys

repo = _Repository()
####
database_existed = os.path.isfile('moncafe.db')
if (database_existed) :
    os.remove('moncafe.db')

db_connection = sqlite3.connect('moncafe.db')
with db_connection :
    #####
    config_file = sys.argv
    with open(config_file):
        for rec in config_file:
            if rec[0] == 'E':
                repo.employees.insert(Employee(*rec[1:]))
            elif rec[0] == 'S':
                repo.suppliers.insert(Supplier(*rec[1:]))
            elif rec[0] == 'P':
                repo.products.insert(Product(*rec[1:]))
            elif rec[0] == 'C':
                repo.coffee_stands.insert(Coffee_stand(*rec[1:]))
