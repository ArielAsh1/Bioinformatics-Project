
import sqlite3


def create_db_test():
    # Connect to the database
    conn = sqlite3.connect('new_database.db')

    # Create a cursor
    cursor = conn.cursor()

    # Import data from a CSV file
    with open('import.sql', 'r') as f:
        cursor.executescript(f.read())

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == '__main__':
    create_db_test()
