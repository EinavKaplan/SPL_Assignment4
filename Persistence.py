# file: persistence.py

import sqlite3
import atexit
import os


# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand


class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Coffee_stand(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Activity(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


class ReportActivities(object):
    def __init__(self, date, item_description, quantity, seller_name, supplier_name):
        self.date = date
        self.item_description = item_description
        self.quantity = quantity
        self.seller_name = seller_name
        self.supplier_name = supplier_name


class ReportEmployees(object):
    def __init__(self, name, salary, working_location, total_sales_income):
        self.name = name
        self.salary = salary
        self.working_location = working_location
        self.total_sales_income = total_sales_income


# Data Access Objects:
# All of these are meant to be singletons
class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO Employees (id, name, salary, coffee_stand) VALUES (?, ?, ?, ?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def find(self, employee_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, salary, coffee_stand FROM Employees WHERE id = ?
        """, [employee_id])
        out = c.fetchone()
        if out is not None:
            return Employee(*out)
        else:
            return None

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                  SELECT id, name, salary, coffee_stand FROM Employees
              """).fetchall()

        return [Employee(*row) for row in all]


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO Suppliers (id, name, contact_information) VALUES (?, ?, ?)
        """, [supplier.id, supplier.name, supplier.contact_information])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
                SELECT id, name, contact_information FROM Suppliers WHERE id = ?
            """, [supplier_id])
        out = c.fetchone()
        if out is not None:
            return Supplier(*out)
        else:
            return None

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                  SELECT id, name, contact_information FROM Suppliers
              """).fetchall()

        return [Supplier(*row) for row in all]


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
            INSERT INTO Products (id, description, price, quantity) VALUES (?, ?, ?, ?)
        """, [product.id, product.description, product.price, product.quantity])

    def find(self, product_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, description, price, quantity FROM Products WHERE id = ?
        """, [product_id])

        return Product(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                  SELECT id, description, price, quantity FROM Products
              """).fetchall()

        return [Product(*row) for row in all]

    def update_quantity(self, product):
        self._conn.execute("""
            UPDATE Products SET quantity = ? WHERE id = ?
        """, (product.quantity, product.id))


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
               INSERT INTO Coffee_stands(id, location, number_of_employees) VALUES (?, ?, ?)
           """, (coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees))

    def find(self, coffee_stand_id):
        c = self._conn.cursor()
        c.execute("""
               SELECT id, location, number_of_employees FROM Coffee_stands WHERE id = ?
           """, [coffee_stand_id])

        return Coffee_stand(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                  SELECT id, location, number_of_employees FROM Coffee_stands
              """).fetchall()

        return [Coffee_stand(*row) for row in all]


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
               INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
           """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
               SELECT product_id, quantity, activator_id, date FROM Activities ORDER BY date
           """).fetchall()

        return [Activity(*row) for row in all]


class _ReportActivities:
    def __init__(self, conn):
        self._conn = conn

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
        SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name
         FROM ((Activities JOIN Products on Activities.product_id = Products.id) 
         LEFT JOIN Employees on Activities.activator_id = Employees.id) 
         LEFT JOIN Suppliers on Activities.activator_id = Suppliers.id
         ORDER BY Activities.date
         """).fetchall()

        return [ReportActivities(*row) for row in all]


class _ReportEmployees:
    def __init__(self, conn):
        self._conn = conn

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
        SELECT Employees.name, Employees.salary, Coffee_stands.location, sum((-Activities.quantity) * Products.price)
        FROM ((Employees JOIN Coffee_stands on Employees.coffee_stand = Coffee_stands.id) LEFT JOIN Activities 
        on Employees.id = Activities.activator_id) LEFT JOIN Products on Activities.product_id = Products.id
        GROUP BY Employees.id
        ORDER BY Employees.name
        """).fetchall()

        return [ReportEmployees(*row) for row in all]


# The Repository
class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('moncafe.db')
        self.employees = _Employees(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.products = _Products(self._conn)
        self.coffee_stands = _Coffee_stands(self._conn)
        self.activities = _Activities(self._conn)
        self.report_activities = _ReportActivities(self._conn)
        self.report_employees = _ReportEmployees(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        if os.path.isfile("moncafe.db"):
            self.close()
            os.remove("moncafe.db")
            self.__init__()
        self._conn.executescript("""
                CREATE TABLE Employees (
                    id  INTEGER PRIMARY KEY,
                    name    TEXT    NOT NULL,
                    salary  REAL    NOT NULL,
                    coffee_stand    INTEGER REFERENCES Coffee_stands(id)
                );

                CREATE TABLE Suppliers (
                    id  INTEGER PRIMARY KEY,
                    name    TEXT    NOT NULL,
                    contact_information TEXT
                );
                
                CREATE TABLE Products (
                    id  INTEGER PRIMARY KEY,
                    description    TEXT    NOT NULL,
                    price   REAL    NOT NULL,
                    quantity    INTEGER NOT NULL
                );
                
                CREATE TABLE Coffee_stands (
                    id  INTEGER PRIMARY KEY,
                    location    TEXT    NOT NULL,
                    number_of_employees INTEGER
                );
                
                CREATE TABLE Activities (
                    product_id  INTEGER REFERENCES Products(id),
                    quantity    INTEGER NOT NULL,
                    activator_id    INTEGER NOT NULL,
                    date    DATE    NOT NULL
                );
            """)


# the repository singleton
repo = _Repository()
atexit.register(repo.close)
