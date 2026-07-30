import sqlite3

print("="*50)
print("Student Management System")
print("="*50)

conn = sqlite3.connect("student_mngmt_system.db")
cursor = conn.cursor()
print("Database created successfully.")

#=========== Student Table ===================================
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS students(
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    mobile TEXT,
    email TEXT,
    course TEXT ,
    attendance INTEGER DEFAULT 0)''')
print("Student Table created successfully.")

#========== Attendance Table ====================================
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS attendance(
    attendance_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    date TEXT,
    status TEXT)'''
)
print("Attendance Table created successfully.")
conn.commit()

#============= SQL Query ==================================
cursor.execute(
    '''SELECT name FROM sqlite_master 
    WHERE type="table" '''
)
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

#=================Display student table structure =========================
cursor.execute("PRAGMA table_info(students)")
columns = cursor.fetchall()
print("Student Table Structure:")
for column in columns:
    print(column)

#=================== Display Attendance table structure ===============================
cursor.execute("PRAGMA table_info(attendance)")
columns = cursor.fetchall()
print("Attendance Table Structure:")
for column in columns:
    print(column)

#===================Student Registration=====================================
print("Project Features")
features = [
    "1. Student Registration",
    "2. View Student",
    "3. Search Student",
    "4. Update Student",
    "5. Delete Student",
    "6.Attendance",
    "7.Report"
]
for feature in features:
    print(feature)

conn.close()
print("Database connection closed.")