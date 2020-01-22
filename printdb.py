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
    reports = repo.report_employees.find_all()
    for r in reports:
        if r.total_sales_income is not None:
            print(r.name + " " + str(r.salary) + " " + r.working_location + " " + str(r.total_sales_income))
        else:
            print(r.name + " " + str(r.salary) + " " + r.working_location + " 0")


def print_activities_report():
    reports = repo.report_activities.find_all()
    if reports:
        print('Activities')
    for r in reports:
        if r.seller_name is not None:
            print("(" + str(r.date) + ", '" + r.item_description + "', " + str(r.quantity) + ", '" + r.seller_name
                  + "', None)")
        else:
            print("(" + str(r.date) + ", '" + r.item_description + "', " + str(r.quantity) + ", None, '"
                  + r.supplier_name + "')")


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
