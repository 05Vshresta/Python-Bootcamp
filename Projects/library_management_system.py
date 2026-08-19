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

#=============== Search book ===========================================
def search_book():
    book_id = int(input("Enter book id: "))

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

#=============================== Update Book ===========================================
def update_book():
    book_id = int(input("Enter book id: "))

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

#==================== Delete Book =======================================
def delete_book():
    book_id = int(input("Enter book id: "))

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