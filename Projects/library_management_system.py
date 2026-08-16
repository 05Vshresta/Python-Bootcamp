import sqlite3

# ============ DATABASE CONNECTION ========================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

print("Database connected successfully")
print("Welcome to the Library Management System")

# ============ CREATE TABLE ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    category TEXT,
    quantity INTEGER,
    available INTEGER
)
""")

print("Books Table created successfully")


# ============ ADD BOOK ====================================
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    category = input("Enter category: ")
    quantity = int(input("Enter quantity: "))

    cursor.execute("""
    INSERT INTO books(
        title, author, category, quantity, available
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        author,
        category,
        quantity, # Total quantity of books
        quantity  # Available quantity of books (initially same as total quantity)
    ))

    conn.commit()

    print("Book added successfully")

# ============ VIEW BOOKS ==================================
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if len(books) == 0:
        print("No Books Found")
    else:
        print("========== Available Books List ==============")

        for book in books:
            print(f"""
Book ID: {book[0]}
Title: {book[1]}
Author: {book[2]}
Category: {book[3]}
Quantity: {book[4]}
Available: {book[5]}
""")

# ============ MAIN MENU ===================================
while True:
    print("\n1. Add Book")
    print("2. View Books")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()

    elif choice == "3":
        print("Thank you for visiting!")
        conn.close()
        break

    else:
        print("Invalid choice")