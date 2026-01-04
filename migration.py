import mysql.connector

def run_migration():
    try:
        # Connect to MySQL Server (no DB yet)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # change if needed
            password="Dev@123321" # change if needed
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        cursor.execute("USE library")

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        )
        """)

        # Create book table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            book_name VARCHAR(200) NOT NULL,
            book_author VARCHAR(200),
            no_of_copies INT DEFAULT 20,
            price FLOAT,
            available INT DEFAULT 20
        )
        """)

        # Create borrowed_book table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_book (
            borrowed_book_id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            user_id INT NOT NULL,
            borrow_date DATE,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        print("✅ Database migration completed successfully!")

    except mysql.connector.Error as err:
        print("❌ Migration failed:", err)

    finally:
        cursor.close()
        conn.close()
