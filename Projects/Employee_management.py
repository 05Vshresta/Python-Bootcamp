#================Employee Management System================

import sqlite3
import re

#============================
#Admin Credentials
#============================
USERNAME = "admin"
PASSWORD = "admin123"

#=========== Database Connection =============================
conn =  sqlite3.connect("employee.db")
cursor = conn.cursor()

#========== Create a Employee Table =============
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
employee_id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
mobile TEXT,
email TEXT,
department TEXT,
salary REAL,
attendance INTEGER DEFAULT 0
)
""")
print("Employee Table Created Successfully")

# Add the attendance column if it doesn't exist (for schema evolution)
try:
    cursor.execute("ALTER TABLE employees ADD COLUMN attendance INTEGER DEFAULT 0")
    conn.commit()
    print("Added 'attendance' column to employees table (if it was missing).")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("'attendance' column already exists.")
    else:
        raise # Re-raise other operational errors

#=================== Employee Class ===========================
class Employee:
  def __init__(self, name, mobile, email, department, salary):
    self.name = name
    self.mobile = mobile
    self.email = email
    self.department = department
    self.salary = salary

#===========Name Validation==================
  @staticmethod
  def validate_name(name):
    if name.strip() == "": # Changed from " " to "" to catch empty string
      print("Name cannot be empty")
      return False

    if not name.replace(" ","").isalpha():
      print("Name should contain only alphabets")
      return False

    if len(name.strip()) < 3:
      print("Name should be at least 3 characters long")
      return False

    return True

  #======Mobile Validation==========
  @staticmethod
  def validate_mobile(mobile):

    if not mobile.isdigit():
      print("Mobile should contain only digits")
      return False
    
    if len(mobile) != 10:
      print("Mobile should be 10 digits long")
      return False
    
    if mobile[0] not in ["6","7","8","9"]:
      print("Mobile should start with 6,7,8,9")
      return False
    
    return True

  #======EMail Validation===========S
  @staticmethod
  def validate_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern,email):
      print("Invalid Email")
      return False
    
    return True

  #======Department Validation========== (Renamed from validate_course)
  @staticmethod
  def validate_department(department):
    
    departments =["Python","Java","AI&ML","Data Science","Full Stack"]

    if department not in departments:
      print("Invalid Department")
      print("Available Departments are :")

      for dept in departments:
        print("-",dept)
      return False

    return True


#===================== Employee Registration ========================
  def register(self):
  #Name Validation
    if not Employee.validate_name(self.name):
      return

    #Mobile Validation
    if not Employee.validate_mobile(self.mobile):
      return

    #Email Validation
    if not Employee.validate_email(self.email):
      return

    #Department Validation
    if not Employee.validate_department(self.department):
      return


    #Duplicate Mobile Check
    cursor.execute("""
    SELECT COUNT(*) FROM employees
    WHERE mobile = ?
    """,(self.mobile,))

    if cursor.fetchone()[0]:
      print("Mobile number is already registered")
      return

    #Duplicate Mail Check
    cursor.execute("""
    SELECT COUNT(*) FROM employees
    WHERE email = ?
    """,(self.email,))


    if cursor.fetchone()[0]:
      print("Email is already registered")
      return


    cursor.execute("""
    INSERT INTO employees(name, mobile, email, department, salary)
    VALUES (?, ?, ?, ?, ?)
    """,(
      self.name,
      self.mobile,
      self.email,
      self.department,
      self.salary
    )
    )

    conn.commit()
    print("Employee Registered Successfully")

#========================= Display Employees ================================
  @staticmethod
  def display_employees():
    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    if len(employees) == 0:
      print("No Employees Found")
    else:
      print("========== Available Employees List==============")
      for employee in employees:
        print(f"""
