import sqlite3
import re
#=================== Admin Credentials ====================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============ DATABASE CONNECTION ========================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

print("Database connected successfully")
print("Welcome to the Library Management System")


# ============ CREATE TABLE ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    available INTEGER NOT NULL
)
""")

conn.commit()

print("Books Table created successfully")


# ============ ADD AVAILABLE COLUMN IF MISSING =============
# This is useful if an older library.db already exists
try:
    cursor.execute(
        "ALTER TABLE books ADD COLUMN available INTEGER DEFAULT 0"
    )
    conn.commit()
    print("'available' column added successfully.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("'available' column already exists.")
    else:
        raise


# =================== BOOK CLASS ==========================
class Book:

    def __init__(self, title, author, category, quantity):
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity

    # ============ TITLE VALIDATION ========================
    @staticmethod
    def validate_title(title):

        if title.strip() == "":
            print("Title cannot be empty")
            return False

        if not re.fullmatch(
            r"[A-Za-z0-9\s:,'!?&.+()\-]+",
            title
        ):
            print(
                "Title should contain only letters, numbers, "
                "spaces and basic punctuation"
            )
            return False

        if len(title.strip()) < 2:
            print("Title should be at least 2 characters long")
            return False

        return True

    # ============ AUTHOR VALIDATION =======================
    @staticmethod
    def validate_author(author):

        if author.strip() == "":
            print("Author name cannot be empty")
            return False

        if not re.fullmatch(r"[A-Za-z\s.]+", author):
            print(
                "Author name should contain only letters, "
                "spaces and dots"
            )
            return False

        if len(author.strip()) < 2:
            print("Author name should be at least 2 characters long")
            return False

        return True

    # ============ CATEGORY VALIDATION =====================
    @staticmethod
    def validate_category(category):

        if category.strip() == "":
            print("Category cannot be empty")
            return False

        if not re.fullmatch(r"[A-Za-z\s]+", category):
            print("Category should contain only letters and spaces")
            return False

        if len(category.strip()) < 2:
            print("Category should be at least 2 characters long")
            return False

        return True

    # ============ QUANTITY VALIDATION =====================
    @staticmethod
    def validate_quantity(quantity):

        if not isinstance(quantity, int) or quantity <= 0:
            print("Quantity should be a positive integer")
            return False

        return True


# ============ ADD BOOK ====================================
def add_book():

    print("\n========== ADD BOOK ==========")

    # -------- TITLE VALIDATION --------
    while True:
        title = input("Enter book title: ").strip()

        if Book.validate_title(title):
            break

    # -------- AUTHOR VALIDATION --------
    while True:
        author = input("Enter author name: ").strip()

        if Book.validate_author(author):
            break

    # -------- CATEGORY VALIDATION --------
    while True:
        category = input("Enter category: ").strip()

        if Book.validate_category(category):
            break

    # -------- QUANTITY VALIDATION --------
    while True:
        try:
            quantity = int(input("Enter quantity: "))

            if Book.validate_quantity(quantity):
                break

        except ValueError:
            print("Quantity should be a valid integer")

    # -------- DUPLICATE BOOK CHECK --------
    cursor.execute("""
        SELECT * FROM books
        WHERE title = ? AND author = ?
    """, (title, author))

    book = cursor.fetchone()

    if book:
        print("This book is already registered")
        return

    # -------- INSERT BOOK --------
    cursor.execute("""
        INSERT INTO books(
            title,
            author,
            category,
            quantity,
            available
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        author,
        category,
        quantity,
        quantity
    ))

    conn.commit()

    print("Book added successfully")


# ============ VIEW BOOKS ==================================
def view_books():

    print("\n========== AVAILABLE BOOKS ==========")

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if len(books) == 0:
        print("No Books Found")
        return

    for book in books:

        print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
----------------------------------------
""")


# ============ SEARCH BOOK ================================
def search_book():

    print("\n========== SEARCH BOOK ==========")

    try:
        book_id = int(input("Enter book ID: "))

    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        return

    cursor.execute("""
        SELECT * FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()

    if book:

        print("\n========= BOOK DETAILS =========")

        print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")

    else:
        print("Book is not found")


