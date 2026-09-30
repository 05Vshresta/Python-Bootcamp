import sqlite3

# Connect to database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

# Create issue table
cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    student_name TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id)
)
""")

conn.commit()


# Add a new book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    quantity = int(input("Enter quantity: "))

    cursor.execute(
        "INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
        (title, author, quantity)
    )

    conn.commit()
    print("Book added successfully.")


# View all books
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if not books:
        print("No books available.")
        return

    print("\nID | Title | Author | Quantity")
    print("-" * 40)

    for book in books:
        print(book)


# Search book
def search_book():
    title = input("Enter book title to search: ")

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ('%' + title + '%',)
    )

    books = cursor.fetchall()

    if not books:
        print("Book not found.")
        return

    for book in books:
        print(book)


# Issue a book
def issue_book():
    book_id = int(input("Enter book ID: "))

    cursor.execute(
        "SELECT title, quantity FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        return

    if book[1] <= 0:
        print("Book is not available.")
        return

    student_name = input("Enter student name: ")

    cursor.execute(
        "INSERT INTO issued_books (book_id, student_name) VALUES (?, ?)",
        (book_id, student_name)
    )

    cursor.execute(
        "UPDATE books SET quantity = quantity - 1 WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    print("Book issued successfully.")


# Return a book
def return_book():
    issue_id = int(input("Enter issue ID: "))

    cursor.execute(
        "SELECT book_id FROM issued_books WHERE issue_id = ?",
        (issue_id,)
    )

    record = cursor.fetchone()

    if record is None:
        print("Issue record not found.")
        return

    book_id = record[0]

    cursor.execute(
        "UPDATE books SET quantity = quantity + 1 WHERE id = ?",
        (book_id,)
    )

    cursor.execute(
        "DELETE FROM issued_books WHERE issue_id = ?",
        (issue_id,)
    )

    conn.commit()
    print("Book returned successfully.")


# Delete a book
def delete_book():
    book_id = int(input("Enter book ID: "))

    cursor.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        return

    cursor.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    print("Book deleted successfully.")


# Main menu
while True:

    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Delete Book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            issue_book()

        elif choice == "5":
            return_book()

        elif choice == "6":
            delete_book()

        elif choice == "7":
            print("Thank you for using Library Management System.")
            break

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Please enter a valid number.")


# Close database connection
conn.close()