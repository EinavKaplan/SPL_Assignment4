# file: action.py
from Persistence import *
import sys

config_file = sys.argv
with open(config_file):
    for rec in config_file:
        if rec[1] > 0:
            repo.activities.insert(Activity(*rec))
            product = repo.products.find(rec[0])
            product.quantity += rec[1]
            repo.products.update_quantity(Product(product.id, product.description, product.price, product.quantity))
        elif rec[1] < 0:
            product = repo.products.find(rec[0])
            quantity = product.quantity + rec[1]
            if quantity > 0:
                repo.activities.insert(Activity(*rec))
                repo.products.update_quantity(Product(product.id, product.description, product.price, quantity))