employee ID: {employee[0]}
Name: {employee[1]}
Mobile: {employee[2]}
Email: {employee[3]}
Department: {employee[4]}
Salary: {employee[5]}
Attendance: {employee[6]}
""")

#============================ Employee Search by id ===========================
  @staticmethod
  def search_employee_by_id():
    try:
      employee_id = int(input("Enter Employee ID: "))
    except ValueError:
      print("Invalid Input")
      print("Please Enter a number")
      return

    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = cursor.fetchone()
    if employee:
      print(f"""
  employee id : {employee[0]}
  Name: {employee[1]}
  Mobile: {employee[2]}
  Email: {employee[3]}
  Department: {employee[4]}
  Salary: {employee[5]}
  Attendance: {employee[6]}
  """)
    else:
      print("Employee Not Found")

#============================== Employee Search by name =======================
  @staticmethod
  def search_employee_by_name():
    name = input("Enter Employee Name: ")
    cursor.execute("""SELECT * FROM employees where name LIKE ?""",("%" + name + "%",))
    employees = cursor.fetchall()
    if employees:
      print("========== Available Employees List==============")
      for employee in employees:
        print(f"""
    employee ID: {employee[0]}
    Name: {employee[1]}
    Mobile: {employee[2]}
    Email: {employee[3]}
    Department: {employee[4]}
    Salary: {employee[5]}
    """)
    else:
      print("Employee Not Found")

#================================ Update Employee details =====================
  @staticmethod
  def update_employee():

    try:
      employee_id = int(input("Enter Employee ID: "))
    except ValueError:
      print("Invalid Input")
      print("Please Enter a number")
      return

    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = cursor.fetchone()
    if employee:
      print("=============== Current Employee details ===================")
      print("------------------------------------------------------------")
      print(f"""
    employee ID: {employee[0]}
    Name: {employee[1]}
    Mobile: {employee[2]}
    Email: {employee[3]}
    Department: {employee[4]}
    Salary: {employee[5]}
    Attendance:{employee[6]}
    """)
      print("------------------------------------------------------------")
      print("===================== Update Employee Details =====================")
      print("------------------------------------------------------------")
      name = input("Enter Employee Name: ")
      mobile = input("Enter Employee Mobile: ")
      email = input("Enter Employee Email: ")
      department = input("Enter Employee Department: ")
      salary = float(input("Enter Employee Salary: "))
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
      conn.commit()
      print("Employee Details Updated Successfully")
    else:
      print("Employee Not Found")


  #============================ Delete Employee Details =======================
  @staticmethod
  def delete_employee():
    try:
      employee_id = int(input("Enter Employee ID: "))
    except ValueError:
      print("Invalid Input")
      print("Please Enter a number")
      return

    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = cursor.fetchone()
    if employee:
      print("=============== Current Employee details ===================")
      print("------------------------------------------------------------")
      print(f"""
    employee ID: {employee[0]}
    Name: {employee[1]}
    Mobile: {employee[2]}
    Email: {employee[3]}
    Department: {employee[4]}
    Salary: {employee[5]}
    """)

      confirm = input("Are you sure you want to delete this employee? (Y/N): ").upper()

      if confirm == "Y":
        cursor.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        conn.commit()
        print("Employee Deleted Successfully")
      else:
        print("Employee Not Deleted")
    else:
      print("Employee Not Found")

  #=============================== Mark Attendance ========================
  @staticmethod
  def mark_attendance():
    try:
      employee_id = int(input("Enter Employee ID: "))
    except ValueError:
      print("Invalid Input")
      print("Please Enter a number")
      return

    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = cursor.fetchone()
    if employee:
      print(f"""
      employee ID: {employee[0]}
      Name: {employee[1]}
      Mobile: {employee[2]}
      Email: {employee[3]}
      Department: {employee[4]}
      Salary: {employee[5]}
      """)

      print("""
      Attendance status
        1 -> Present
        0 -> Absent
      """)

      attendance = int(input("Enter Attendance: "))
      cursor.execute("""
      UPDATE employees
      SET
      attendance = ?
      WHERE employee_id = ?
      """,(
        attendance,
        employee_id
      ))
      
      conn.commit()
      print("Attendance Marked Successfully")
    else:
      print("Employee Not Found")

  #======================= Attendance Report ==================================
  @staticmethod
  def attendance_report():
    cursor.execute("""
    SELECT employee_id,
        name,
        department, 
        attendance
    FROM employees""")

    employees = cursor.fetchall()

    if len(employees) == 0:
      print("No employees data is found")
    else:
      print("===========Attendance Report===========")
      for employee in employees:

        status = "Present" if employee[3] == 1 else "Absent"

        print(f"""
        Employee ID : {employee[0]}
        Name : {employee[1]}
        Department : {employee[2]}
        Attendance : {status}
        """)

  #============= Dashboard ====================
  @staticmethod
  def dashboard():
    #Total Employees
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    #Present employees
    cursor.execute("SELECT COUNT(*) FROM employees WHERE attendance = 1")
    present_employees = cursor.fetchone()[0]

    #Absent employees
    cursor.execute("SELECT COUNT(*) FROM employees WHERE attendance = 0")
    absent_employees = cursor.fetchone()[0]

    #Attendance Percentage
    if total_employees > 0:
      attendance_percentage = (present_employees / total_employees) * 100
    else:
      attendance_percentage = 0

    print("=========================")
    print("Employees Dashboard")
    print("========================")

    print(f"Total Employee :{total_employees}")
    print(f"Present Employee :{present_employees}")
    print(f"Absent Employee :{absent_employees}")
    print(f"Attendance Percentage :{attendance_percentage}")
    print("=========================")

  #========= LogIn ====================
  @staticmethod
  def login():
    attempts = 3

    while attempts > 0:
      print("===============Admin Login====================")
      username = input("Username :")
      password = input("Password :")

      if (username == USERNAME) and (password == PASSWORD):
        print("LogIn is Successfull")
        print("Welcome Admin")

        return True

      else:
        attempts -= 1
        print("Invalid Username or Password")

        if attempts > 0:
          print(f"Remaining attempts :{attempts}")

    print("Your attempts exceed the Maximum")      # This line should be outside the while loop


if Employee.login():
  while True:
    print("""
    =========Employee Management System============
    1.Register Employee
    2.View Employee
    3.Search by id
    4.Search by name
    5.Update Employee
    6.Delete Employee
    7.Attendance
    8.Attendance Report
    9.Dashboard
    10.Exit
    """)

    choice = input("Enter the choice :")

    if choice == "1":
        print("=========Employee registration===========")
        name = input("Enter the name :")
        mobile = input("Enter the mobile no :")
        email = input("Enter the email :")
        print("""Available Departments are :
        1.Python
        2.Java
        3.AI&ML
        4.Data Science
        5.Full Stack""")

        department = input("Enter the department :") # Changed from course to department
        salary = float(input("Enter the salary :" )) # Added salary input


        employee = Employee(name,mobile,email,department, salary) # Corrected parameters

        employee.register()

    elif choice == "2":
      Employee.display_employees()

    elif choice =="3":
      Employee.search_employee_by_id()

    elif choice == "4":
        Employee.search_employee_by_name()

    elif choice == "5":
        Employee.update_employee()

    elif choice == "6":
        Employee.delete_employee()

    elif choice == "7":
        Employee.mark_attendance()

    elif choice == "8":
        Employee.attendance_report()

    elif choice == "9":
        Employee.dashboard()

    elif choice == "10":
      print("Thank you")
      break
    else:
      print("Invalid Choice")

conn.close()

print("Database is closed successfully")