import sqlite3

# ================== Database Connection ==================
conn = sqlite3.connect("employee_management.db")
cursor = conn.cursor()

print("Database connection established successfully!")

# ================== Create Employee Table ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    mobile TEXT,
    email TEXT,
    department TEXT,
    salary REAL,
    status INTEGER DEFAULT 0 )
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
        print(f"\n '{self.name}' is an employee registered successfully!")

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
                    Salary      : {employee[5]}
                    Status      : {employee[6]}
                    --------------------------------------------
                """)

#================Employee search by id=====================

    @staticmethod
    def search_employee_by_id(employee_id):
        cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
        employee = cursor.fetchone()

        if employee:
            print("============================= Employee Details ============================")
            print(f"""
            Employee ID : {employee[0]}
            Name        : {employee[1]}
            Mobile      : {employee[2]}
            Email       : {employee[3]}
            Department  : {employee[4]}
            Salary      : {employee[5]}
            Status      : {employee[6]}
            --------------------------------------------
            """)
            print("Employee found successfully!")
        else:
            print(f"\nEmployee with ID {employee_id} not found.")

    #=====================Employee search by name=========================
    @staticmethod
    def search_by_name():
        name = input("Enter employee name to search: ")

        cursor.execute("""SELECT * FROM employees WHERE name LIKE ?""",("%" + name + "%",))
        employees = cursor.fetchall()

        if employees:
            print("============================= Employee Details ============================")
            for employee in employees:
                print(f"""
                Employee ID : {employee[0]}
                Name        : {employee[1]}
                Mobile      : {employee[2]}
                Email       : {employee[3]}
                Department  : {employee[4]}
                Salary      : {employee[5]}
                Status      : {employee[6]}
                --------------------------------------------
                """)
            print(f"Found {len(employees)} employee(s) with name '{name}'.")
        else:
            print(f"\nNo employees found with name '{name}'.")

    #=====================Employee search by department======================
    @staticmethod
    def search_department(department):
        cursor.execute("SELECT * FROM employees WHERE department = ?", (department,))
        employees = cursor.fetchall()

        if employees:
            print("============================= Employee Details ============================")
            for employee in employees:
                print(f"""
                Employee ID : {employee[0]}
                Name        : {employee[1]}
                Mobile      : {employee[2]}
                Email       : {employee[3]}
                Department  : {employee[4]}
                Salary      : {employee[5]}
                Status      : {employee[6]}
                --------------------------------------------
                """)
            print(f"Found {len(employees)} employee(s) in the '{department}' department.")
        else:
            print(f"\nNo employees found in the '{department}' department.")

    #==============================Update employee ========================
    @staticmethod
    def update_employee():
        employee_id = int(input("Enter employee id to update :"))
        cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
        employee = cursor.fetchone()

        if employee:
            print("=============================Current Employee Details ============================")
            print(f"""
            Employee ID : {employee[0]}
            Name        : {employee[1]}
            Mobile      : {employee[2]}
            Email       : {employee[3]}
            Department  : {employee[4]}
            Salary      : {employee[5]}
            Status      : {employee[6]}
            --------------------------------------------
            """)
            print("Employee found successfully!")
            print("============================= Update Employee Details ============================")
            name = input("Enter the name :")
            mobile = input("Enter the mobile no :")
            email = input("Enter the email :")
            department = input("Enter the department :")
            salary = float(input("Enter the salary :")) # Added missing salary input


            cursor.execute("""
                UPDATE employees

                SET
                name = ?,
                mobile = ?,
                email = ?,
                department = ?,
                salary = ?
                WHERE employee_id = ?
                """,(
                    name,
                    mobile,
                    email,
                    department,
                    salary,
                    employee_id
                ))
            conn.commit() # Commit the changes
            print(f"Employee with ID {employee_id} updated successfully!")

        else:
            print(f"\nEmployee with ID {employee_id} not found.")

#==================== Delete Employee =========================
    @staticmethod
    def delete_employee():

        employee_id = int(input("Enter employee id to delete :"))

        cursor.execute(
        """SELECT * FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
        employee = cursor.fetchone()

        if employee:
            print("=============================Current Employee Details ============================")
            print(f"""
            Employee ID : {employee[0]}
            Name        : {employee[1]}
            Mobile      : {employee[2]}
            Email       : {employee[3]}
            Department  : {employee[4]}
            Salary      : {employee[5]}
            Status      : {employee[6]}
            --------------------------------------------
            """)

            confirm = input("Are you sure you want to delete this employee? (yes/no): ").upper()
            if confirm == "YES":
                cursor.execute(
                    """DELETE FROM employees
                    WHERE employee_id = ?
                    """, (employee_id,))
                conn.commit()
                print(f"Employee with ID {employee_id} deleted successfully!")
            else:
                print(f"Employee with ID {employee_id} deletion cancelled")
        else:
            print(f"\nEmployee with ID {employee_id} not found.")

