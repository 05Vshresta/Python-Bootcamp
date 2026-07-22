import sqlite3

#create the table to db
def create_table():
  conn = sqlite3.connect("students.db")
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS student(
  id INTEGER PRIMARY KEY,
  name TEXT,
  course TEXT,
  marks INTEGER
  )
  """)
  conn.commit()
  conn.close()

#Add new student to db
def add_student():
  name = input("Enter Name : ")
  course = input("Enter Course : ")
  marks = int(input("Enter Marks :"))
  conn = sqlite3.connect("students.db")
  cursor = conn.cursor()
  cursor.execute("INSERT INTO student(name,course,marks) VALUES(?,?,?)",(name,course,marks))
  conn.commit()
  conn.close()
  print("Students data added successfully")

#Display all the student records
def view_student():
  conn = sqlite3.connect("students.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM student")
  rows = cursor.fetchall()
  conn.commit()
  conn.close()

  for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} | Course:{row[2]} | Marks: {row[3]}")

#update student details
def update_student():
  student_id = int(input("Enter the student id to update marks : "))
  new_marks = int(input("marks : "))
  conn = sqlite3.connect("students.db")
  cursor = conn.cursor()
  cursor.execute("UPDATE student SET marks = ? WHERE id = ?",(new_marks,student_id))
  conn.commit()
  conn.close()
  print("Students data updated successfully")

#delete a student record
def delete_student():
  student_id = int(input("Enter the student id to delete marks : "))
  conn = sqlite3.connect("students.db")
  cursor = conn.cursor()
  cursor.execute("DELETE FROM student WHERE id = ?",(student_id,))
  conn.commit()
  conn.close()
  print("Students data deleted successfully")

create_table()
while True:
  print("\n1.Add student", "2.View student", "3.Update student", "4.Delete student", "5.Exit")
  choice = int(input("Enter your choice : "))
  if choice == 1 : add_student()
  elif choice == 2 : view_student()
  elif choice == 3 : update_student()
  elif choice == 4 : delete_student()
  elif choice == 5 : break
  else : print("Invalid choice")