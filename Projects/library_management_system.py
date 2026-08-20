import sqlite3
import re

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

# Add the available quantity column if it doesn't exist (for schema evolution)
try:
    cursor.execute("ALTER TABLE books ADD COLUMN available INTEGER DEFAULT 0")
    conn.commit()
    print("Added 'available' column to books table (if it was missing).")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("'available' column already exists.")
    else:
        raise # Re-raise other operational errors

#===================Book class=========================
class Book:
    def __init__(self, title, author, category, quantity):
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
      
    #============TITLE VALIDATION FUNCTIONS ========================
    @staticmethod
    def validate_title(title):

        if title.strip() == "":
            print("Title cannot be empty")
            return False

        if not re.fullmatch(r"[A-Za-z0-9\s:,'!?&.+-]+", title):
            print("Title should contain only letters, numbers, spaces and basic punctuation")
            return False

        if len(title.strip()) < 2:
            print("Title should be at least 2 characters long")
            return False

        return True

    #=========== AUTHOR VALIDATION FUNCTIONS ========================
    @staticmethod
    def validate_author(author):
        if author.strip() == "":
            print("Author name cannot be empty")
            return False

        if not re.fullmatch(r"[A-Za-z\s]+", author):
            print("Author name should contain only letters and spaces")
            return False

        if len(author.strip()) < 2:
            print("Author name should be at least 2 characters long")
            return False

        return True

    #=========== CATEGORY VALIDATION FUNCTIONS ========================
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

    #========== QUANTITY VALIDATION FUNCTIONS ========================
    @staticmethod       
    def validate_quantity(quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            print("Quantity should be a positive integer")
            return False

        return True

# ============ ADD BOOK ====================================
def add_book():
    #============= TITLE VALIDATION =========================
    while True:
        title = input("Enter book title: ")
        if Book.validate_title(title):
            break
    #================Author validation============================
    while True:
        author = input("Enter author name: ")
        if Book.validate_author(author): 
            break
    #================Category validation===========================
    while True:
        category = input("Enter category: ")
        if Book.validate_category(category):
            break
    #==================== quantity validation===========================
    while True:
        quantity = input("Enter quantity: ")
        if Book.validate_quantity(quantity):
            quantity = int(quantity)
            break
    # Quantity Validation
    while True:
        try:
            quantity = int(input("Enter quantity: "))

            if Book.validate_quantity(quantity):
                break

        except ValueError:
            print("Quantity should be a valid integer")

    # Duplicate Book Check
    cursor.execute("SELECT * FROM books WHERE title = ? AND author = ?",(title.strip(), author.strip()))

    if cursor.fetchone()[0]:
        print("This book is already registered")
        return

    # Insert Book
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
        title.strip(),
        author.strip(),
        category.strip(),
        quantity,
        quantity
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

#=============== SEARCH BOOK ===========================================
def search_book():
    try:
        book_id = int(input("Enter book id: "))
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        return

    cursor.execute("""SELECT * FROM books
    WHERE book_id = ?""",(book_id,)
    )
    book = cursor.fetchone()
    
    if book:
        print("=========BOOKS Details=========")
    
        print(f"""
            Book ID: {book[0]}
            Title: {book[1]}
            Author: {book[2]}
            Category: {book[3]}
            Quantity: {book[4]}
            Available: {book[5]}
        """)
    else:
        print("Book is not found")

#=============================== UPDATE BOOK ===========================================
def update_book():
    try:
        book_id = int(input("Enter book id: "))
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        return

    cursor.execute("""SELECT * FROM books
    WHERE book_id = ?""",(book_id,)
    )
    book = cursor.fetchone()

    if book:
        print("=========BOOKS Details=========")
    
        print(f"""
            Book ID: {book[0]}
            Title: {book[1]}
            Author: {book[2]}
            Category: {book[3]}
            Quantity: {book[4]}
            Available: {book[5]}
        """)
        print("----------------------------------------")
        print("Update Book Details")
        print("----------------------------------------")
        Title = input("Enter new title: ")
        Author = input("Enter new author: ")
        Category = input("Enter new category: ")
        Quantity = int(input("Enter new quantity: "))

        cursor.execute("""
        UPDATE books
        SET 
            title = ?,
            author = ?,
            category = ?,
            quantity = ?,
            available = ?
        WHERE book_id = ?""",
        (Title, Author, Category, Quantity, Quantity, book_id))
        conn.commit()
        
        print("Book details updated successfully")
    else:
        print("Book is not found")

#==================== DELETE BOOK =======================================
def delete_book():
    try:
        book_id = int(input("Enter book id: "))
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        return

    cursor.execute("""SELECT * FROM books
    WHERE book_id = ?""",(book_id,)
    )
    book = cursor.fetchone()

    if book:
        print("=========BOOKS Details=========")
        print(f"""
            Book ID: {book[0]}
            Title: {book[1]}
            Author: {book[2]}
            Category: {book[3]}
            Quantity: {book[4]}
            Available: {book[5]}
            """)
        confirm = input("Are you sure you want to delete this book? (y/n): ").upper()
        if confirm == "Y":
            cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            conn.commit()
            print("Book deleted successfully")
        else:
            print("Book deletion cancelled")
    else:
        print("Book is not found")
        

# ============ MAIN MENU ===================================
while True:
    print("\n1. Add Book")
    print("2. View Books")
    print("3. Search by ID")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Exit")

    choice = input("Enter your choice: ")

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
        print("Thank you for visiting!")
        conn.close()
        break

    else:
        print("Invalid choice")