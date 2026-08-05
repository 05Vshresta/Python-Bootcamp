import sqlite3

# ================== Database Connection ==================
conn = sqlite3.connect("employee_management.db")
cursor = conn.cursor()

print("Database connection established successfully!")

# ================== Create Employee Table ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    mobile TEXT,
    email TEXT,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    status INTEGER DEFAULT 0
)
""")

conn.commit()
print("Employee Table created successfully!")

# ================== Employee Class ==================
class Employee:
    def __init__(self, name, mobile, email, department, salary):
        self.name = name
        self.mobile = mobile
        self.email = email
        self.department = department
        self.salary = salary

    # ================== Employee Registration ==================
    def register(self):
        cursor.execute("""
        INSERT INTO employees(name, mobile, email, department, salary)
        VALUES (?, ?, ?, ?, ?)
        """, (
            self.name,
            self.mobile,
            self.email,
            self.department,
            self.salary
        ))

        conn.commit()
        print(f"\nEmployee '{self.name}' registered successfully!")

    # ================== Display Employees ==================
    @staticmethod
    def display_employees():
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        if not employees:
            print("\nNo employees found.")
        else:
            print("\n============== Employee List ==============")

            for employee in employees:
                print(f"""
Employee ID : {employee[0]}
Name        : {employee[1]}
Mobile      : {employee[2]}
Email       : {employee[3]}
Department  : {employee[4]}
Salary      : ₹{employee[5]:,.2f}
Status      : {employee[6]}
--------------------------------------------
""")

#=================== search by id ===================
@staticmethod
def search_by_id():
    employee_id = int(input("Enter the Employee Id :"))
    cursor.execute("""
    SELECT* FROM employees
    WHERE employee_id = ?""",(employee_id,))
    employee = cursor.fetchone()
    if employee == 0:
        print("No employee data is found")
    else:
        print("=========Employee Details=========")
        print(f"""
        Employee ID : {employee[0]}
        Name : {employee[1]}
        Mobile : {employee[2]}
        Email : {employee[3]}
        Department : {employee[4]}
        Salary : ₹{employee[5]:,.2f}
        Status : {employee[6]}
        """)
    print("Employee is not found")
    

# ================== Main Menu ==================
while True:
    print("""
================== Employee Management System ==================
1. Register Employee
2. Display Employees
3. Search Employee by ID
4. Exit
""")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("\n============== Employee Registration ==============")

        name = input("Enter employee name: ")
        mobile = input("Enter employee mobile: ")
        email = input("Enter employee email: ")
        department = input("Enter employee department: ")

        try:
            salary = float(input("Enter employee salary: "))
        except ValueError:
            print("Invalid salary! Please enter a numeric value.")
            continue

        employee = Employee(name, mobile, email, department, salary)
        employee.register()

    elif choice == '2':
        Employee.display_employees()

    elif choice == '3':
        Employee.search_by_id()

    elif choice == '4':
        print("Thank you for using Employee Management System.")
        conn.close()
        break

    else:
        print("Invalid choice! Please try again.")