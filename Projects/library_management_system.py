"""Simple Library Management System"""

import sqlite3
import re
from datetime import date


# ============================================================
# ADMIN CREDENTIALS
# ============================================================

USERNAME = "admin"
PASSWORD = "admin123"


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

print("Database connection built successfully")
print("Welcome to the Library Management System")


# ============================================================
# CREATE BOOKS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    available INTEGER NOT NULL
)
""")

print("Books table created successfully")


# ============================================================
# CREATE MEMBERS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS members(
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

print("Members table created successfully")


# ============================================================
# CREATE ISSUED BOOKS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books(
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT NOT NULL DEFAULT 'Issued',

    FOREIGN KEY(book_id)
    REFERENCES books(book_id),

    FOREIGN KEY(member_id)
    REFERENCES members(member_id)
)
""")

print("Issued books table created successfully")

conn.commit()


# ============================================================
# BOOK CLASS
# ============================================================

class Book:

    # ========================================================
    # CONSTRUCTOR
    # ========================================================

    def __init__(self, title, author, category, quantity):
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity

    # ========================================================
    # TITLE VALIDATION
    # ========================================================

    @staticmethod
    def validate_title(title):

        if title.strip() == "":
            print("Title cannot be empty")
            return False

        if not re.fullmatch(
                r"[A-Za-z0-9\s:,'!?&.+-]+",
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

    # ========================================================
    # AUTHOR VALIDATION
    # ========================================================

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

    # ========================================================
    # CATEGORY VALIDATION
    # ========================================================

    @staticmethod
    def validate_category(category):

        if category.strip() == "":
            print("Category cannot be empty")
            return False

        if not re.fullmatch(r"[A-Za-z\s&]+", category):
            print(
                "Category should contain only letters, "
                "spaces and &"
            )
            return False

        if len(category.strip()) < 2:
            print("Category should be at least 2 characters long")
            return False

        return True

    # ========================================================
    # QUANTITY VALIDATION
    # ========================================================

    @staticmethod
    def validate_quantity(quantity):

        if not isinstance(quantity, int) or quantity <= 0:
            print("Quantity should be a positive integer")
            return False

        return True

    # ========================================================
    # ADD BOOK
    # ========================================================

    @staticmethod
    def add_book():

        # ---------------- TITLE ----------------

        while True:
            title = input("Enter book title: ").strip()

            if Book.validate_title(title):
                break

        # ---------------- AUTHOR ----------------

        while True:
            author = input("Enter author name: ").strip()

            if Book.validate_author(author):
                break

        # ---------------- CATEGORY ----------------

        while True:
            category = input("Enter category: ").strip()

            if Book.validate_category(category):
                break

        # ---------------- QUANTITY ----------------

        while True:

            try:
                quantity = int(input("Enter quantity: "))

                if Book.validate_quantity(quantity):
                    break

            except ValueError:
                print("Quantity should be a valid integer")

        # ---------------- DUPLICATE BOOK CHECK ----------------

        cursor.execute("""
            SELECT book_id
            FROM books
            WHERE title = ?
            AND author = ?
        """, (title, author))

        existing_book = cursor.fetchone()

        if existing_book is not None:
            print("This book is already registered")
            return

        # ---------------- INSERT BOOK ----------------

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

    # ========================================================
    # VIEW BOOKS
    # ========================================================

    @staticmethod
    def display_books():

        cursor.execute("""
            SELECT
                book_id,
                title,
                author,
                category,
                quantity,
                available
            FROM books
        """)

        books = cursor.fetchall()

        if len(books) == 0:

            print("No books data is found")

        else:

            print("=========== Available Books List ===========")

            for book in books:

                print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
----------------------------------------------
""")

    # ========================================================
    # SEARCH BOOK BY ID
    # ========================================================

    @staticmethod
    def search_by_id():

        try:
            book_id = int(input("Enter the book ID: "))

        except ValueError:
            print("Invalid Book ID")
            print("Please enter a number")
            return

        cursor.execute("""
            SELECT
                book_id,
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

            print("=========== Book Details ===========")

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

    # ========================================================
    # UPDATE BOOK
    # ========================================================

    @staticmethod
    def update_book():

        try:
            book_id = int(input("Enter the book ID: "))

        except ValueError:
            print("Invalid Book ID")
            print("Please enter a number")
            return

        cursor.execute("""
            SELECT
                book_id,
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

            print("=========== Current Book Details ===========")

            print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")

            print("------------------------------------------")
            print("Update Book Details")
            print("------------------------------------------")

            # ---------------- TITLE ----------------

            while True:

                title = input("Enter new title: ").strip()

                if Book.validate_title(title):
                    break

            # ---------------- AUTHOR ----------------

            while True:

                author = input("Enter new author: ").strip()

                if Book.validate_author(author):
                    break

            # ---------------- CATEGORY ----------------

            while True:

                category = input("Enter new category: ").strip()

                if Book.validate_category(category):
                    break

            # ---------------- QUANTITY ----------------

            while True:

                try:

                    quantity = int(
                        input("Enter new quantity: ")
                    )

                    if Book.validate_quantity(quantity):
                        break

                except ValueError:

                    print("Quantity should be a valid integer")

            # Calculate currently issued copies

            issued_copies = book[4] - book[5]

            if quantity < issued_copies:

                print(
                    f"Quantity cannot be less than "
                    f"currently issued copies ({issued_copies})"
                )

                return

            # Calculate new available quantity

            available = quantity - issued_copies

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
                available,
                book_id
            ))

            conn.commit()

            print("Book details updated successfully")

        else:

            print("Book is not found")

    # ========================================================
    # DELETE BOOK
    # ========================================================

    @staticmethod
    def delete_book():

        try:
            book_id = int(input("Enter the book ID: "))

        except ValueError:

            print("Invalid Book ID")
            print("Please enter a number")
            return

        cursor.execute("""
            SELECT
                book_id,
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

            print("=========== Current Book Details ===========")

            print(f"""
Book ID    : {book[0]}
Title      : {book[1]}
Author     : {book[2]}
Category   : {book[3]}
Quantity   : {book[4]}
Available  : {book[5]}
""")

            # Check issued copies

            issued_copies = book[4] - book[5]

            if issued_copies > 0:

                print(
                    "This book cannot be deleted because "
                    f"{issued_copies} copy/copies are currently issued."
                )

                return

            # Confirmation

            confirm = input(
                "Are you sure you want to delete this book? (Y/N): "
            ).upper()

            if confirm == "Y":

                cursor.execute("""
                    DELETE FROM books
                    WHERE book_id = ?
                """, (book_id,))

                conn.commit()

                print("Book deleted successfully")

            else:

                print("Book deletion cancelled")

        else:

            print("Book is not found")

    # ========================================================
    # ISSUE BOOK
    # ========================================================

    @staticmethod
    def issue_book():

        try:

            book_id = int(input("Enter the book ID: "))
            member_id = int(input("Enter the member ID: "))

        except ValueError:

            print("Book ID and Member ID must be numbers")
            return

        # ---------------- CHECK BOOK ----------------

        cursor.execute("""
            SELECT title, available
            FROM books
            WHERE book_id = ?
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:

            print("Book is not found")
            return

        # ---------------- CHECK AVAILABILITY ----------------

        if book[1] <= 0:

            print("Book is currently unavailable")
            return

        # ---------------- CHECK MEMBER ----------------

        cursor.execute("""
            SELECT name
            FROM members
            WHERE member_id = ?
        """, (member_id,))

        member = cursor.fetchone()

        if member is None:

            print("Member is not found")
            return

        # ---------------- ISSUE DATE ----------------

        issue_date = date.today().isoformat()

        # ---------------- INSERT ISSUE RECORD ----------------

        cursor.execute("""
            INSERT INTO issued_books(
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

        # Reduce available quantity

        cursor.execute("""
            UPDATE books
            SET available = available - 1
            WHERE book_id = ?
        """, (book_id,))

        conn.commit()

        print("Book issued successfully")

        print(f"Book       : {book[0]}")
        print(f"Member     : {member[0]}")
        print(f"Issue Date : {issue_date}")

    # ========================================================
    # VIEW ISSUED BOOKS
    # ========================================================

    @staticmethod
    def view_issued_books():

        cursor.execute("""
            SELECT
                issue_id,
                book_id,
                member_id,
                issue_date,
                status
            FROM issued_books
            WHERE status = 'Issued'
            ORDER BY issue_date DESC
        """)

        issued_books = cursor.fetchall()

        if len(issued_books) == 0:

            print("No books are currently issued")

        else:

            print("=========== ISSUED BOOKS ===========")

            for book in issued_books:

                print(f"""
Issue ID   : {book[0]}
Book ID    : {book[1]}
Member ID  : {book[2]}
Issue Date : {book[3]}
Status     : {book[4]}
--------------------------------------
""")

    # ========================================================
    # RETURN BOOK
    # ========================================================

    @staticmethod
    def return_book():

        try:

            issue_id = int(input("Enter the issue ID: "))

        except ValueError:

            print("Invalid Issue ID")
            print("Please enter a number")
            return

        # ---------------- FIND ISSUE RECORD ----------------

        cursor.execute("""
            SELECT
                book_id,
                member_id,
                status
            FROM issued_books
            WHERE issue_id = ?
        """, (issue_id,))

        record = cursor.fetchone()

        if record is None:

            print("Issue record is not found")
            return

        book_id = record[0]
        member_id = record[1]
        status = record[2]

        # ---------------- CHECK STATUS ----------------

        if status == "Returned":

            print("This book has already been returned")
            return

        # ---------------- RETURN DATE ----------------

        return_date = date.today().isoformat()

        # ---------------- UPDATE ISSUE RECORD ----------------

        cursor.execute("""
            UPDATE issued_books
            SET
                return_date = ?,
                status = 'Returned'
            WHERE issue_id = ?
        """, (
            return_date,
            issue_id
        ))

        # Increase available quantity

        cursor.execute("""
            UPDATE books
            SET available = available + 1
            WHERE book_id = ?
        """, (book_id,))

        conn.commit()

        print("Book returned successfully")

        print(f"Book ID     : {book_id}")
        print(f"Member ID   : {member_id}")
        print(f"Return Date : {return_date}")

    # ========================================================
    # VIEW RETURNED BOOKS
    # ========================================================

    @staticmethod
    def view_returned_books():

        cursor.execute("""
            SELECT
                issue_id,
                book_id,
                member_id,
                issue_date,
                return_date,
                status
            FROM issued_books
            WHERE status = 'Returned'
            ORDER BY return_date DESC
        """)

        returned_books = cursor.fetchall()

        if len(returned_books) == 0:

            print("No returned books found")

        else:

            print("=========== RETURNED BOOKS ===========")

            for book in returned_books:

                print(f"""
Issue ID    : {book[0]}
Book ID     : {book[1]}
Member ID   : {book[2]}
Issue Date  : {book[3]}
Return Date : {book[4]}
Status      : {book[5]}
---------------------------------------
""")

    # ========================================================
    # MEMBER BORROWING HISTORY
    # ========================================================

    @staticmethod
    def member_history():

        try:

            member_id = int(input("Enter the member ID: "))

        except ValueError:

            print("Invalid Member ID")
            print("Please enter a number")
            return

        # Check member

        cursor.execute("""
            SELECT name
            FROM members
            WHERE member_id = ?
        """, (member_id,))

        member = cursor.fetchone()

        if member is None:

            print("Member is not found")
            return

        # Get borrowing history

        cursor.execute("""
            SELECT
                issue_id,
                book_id,
                issue_date,
                return_date,
                status
            FROM issued_books
            WHERE member_id = ?
            ORDER BY issue_date DESC
        """, (member_id,))

        history = cursor.fetchall()

        if len(history) == 0:

            print("No borrowing history found for this member")

        else:

            print("=========== MEMBER BORROWING HISTORY ===========")

            print(f"Member ID   : {member_id}")
            print(f"Member Name : {member[0]}")

            for record in history:

                print(f"""
Issue ID    : {record[0]}
Book ID     : {record[1]}
Issue Date  : {record[2]}
Return Date : {record[3]}
Status      : {record[4]}
----------------------------------------------
""")

    # ========================================================
    # DASHBOARD
    # ========================================================

    @staticmethod
    def dashboard():

        # Total book titles

        cursor.execute("""
            SELECT COUNT(*)
            FROM books
        """)

        total_books = cursor.fetchone()[0]

        # Total physical copies

        cursor.execute("""
            SELECT SUM(quantity)
            FROM books
        """)

        total_copies = cursor.fetchone()[0] or 0

        # Available copies

        cursor.execute("""
            SELECT SUM(available)
            FROM books
        """)

        available_copies = cursor.fetchone()[0] or 0

        # Currently issued

        cursor.execute("""
            SELECT COUNT(*)
            FROM issued_books
            WHERE status = 'Issued'
        """)

        issued_books = cursor.fetchone()[0]

        # Returned books

        cursor.execute("""
            SELECT COUNT(*)
            FROM issued_books
            WHERE status = 'Returned'
        """)

        returned_books = cursor.fetchone()[0]

        # Total transactions

        cursor.execute("""
            SELECT COUNT(*)
            FROM issued_books
        """)

        total_transactions = cursor.fetchone()[0]

        # ---------------- DISPLAY DASHBOARD ----------------

        print("""
========================================
          LIBRARY DASHBOARD
========================================
""")

        print(f"Total Book Titles : {total_books}")
        print(f"Total Copies      : {total_copies}")
        print(f"Available Copies  : {available_copies}")
        print(f"Currently Issued  : {issued_books}")
        print(f"Returned Books    : {returned_books}")
        print(f"Total Transactions: {total_transactions}")

        print("""
========================================
""")

    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    @staticmethod
    def login():

        attempts = 5

        while attempts > 0:

            print("""
========================================
             ADMIN LOGIN
========================================
""")

            username = input("Username : ")
            password = input("Password : ")

            if username == USERNAME and password == PASSWORD:

                print("Login is successful")
                print("Welcome Admin")

                return True

            else:

                attempts -= 1

                print("Invalid Username or Password")

                if attempts > 0:

                    print(
                        f"Remaining attempts : {attempts}"
                    )

        print("Your attempts exceeded the maximum limit")

        return False


# ============================================================
# MAIN MENU
# ============================================================

if Book.login():

    while True:

        print("""
========================================
       LIBRARY MANAGEMENT SYSTEM
========================================

1. Add Book
2. View Books
3. Search Book by ID
4. Update Book
5. Delete Book
6. Issue Book
7. View Issued Books
8. Return Book
9. View Returned Books
10. Member Borrowing History
11. Dashboard
12. Exit

========================================
""")

        choice = input("Enter the choice: ").strip()

        # ---------------- ADD BOOK ----------------

        if choice == "1":

            print("=========== ADD BOOK ===========")

            Book.add_book()

        # ---------------- VIEW BOOKS ----------------

        elif choice == "2":

            Book.display_books()

        # ---------------- SEARCH BOOK ----------------

        elif choice == "3":

            Book.search_by_id()

        # ---------------- UPDATE BOOK ----------------

        elif choice == "4":

            Book.update_book()

        # ---------------- DELETE BOOK ----------------

        elif choice == "5":

            Book.delete_book()

        # ---------------- ISSUE BOOK ----------------

        elif choice == "6":

            Book.issue_book()

        # ---------------- VIEW ISSUED BOOKS ----------------

        elif choice == "7":

            Book.view_issued_books()

        # ---------------- RETURN BOOK ----------------

        elif choice == "8":

            Book.return_book()

        # ---------------- VIEW RETURNED BOOKS ----------------

        elif choice == "9":

            Book.view_returned_books()

        # ---------------- MEMBER HISTORY ----------------

        elif choice == "10":

            Book.member_history()

        # ---------------- DASHBOARD ----------------

        elif choice == "11":

            Book.dashboard()

        # ---------------- EXIT ----------------

        elif choice == "12":

            print("""
Thank you for using the
Library Management System!
""")

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("Database is closed successfully")