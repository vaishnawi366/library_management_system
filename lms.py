import mysql.connector
import migration
from datetime import date

conn = None
cursor = None

def init_db():
    global conn, cursor
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dev@123321",
        database="library"
    )
    cursor = conn.cursor()

# ---------------- AUTHENTICATION ----------------
def signup():
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    try:
        cursor.execute(
            "INSERT INTO users (user_name, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print("✅ Signup successful!")
    except mysql.connector.IntegrityError:
        print("❌ Username already exists. Try a different one.")



def signin():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute(
        "SELECT user_id FROM users WHERE user_name=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()

    if user:
        print("✅ Login successful!")
        return user[0]
    else:
        print("❌ Invalid credentials")
        return None


# ---------------- BOOK FUNCTIONS ----------------
def add_books():
    name = input("Book Name: ")
    author = input("Author Name: ")
    price = float(input("Price: "))
    copies = int(input("Number of copies: "))

    cursor.execute("""
        INSERT INTO book (book_name, book_author, no_of_copies, price, available)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, author, copies, price, copies))

    conn.commit()
    print("📚 Book added successfully!")


def get_books():
    cursor.execute("""
        SELECT book_id, book_name, book_author, price, available
        FROM book
    """)
    books = cursor.fetchall()

    if not books:
        print("\n📭 No books available\n")
        return

    print("\n📚 Available Books")
    print("-" * 70)
    print(f"{'ID':<5} {'Name':<20} {'Author':<20} {'Price':<10} {'Available'}")
    print("-" * 70)

    for book_id, name, author, price, available in books:
        print(f"{book_id:<5} {name:<20} {author:<20} {price:<10} {available}")

    print("-" * 70)


def search_book():
    keyword = input("Enter book name or author: ")

    cursor.execute("""
        SELECT * FROM book
        WHERE book_name LIKE %s OR book_author LIKE %s
    """, (f"%{keyword}%", f"%{keyword}%"))

    books = cursor.fetchall()
    for b in books:
        print(b)


def delete_book():
    book_id = input("Enter Book ID to delete: ")

    cursor.execute("DELETE FROM book WHERE book_id=%s", (book_id,))
    conn.commit()
    print("🗑 Book deleted successfully!")


# ---------------- BORROW & RETURN ----------------
def borrow_book(user_id):
    book_id = input("Enter Book ID to borrow: ")

    cursor.execute("SELECT available FROM book WHERE book_id=%s", (book_id,))
    result = cursor.fetchone()

    if result and result[0] > 0:
        cursor.execute("""
            INSERT INTO borrowed_book (book_id, user_id, borrow_date)
            VALUES (%s, %s, %s)
        """, (book_id, user_id, date.today()))

        cursor.execute("""
            UPDATE book
            SET available = available - 1
            WHERE book_id=%s
        """, (book_id,))

        conn.commit()
        print("📖 Book borrowed successfully!")
    else:
        print("❌ Book not available")


def return_book(user_id):
    book_id = input("Enter Book ID to return: ")

    cursor.execute("""
        SELECT borrowed_book_id FROM borrowed_book
        WHERE book_id=%s AND user_id=%s AND return_date IS NULL
    """, (book_id, user_id))

    record = cursor.fetchone()

    if record:
        cursor.execute("""
            UPDATE borrowed_book
            SET return_date=%s
            WHERE borrowed_book_id=%s
        """, (date.today(), record[0]))

        cursor.execute("""
            UPDATE book
            SET available = available + 1
            WHERE book_id=%s
        """, (book_id,))

        conn.commit()
        print("✅ Book returned successfully!")
    else:
        print("❌ No borrowed record found")


# ---------------- MAIN MENU ----------------
def main_menu(user_id):
    while True:
        print("""
        -------- LIBRARY MANAGEMENT SYSTEM --------
        1. Add Book
        2. View All Books
        3. Search Book
        4. Delete Book
        5. Borrow Book
        6. Return Book
        7. Logout
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            add_books()
        elif choice == "2":
            get_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            borrow_book(user_id)
        elif choice == "6":
            return_book(user_id)
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice")


# ---------------- PROGRAM START ----------------
def login_menu():
    while True:
        print("""
        ===== Library System =====
        1. Signup
        2. Signin
        3. Exit
        """)

        option = input("Enter option: ")

        if option == "1":
            signup()
        elif option == "2":
            user_id = signin()
            if user_id:
                main_menu(user_id)
        elif option == "3":
            break
        else:
            print("❌ Invalid option")

    cursor.close()
    conn.close()


if __name__=="__main__":
    migration.run_migration()
    init_db()
    login_menu()