#======================== Mark Employee status ==========================================

def mark_employee_status():
    employee_id = int(input("Enter employee id to mark status :"))

    cursor.execute(
        """SELECT * FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
    employee = cursor.fetchone()

    if employee:
        print("=============================Current Employee Details ============================")
        print(f"""
        Employee ID : {employee[0]}
        Name        : {employee[1]}
        Mobile      : {employee[2]}
        Email       : {employee[3]}
        Department  : {employee[4]}
        Salary      : {employee[5]}
        Status      : {employee[6]}
        --------------------------------------------
        """)

        status = int(input("Enter the status (0 for inactive, 1 for active): "))

        cursor.execute(
            """UPDATE employees
            SET status = ?
            WHERE employee_id = ?
            """, (status, employee_id))
        conn.commit()
        print(f"Employee with ID {employee_id} status updated successfully!")
    else:
        print(f"\nEmployee with ID {employee_id} not found.")


#==================================== Employee status report ==========================================

def attendance_report():
    cursor.execute("""
    SELECT employee_id,
        name,
        department,
        status
    FROM employees""")

    employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found.")
    else:
        print("\n============== Employee Status Report ==============")

        for employee in employees:
            status = "Active" if employee[3] == 1 else "Inactive"
            print(f"""
            Employee ID : {employee[0]}
            Name        : {employee[1]}
            Department  : {employee[2]}
            Status      : {status}
            --------------------------------------------
            """)


# ================== Main Menu ==================
while True:
    print("""
================== Employee Management System ==================
1. Register Employee
2. Display Employees
3. Search Employee by ID
4. Search Employee by Name
5. Search Employee by Department
6. Update Employee
7. Delete Employee
8. Mark Employee Status
9. Employee Status Report   
10. Exit
""")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("\n============== Employee Registration ==============")

        name = input("Enter employee name: ")
        mobile = input("Enter employee mobile: ")
        email = input("Enter employee email: ")
        department = input("Enter employee department: ")
        salary = float(input("Enter employee salary: "))

        employee = Employee(name, mobile, email, department, salary)
        employee.register()

    elif choice == '2':
        Employee.display_employees()

    elif choice == '3':
        employee_id = int(input("Enter employee ID to search: "))
        Employee.search_employee_by_id(employee_id)

    elif choice == '4':
        Employee.search_by_name()

    elif choice == '5':
        department = input("Enter department to search: ")
        Employee.search_department(department) # Corrected method call

    elif choice == '6':
        Employee.update_employee()


    elif choice == '7':
        Employee.delete_employee()
        Employee.display_employees()  # Display updated employee list after deletion

    elif choice == '8':
        mark_employee_status()

    elif choice == '9':
        attendance_report()

    elif choice == '10':
        print("Thank you for using Employee Management System.")
        conn.close()
        break

    else:
        print("Invalid choice! Please try again.")