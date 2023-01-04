
import sqlite3


def create_db_test():
    # Connect to the database
    conn = sqlite3.connect('new_database.db')

    # Create a cursor
    cursor = conn.cursor()

    # # Import data from a CSV file
    # with open('import.sql', 'r') as f:
    #     cursor.executescript(f.read())

    # Create a table
    cursor.execute('''CREATE TABLE table1 (series_number TEXT,
      sample_number TEXT,
      clinical_condition TEXT,
      sex TEXT,
      age TEXT, 
      tissue TEXT,
      patient_id TEXT,
      cell_type TEXT,
      smokers TEXT,
      notes TEXT);
    ''')

    # Import data from a CSV file
    with open('GSE114724_metaData10X.csv', 'r') as f:
        cursor.execute(f"DELETE FROM table1")
        cursor.copy_from(f, 'table1', sep=',')


    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == '__main__':
    create_db_test()
