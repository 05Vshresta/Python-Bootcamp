import sqlite3
conn = sqlite3.connect("student_managment.db")
cursor = conn.cursor()
print("Database is connection build successfully")
#===========Student table==============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
student_id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
mobile TEXT,
email TEXT,
course TEXT,
attedance INTEGER DEFAULT 0)
""")
print("Students Table is created")
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
#=========================Display Students=========================
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
        Attendance : {student[5]}""")
#==========================Main Program=========================
while True:
  print("""
  =========Student Mangement System============
  1.Register Students
  2.View students
  3.Exit
  """)
#==========================User Input================================
  choice = input("Enter the choice : ")
  if choice == "1":
    print("=========student registration=========== ")
    name = input("Enter the name : ")
    mobile = input("Enter the mobile no : ")
    email = input("Enter the email : ")
    course = input("Enter the course : ")
    student = Student(name,mobile,email,course)
    student.register()
  elif choice == "2":
    Student.display_students()
  elif choice == "3":
    print("Thank you")
    break
  else:
    print("Invalid Choice")
#==============Close Connection====================================
conn.close()
print("Database is closed successfully")