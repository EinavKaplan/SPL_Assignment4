# file: printdb
from Persistence import *


# print activities by date
def print_activities():
    print('Activities')
    activities = repo.activities.find_all()
    for a in activities:
        print("("+str(a.product_id)+", "+str(a.quantity)+", "+str(a.activator_id)+", "+str(a.date)+")")


# print Coffee_stand by id
def print_coffee_stands():
    print('Coffee stands')
    coffee_stands = repo.coffee_stands.find_all()
    for coffee in coffee_stands:
        print("("+str(coffee.id)+", '"+coffee.location+"', "+str(coffee.number_of_employees)+")")


# print Employees by id
def print_employees():
    print('Employees')
    employees = repo.employees.find_all()
    for e in employees:
        print("("+str(e.id)+", '"+e.name+"', "+str(e.salary)+", "+str(e.coffee_stand)+")")


# print Products by id
def print_products():
    print('Products')
    products = repo.products.find_all()
    for p in products:
        print("("+str(p.id)+", '"+p.description+"', "+str(p.price)+", "+str(p.quantity)+")")


# print Suppliers by id
def print_suppliers():
    print('Suppliers')
    suppliers = repo.suppliers.find_all()
    for s in suppliers:
        print("("+str(s.id)+", '"+s.name+"', '"+s.contact_information+"')")


def print_employee_report():
    print('Employees report')
    # Name, Salary, Working location, total sales income.
    employees = repo.employees.find_all()
    for e in employees:
        coffee_stand = repo.coffee_stands.find(e.coffee_stand)
        sales_income = find_sales_income(e.id)
        print(e.name+" "+str(e.salary)+" "+coffee_stand.location+" "+str(sales_income))


def find_sales_income(employee_id):
    activities = repo.activities.find_all()
    total = 0
    for a in activities:
        if a.activator_id == employee_id:
            product = repo.products.find(a.product_id)
            total = total + (-a.quantity)*product.price
    return total


def print_activities_report():
    activities = repo.activities.find_all()
    if len(activities) > 0:
        print('Activities')
        for a in activities:
            product = repo.products.find(a.product_id)
            employee = repo.employees.find(a.activator_id)
            supplier = repo.suppliers.find(a.activator_id)
            if employee is not None:
                print("("+str(a.date)+", '"+product.description+"', "+str(a.quantity)+", '"+employee.name+"', None)")
            else:
                print("("+str(a.date)+", '"+product.description+"', "+str(a.quantity)+", None, '"+supplier.name+"')")


def print_all():
    print_activities()
    print_coffee_stands()
    print_employees()
    print_products()
    print_suppliers()
    print('')
    print_employee_report()
    print('')
    print_activities_report()


if __name__ == '__main__':
    print_all()
