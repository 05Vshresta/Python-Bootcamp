"""Simple Student management student"""

student_names = {}

while True:
    print("\n====Student Management System====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Exit")

    choice = input("Enter your choice : ")

    if choice == "1":
        roll_no = input("Enter Roll Number : ")
        name = input("Enter Student name : ")
        student_names[roll_no] = name
        print("Student added successfully!")

    elif choice == "2":
        print("\nStudent Records")
        for roll_no,name in student_names.items():
            print(roll_no, "-" ,name)
    
    elif choice == "3":
        print("Thank you!")

    else:
        print("Invalid choice.")

