import sqlite3
import re
from datetime import date


# =================== ADMIN CREDENTIALS ====================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ================= DATABASE CONNECTION ====================

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON")

print("Database connected successfully")
print("Welcome to the Library Management System")


# ================= CREATE BOOKS TABLE ======================

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
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


# ================ ADD AVAILABLE COLUMN IF MISSING ==========

# Useful if an older library.db already exists
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


# ================= CREATE ISSUED BOOKS TABLE ===============

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT NOT NULL DEFAULT 'Issued',

    FOREIGN KEY (book_id)
    REFERENCES books(book_id)
)
""")

conn.commit()

print("Issued Books Table created successfully")


# ====================== BOOK CLASS =========================

class Book:

    def __init__(self, title, author, category, quantity):
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity


    # ============ TITLE VALIDATION ==========================

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


    # ============ AUTHOR VALIDATION =========================

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


    # ============ CATEGORY VALIDATION =======================

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


    # ============ QUANTITY VALIDATION =======================

    @staticmethod
    def validate_quantity(quantity):

        if not isinstance(quantity, int) or quantity <= 0:
            print("Quantity should be a positive integer")
            return False

        return True


# ====================== ADD BOOK ===========================

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
        SELECT book_id
        FROM books
        WHERE title = ?
        AND author = ?
    """, (title, author))

    book = cursor.fetchone()

    if book:

        print("This book is already registered")
        return


    # -------- INSERT BOOK --------

    cursor.execute("""
        INSERT INTO books (
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


# ====================== VIEW BOOKS =========================

def view_books():

    print("\n========== BOOKS ==========")

    cursor.execute("""
        SELECT book_id,
               title,
               author,
               category,
               quantity,
               available
        FROM books
        ORDER BY book_id
    """)

    books = cursor.fetchall()

    if not books:

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


# ====================== SEARCH BOOK =======================

def search_book():

    print("\n========== SEARCH BOOK ==========")

    try:

        book_id = int(input("Enter book ID: "))

    except ValueError:

        print("Invalid input. Please enter a valid book ID.")
        return


    cursor.execute("""
        SELECT book_id,
               title,
               author,
               category,
               quantity,
               available
        FROM books
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


# ====================== UPDATE BOOK =======================

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
        SELECT book_id,
               title,
               author,
               category,
               quantity,
               available
        FROM books
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


    # -------- CALCULATE ISSUED COPIES --------

    issued_count = book[4] - book[5]


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

            if not Book.validate_quantity(quantity):
                continue

            if quantity < issued_count:

                print(
                    f"Quantity cannot be less than the "
                    f"number of issued books ({issued_count})."
                )
                continue

            break

        except ValueError:

            print("Quantity should be a valid integer")


    # -------- DUPLICATE CHECK --------

    cursor.execute("""
        SELECT book_id
        FROM books
        WHERE title = ?
        AND author = ?
        AND book_id != ?
    """, (title, author, book_id))

    duplicate = cursor.fetchone()


    if duplicate:

        print(
            "Another book with the same title and author "
            "already exists."
        )
        return


    # -------- CALCULATE NEW AVAILABLE COUNT --------

    available = quantity - issued_count


    # -------- UPDATE BOOK --------

    cursor.execute("""
        UPDATE books
        SET title = ?,
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
        available,
        book_id
    ))

    conn.commit()

    print("Book details updated successfully")


# ====================== DELETE BOOK ========================

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
        SELECT book_id,
               title,
               author,
               category,
               quantity,
               available
        FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()


    if not book:

        print("Book is not found")
        return


    # -------- CHECK ISSUE RECORDS --------

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE book_id = ?
    """, (book_id,))

    issue_count = cursor.fetchone()[0]


    if issue_count > 0:

        print(
            "This book cannot be deleted because "
            "it has issue records."
        )
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


# ================= MARK BOOK AVAILABILITY ==================

def mark_availability():

    print("\n========== MARK BOOK AVAILABILITY ==========")

    try:

        book_id = int(input("Enter Book ID: "))

    except ValueError:

        print("Invalid Book ID")
        print("Please enter a number")
        return


    # -------- FIND BOOK --------

    cursor.execute("""
        SELECT book_id,
               title,
               author,
               category,
               quantity,
               available
        FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()


    if not book:

        print("Book is not found")
        return


    print("========= CURRENT BOOK DETAILS =========")

    print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")


    # -------- AVAILABLE QUANTITY VALIDATION --------

    try:

        available = int(
            input("Enter Available Quantity: ")
        )

    except ValueError:

        print("Invalid Availability Quantity")
        print("Please enter a number")
        return


    if available < 0:

        print("Available quantity cannot be negative")
        return


    if available > book[4]:

        print(
            "Available quantity cannot be greater "
            "than total quantity"
        )
        return


    # -------- UPDATE AVAILABILITY --------

    cursor.execute("""
        UPDATE books
        SET available = ?
        WHERE book_id = ?
    """, (available, book_id))

    conn.commit()

    print("Book availability marked successfully")


# ====================== ISSUE BOOK ========================

def issue_book():

    print("\n========== ISSUE BOOK ==========")


    # -------- BOOK ID --------

    try:

        book_id = int(input("Enter Book ID: "))

    except ValueError:

        print("Invalid Book ID. Please enter a number.")
        return


    # -------- MEMBER ID --------

    try:

        member_id = int(input("Enter Member ID: "))

        if member_id <= 0:

            print("Member ID must be a positive integer.")
            return

    except ValueError:

        print("Invalid Member ID. Please enter a number.")
        return


    # -------- FIND BOOK --------

    cursor.execute("""
        SELECT book_id,
               title,
               author,
               category,
               quantity,
               available
        FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()


    if not book:

        print("Book is not found")
        return


    print("\n========= BOOK DETAILS =========")

    print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")


    # -------- CHECK AVAILABILITY --------

    if book[5] <= 0:

        print("No copies of this book are currently available.")
        return


    # -------- ISSUE DATE --------

    issue_date = date.today().isoformat()


    try:

        # Insert issue record
        cursor.execute("""
            INSERT INTO issued_books (
                book_id,
                member_id,
                issue_date,
                status
            )
            VALUES (?, ?, ?, ?)
        """, (
            book_id,
            member_id,
            issue_date,
            "Issued"
        ))


        # Decrease available count
        cursor.execute("""
            UPDATE books
            SET available = available - 1
            WHERE book_id = ?
            AND available > 0
        """, (book_id,))


        conn.commit()


        print("\nBook issued successfully!")
        print("Issue ID:", cursor.lastrowid)
        print("Book ID:", book_id)
        print("Member ID:", member_id)
        print("Issue Date:", issue_date)
        print("Remaining Available Copies:", book[5] - 1)


    except sqlite3.Error as e:

        conn.rollback()

        print("Database error:", e)


# ================= VIEW ISSUED BOOKS ======================

def view_issued_books():

    try:

        cursor.execute("""
            SELECT
                ib.issue_id,
                ib.book_id,
                b.title,
                ib.member_id,
                ib.issue_date,
                ib.return_date,
                ib.status
            FROM issued_books ib
            JOIN books b
            ON ib.book_id = b.book_id
            ORDER BY ib.issue_id
        """)

        records = cursor.fetchall()


        if not records:

            print("\nNo issued books found.")
            return


        print("\n================ ISSUED BOOKS ================")

        print(
            f"{'Issue ID':<10}"
            f"{'Book ID':<10}"
            f"{'Title':<25}"
            f"{'Member ID':<12}"
            f"{'Issue Date':<15}"
            f"{'Return Date':<15}"
            f"{'Status':<10}"
        )

        print("-" * 110)


        for record in records:

            (
                issue_id,
                book_id,
                title,
                member_id,
                issue_date,
                return_date,
                status
            ) = record


            print(
                f"{issue_id:<10}"
                f"{book_id:<10}"
                f"{title[:24]:<25}"
                f"{member_id:<12}"
                f"{issue_date:<15}"
                f"{str(return_date or '-'): <15}"
                f"{status:<10}"
            )


    except sqlite3.Error as e:

        print("Database error:", e)


# ====================== RETURN BOOK =======================

def return_book():

    print("\n========== RETURN BOOK ==========")


    try:

        issue_id = int(input("Enter Issue ID: "))

    except ValueError:

        print("Invalid Issue ID. Please enter a number.")
        return


    try:

        # -------- FIND ISSUE RECORD --------

        cursor.execute("""
            SELECT book_id,
                   member_id,
                   status
            FROM issued_books
            WHERE issue_id = ?
        """, (issue_id,))

        record = cursor.fetchone()


        if record is None:

            print("Issue record not found.")
            return


        book_id, member_id, status = record


        # -------- CHECK STATUS --------

        if status == "Returned":

            print("This book has already been returned.")
            return


        # -------- UPDATE ISSUE RECORD --------

        return_date = date.today().isoformat()


        cursor.execute("""
            UPDATE issued_books
            SET return_date = ?,
                status = ?
            WHERE issue_id = ?
        """, (
            return_date,
            "Returned",
            issue_id
        ))


        # -------- INCREASE AVAILABLE COUNT --------

        cursor.execute("""
            UPDATE books
            SET available = MIN(available + 1, quantity)
            WHERE book_id = ?
        """, (book_id,))


        conn.commit()


        print("\nBook returned successfully!")
        print("Issue ID:", issue_id)
        print("Book ID:", book_id)
        print("Member ID:", member_id)
        print("Return Date:", return_date)


    except sqlite3.Error as e:

        conn.rollback()

        print("Database error:", e)


# ======================== LOGIN ============================

def login():

    attempts = 3


    while attempts > 0:

        print("\n========== ADMIN LOGIN ==========")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()


        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            print("Login successful.")
            print("Welcome to the Library Management System!")

            return True


        else:

            attempts -= 1

            print("Invalid Username or Password")


            if attempts > 0:

                print(f"Remaining attempts: {attempts}")


    print("Your attempts exceed the maximum.")

    return False


# ====================== MAIN MENU ==========================

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
        print("6. Mark Book Availability")
        print("7. Issue Book")
        print("8. View Issued Books")
        print("9. Return Book")
        print("10. Exit")
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

            mark_availability()


        elif choice == "7":

            issue_book()


        elif choice == "8":

            view_issued_books()


        elif choice == "9":

            return_book()


        elif choice == "10":

            print(
                "\nThank you for using the "
                "Library Management System!"
            )

            conn.close()

            break


        else:

            print("Invalid choice. Please try again.")