import sqlite3

conn = sqlite3.connect("student_managment.db")
cursor = conn.cursor()

print("Database is connection build successfully")

#==============create students table===========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
student_id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
mobile TEXT,
email TEXT,
course TEXT,
attendance INTEGER DEFAULT 0)
""")
print("Students Table is created")

#==============Alter students table===============================================
# Add the attendance column if it doesn't exist (for schema evolution)
try:
    cursor.execute("ALTER TABLE students ADD COLUMN attendance INTEGER DEFAULT 0")
    conn.commit()
    print("Added 'attendance' column to students table (if it was missing).")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("'attendance' column already exists.")
    else:
        raise # Re-raise other operational errors

#==============Student Class==================
class Student:
  def __init__(self,name,mobile,email,course):
    self.name = name
    self.mobile = mobile
    self.email = email
    self.course = course

  #===========Student Registration==========================
  def register(self):
    cursor.execute("""
    INSERT INTO students(name,mobile,email,course)
    VALUES(?,?,?,?)""",
    (self.name,
     self.mobile,
     self.email,
     self.course
    ))

    conn.commit()
  #===========Display Students Details==========================
  @staticmethod
  def display_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if len(students) == 0:
      print("No students data is found")
    else:
      print("===========Available Students List===========")
      for student in students:
        print(f"""
        Student ID : {student[0]}
        Name : {student[1]}
        Mobile : {student[2]}
        Email : {student[3]}
        Course : {student[4]}
        Attendance : {student[5]}
        """)

  #=========Student Search by id============
  @staticmethod
  def search_by_id():
    student_id = int(input("Enter the student ID :"))
    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?""",(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Student Details=========")

      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
        """)
    else:
      print("Student is not found")

  #=========Student Search by name================
  @staticmethod
  def search_by_name():
    name = input("Enter the student name :")
    cursor.execute("""
    SELECT * FROM students
    WHERE name LIKE ?
    """,("%" + name + "%",))

    students = cursor.fetchall()

    if students:
      print("=========Student Details=========")

      for student in students:
        print(f"""
        Student ID : {student[0]}
        Name : {student[1]}
        Mobile : {student[2]}
        Email : {student[3]}
        Course : {student[4]}
        Attendance : {student[5]}
         """)
    else:
      print("Student is not found")

  #==========Update Student===============
  @staticmethod
  def update_student():

    student_id = int(input("Enter the student ID :"))

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Current Student Details=========")
      print("----------------------------------------")
      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
        """)
      print("----------------------------------------")
      print("Update Student Details")
      print("----------------------------------------")

      name = input("Enter the name :")
      mobile = input("Enter the mobile no :")
      email = input("Enter the email :")
      course = input("Enter the course :")

      cursor.execute("""
      UPDATE students

      SET
      name = ?,
      mobile = ?,
      email = ?,
      course = ?
      WHERE student_id = ?
      """,(
        name,
        mobile,
        email,
        course,
        student_id
      ))

      conn.commit()

      print("Student data is updated successfully")
    else:
      print("Student is not found")

  #==========Delete Student===============
  @staticmethod
  def delete_student():
    student_id = int(input("Enter the student ID :"))

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Current Student Details=========")
      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
      """)

      confirm = input("Are you sure about to delete this partcular student?(Y/N): ").upper()

      if confirm == "Y" :
        cursor.execute("""
        DELETE FROM students
        WHERE student_id = ?
        """,(student_id,))

        conn.commit()
        print("Student data is deleted successfully")

      else:
        print("Student data is not deleted")
    else:
      print("Student data is not found by the ID")

  #=========Mark Attendance============
  @staticmethod
  def mark_attendance():
    student_id = int(input("Enter the student ID :"))

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Current Student Details=========")
      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
      """)

      print("""
      Attendance Status
      1 -> Present
      0 -> Absent
      """)

      attendance = int(input("Enter Attenadance :"))

      if attendance not in (0,1):
        print("Invalid Attendance value")
        return

      cursor.execute("""
      UPDATE students

      SET attendance = ?
      WHERE student_id = ?
      """,
       (attendance,
        student_id))

      conn.commit()

      print("Student Attendance is updated successfully")

    else:
      print("Student is not found")

  #=========Attendance Report============
  @staticmethod
  def attendance_report():
    cursor.execute("""
    SELECT student_id,
        name,
        course,
        attendance
    FROM students""")
    
    students = cursor.fetchall()

    if len(students) == 0:
      print("No students data is found")
    else:
      print("===========Attendance Report===========")
      for student in students:

        status = "Present" if student[3] == 1 else "Absent"

        print(f"""
        Student ID : {student[0]}
        Name : {student[1]}
        Course : {student[2]}
        Attendance : {status}
        """)

while True:
  print("""
  =========Student Mangement System============
  1.Register Students
  2.View students
  3.Search by id
  4.Search by name
  5.Update Student
  6.Delete Student
  7.Attendance
  8.Attendance Report
  9.Exit
  """)

  choice = input("Enter the choice :")

  if choice == "1":
    print("=========student registration===========")
    name = input("Enter the name :")
    mobile = input("Enter the mobile no :")
    email = input("Enter the email :")
    course = input("Enter the course :")

    student = Student(name,mobile,email,course)

    student.register()

  elif choice == "2":
    Student.display_students()

  elif choice =="3":
    Student.search_by_id()

  elif choice == "4":
    Student.search_by_name()

  elif choice == "5":
    Student.update_student()

  elif choice == "6":
    Student.delete_student()

  elif choice == "7":
    Student.mark_attendance()

  elif choice == "8":
    Student.attendance_report()

  elif choice == "9":
    print("Thank you")
    break

  else:
    print("Invalid Choice")

conn.close()

print("Database is closed successfully")

