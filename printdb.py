# file: printdb
from Persistence import *


# print activities by date
def print_activities():
    print('Activities')
    activities = repo.activities.find_all()
    for row in activities:
        print(row)


# print Coffee_stand by id
def print_coffee_stands():
    print('Coffee stands')
    coffee_stands = repo.coffee_stands.find_all()
    for row in coffee_stands:
        print(row)


# print Employees by id
def print_employees():
    print('Employees')
    employees = repo.employees.find_all()
    for row in employees:
        print(row)


# print Products by id
def print_products():
    print('Products')
    products = repo.products.find_all()
    for row in products:
        print(row)


# print Suppliers by id
def print_suppliers():
    print('Suppliers')
    suppliers = repo.suppliers.find_all()
    for row in suppliers:
        print(row)


def print_employee_report():
    print('Employees report')
    # Name, Salary, Working location, total sales income.
    employees = repo.employees.find_all()
    for row in employees:
        coffee_stand = repo.coffee_stands.find(row[3])
        sales_income = find_sales_income(row[0])
        print(row[1]+" "+row[2]+" "+coffee_stand[1]+" "+sales_income)


def find_sales_income(employee_id):
    activities = repo.activities.find_all()
    total = 0
    for row in activities:
        # row[0]=product_id row[1]=quantity row[2] = activator id
        if row[2] == employee_id:
            product = repo.products.find(row[0])
            # product[2] = product price
            total = total + (-row[1])*product[2]
    return total


def print_activities_report():
    activities = repo.activities.find_all()
    if len(activities) > 0:
        for row in activities:
            product = repo.products.find(row[0])
            # date of activity, item description, quantity, name of seller and the name of the supplier
            employee = repo.employees.find(row[2])
            supplier = repo.suppliers.find(row[2])
            if len(employee) > 0:
                print(row[3]+", "+product[1]+", "+row[1]+", "+employee[1]+", None")
            else:
                print(row[3]+", "+product[1]+", "+row[1]+", None, "+supplier[1])


def print_all():
    print_activities()
    print_coffee_stands()
    print_employees()
    print_products()
    print_suppliers()
    print_employee_report()
    print_activities_report()


print_all()
