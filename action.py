# file: action.py
from Persistence import *
import printdb
import sys

args = sys.argv
config_file = args[1]
with open(config_file) as data:
    for rec in data:
        rec = rec.split(', ')
        rec[len(rec) - 1] = rec[len(rec) - 1].replace("\n", "")
        if int(rec[1]) > 0:
            repo.activities.insert(Activity(rec[0], rec[1], rec[2], rec[3]))
            product = repo.products.find(rec[0])
            product.quantity += int(rec[1])
            repo.products.update_quantity(Product(product.id, product.description, product.price, product.quantity))

        elif int(rec[1]) < 0:
            product = repo.products.find(rec[0])
            quantity = product.quantity + int(rec[1])
            if quantity >= 0:
                repo.activities.insert(Activity(rec[0], rec[1], rec[2], rec[3]))
                repo.products.update_quantity(Product(product.id, product.description, product.price, quantity))
    printdb.print_all()
