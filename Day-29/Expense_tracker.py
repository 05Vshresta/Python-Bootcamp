import sqlite3

conn = sqlite3.connect("expense.db")
cursor = conn.cursor()

# Create a table to store expenses
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
print("Table created successfully.")
conn.commit()

# Add expenses to the database
def add_expenses():
    date = input("Enter the date (DD:MM:YYYY) : ")
    category = input("Enter the category : ")
    amount = float(input("Enter the amount : "))
    description = input("Enter the description : ")

    cursor.execute("""
    INSERT INTO expenses (date, category, amount, description)
    VALUES (?, ?, ?, ?)
    """, (date, category, amount, description))

    conn.commit()
    print("Expense added successfully.")


# View all expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()

    if len(records) == 0:
        print("No expenses found.")
        return

    for record in records:
        print("ID         :", record[0])
        print("Date       :", record[1])
        print("Category   :", record[2])
        print("Amount     :", record[3])
        print("Description:", record[4])
        print("====================================")


# Search expenses by category
def search_expenses():
    category = input("Enter the category : ")
    
    cursor.execute(
        "SELECT * FROM expenses WHERE category = ?",
        (category,)
    )

    records = cursor.fetchall()

    if len(records) == 0:
        print("No Records found.")
    else:
        for record in records:
            print("ID         :", record[0])
            print("Date       :", record[1])
            print("Category   :", record[2])
            print("Amount     :", record[3])
            print("Description:", record[4])
            print("====================================")

        print("Expenses found in category.")


# Update expenses
def update_expenses():
    id = input("Enter the ID of the expense to update : ")

    cursor.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (id,)
    )

    record = cursor.fetchone()

    if record is None:
        print("Expense not found.")
        return

    date = input("Enter the new date (DD:MM:YYYY) : ")
    category = input("Enter the new category : ")
    amount = float(input("Enter the new amount : "))
    description = input("Enter the new description : ")

    cursor.execute("""
    UPDATE expenses
    SET date = ?, category = ?, amount = ?, description = ?
    WHERE id = ?
    """, (date, category, amount, description, id))

    conn.commit()
    print("Expense updated successfully.")
    print("================================")

# Delete expenses
def delete_expenses():
    id = input("Enter the ID of the expense to delete : ")

    cursor.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (id,)
    )

    record = cursor.fetchone()

    if record is None:
        print("Expense not found.")
        return

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (id,)
    )

    conn.commit()
    print("Expense deleted successfully.")
    print("================================")
    

# Total expenses
def total_expenses():
    cursor.execute("SELECT SUM(amount) FROM expenses")

    total = cursor.fetchone()

    if total is None:
        total = 0

    print("Total expenses :", total)
    print("================================")


# Main menu
while True:
    print("\n========== Expense Tracker ==========")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expenses by Category")
    print("4. Update Expense")
    print("5. Delete Expense")
    print("6. Total Expenses")
    print("7. Exit")

    choice = input("Enter your choice : ")

    if choice == "1":
        add_expenses()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        search_expenses()

    elif choice == "4":
        update_expenses()

    elif choice == "5":
        delete_expenses()

    elif choice == "6":
        total_expenses()

    elif choice == "7":
        conn.close()
        print("Database closed successfully.")
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice. Please try again.")
        
conn.close()