# ============ UPDATE BOOK ================================
def update_book():

    print("\n========== UPDATE BOOK ==========")

    # -------- BOOK ID VALIDATION --------
    try:
        book_id = int(input("Enter book ID: "))

    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        return

    # -------- FIND BOOK --------
    cursor.execute("""
        SELECT * FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()

    if not book:
        print("Book is not found")
        return

    # -------- DISPLAY CURRENT DETAILS --------
    print("\n========= CURRENT BOOK DETAILS =========")

    print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")

    print("----------------------------------------")
    print("Enter New Book Details")
    print("----------------------------------------")

    # -------- NEW TITLE --------
    while True:
        title = input("Enter new title: ").strip()

        if Book.validate_title(title):
            break

    # -------- NEW AUTHOR --------
    while True:
        author = input("Enter new author: ").strip()

        if Book.validate_author(author):
            break

    # -------- NEW CATEGORY --------
    while True:
        category = input("Enter new category: ").strip()

        if Book.validate_category(category):
            break

    # -------- NEW QUANTITY --------
    while True:
        try:
            quantity = int(input("Enter new quantity: "))

            if Book.validate_quantity(quantity):
                break

        except ValueError:
            print("Quantity should be a valid integer")

    # -------- DUPLICATE CHECK --------
    cursor.execute("""
        SELECT * FROM books
        WHERE title = ?
        AND author = ?
        AND book_id != ?
    """, (title, author, book_id))

    duplicate = cursor.fetchone()

    if duplicate:
        print("Another book with the same title and author already exists.")
        return

    # -------- UPDATE BOOK --------
    cursor.execute("""
        UPDATE books
        SET
            title = ?,
            author = ?,
            category = ?,
            quantity = ?,
            available = ?
        WHERE book_id = ?
    """, (
        title,
        author,
        category,
        quantity,
        quantity,
        book_id
    ))

    conn.commit()

    print("Book details updated successfully")


# ============ DELETE BOOK =================================
def delete_book():

    print("\n========== DELETE BOOK ==========")

    # -------- BOOK ID VALIDATION --------
    try:
        book_id = int(input("Enter book ID: "))

    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        return

    # -------- FIND BOOK --------
    cursor.execute("""
        SELECT * FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()

    if not book:
        print("Book is not found")
        return

    # -------- DISPLAY BOOK --------
    print("\n========= BOOK DETAILS =========")

    print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")

    # -------- DELETE CONFIRMATION --------
    confirm = input(
        "Are you sure you want to delete this book? (y/n): "
    ).strip().upper()

    if confirm == "Y":

        cursor.execute("""
            DELETE FROM books
            WHERE book_id = ?
        """, (book_id,))

        conn.commit()

        print("Book deleted successfully")

    elif confirm == "N":
        print("Book deletion cancelled")

    else:
        print("Invalid choice. Book deletion cancelled")

#================== Log In ================================
@staticmethod
def login():
    attempts = 3
    while attempts > 0:
        print("\n========== ADMIN LOGIN ==========")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Login successful.")
            print("Welcome to the Library Management System!")
            return True
        
        else:
            attempts -= 1
            print("Invalid Username or Password")
           
            if attempts > 0:
                print(f"Remaining attempts :{attempts}")

    print("Your attempts exceed the Maximum")  


# ============ MAIN MENU ===================================
if login():
    while True:

     print("\n========================================")
     print("       LIBRARY MANAGEMENT SYSTEM")
     print("========================================")

     print("1. Add Book")
     print("2. View Books")
     print("3. Search by ID")
     print("4. Update Book")
     print("5. Delete Book")
     print("6. Exit")

     print("========================================")

     choice = input("Enter your choice: ").strip()

     if choice == "1":
         add_book()

     elif choice == "2":
        view_books()

     elif choice == "3":
        search_book()

     elif choice == "4":
        update_book()

     elif choice == "5":
        delete_book()

     elif choice == "6":

        print("\nThank you for using the Library Management System!")

        conn.close()

        break

     else:
        print("Invalid choice. Please select 1-6.")