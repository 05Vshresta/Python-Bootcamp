#library_management_system


import sqlite3

#===========database connection========================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
print("Database connected successfully")
print("Welcome to the Library Management System")

#============= Create the table=====================
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
book_id INTEGER PRIMARY KEY,
title TEXT,
author TEXT,
category Text,
quantity INTEGER,
available INTEGER
)
""")
print(" Books Table created successfully")
#================= ADD BOOK ==============================
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    category = input("Enter category: ")
    quantity = input("Enter quantity:")
    

    cursor.execute("""
    INSERT INTO books(
    title,author,category,quantity,available)
    VALUES(?, ?, ?, ?, ?)
    """,(
    title,
    author,
    category,
    quantity,
   
    ))
    conn.commit()

    print("Book added successfully")

#=====================================================
    while True:
        print("1. Add Book")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            print("Thank you for visiting!")
            conn.close()
            break

        else:
            print("Invalid choice")


