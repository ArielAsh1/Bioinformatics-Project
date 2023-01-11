
import sqlite3


def create_db_test():
    # Connect to the database
    conn = sqlite3.connect('new_database.db')

    # Create a cursor
    cursor = conn.cursor()

    # # Import data from a CSV file
    # with open('import.sql', 'r') as f:
    #     cursor.executescript(f.read())
    # cursor.execute('''DROP TABLE metadata''')
    #cursor.execute('''DROP TABLE experiment_Data''')


    # Create a table
    cursor.execute('''CREATE TABLE metadata (series_number TEXT NOT NULL,
      sample_number TEXT NOT NULL,
      clinical_condition TEXT,
      sex TEXT,
      age TEXT, 
      tissue TEXT,
      patient_id TEXT,
      cell_type TEXT,
      smokers TEXT,
      notes TEXT,
      primary key (series_number, sample_number));
    ''')


    cursor.execute('''CREATE TABLE experiment_Data (series_number TEXT NOT NULL,
      sample_number TEXT NOT NULL,
      is_cell TEXT,
      contig_id TEXT,
      length INTEGER CHECK(length > 0),
      chain TEXT,
      v_gene TEXT,
      d_gene TEXT,
      j_gene TEXT,
      c_gene TEXT,
      full_length TEXT,
      productive TEXT,
      cdr3 TEXT,
      cdr3_nt TEXT,
      reads INTEGER CHECK(reads > 0),
      umis INTEGER CHECK (umis > 0),
      raw_clonotype_id TEXT,
      raw_consensus_id TEXT,
      primary key (series_number, sample_number)
      FOREIGN KEY(series_number) REFERENCES metadata(series_number) 
      ON DELETE CASCADE
      ON UPDATE CASCADE,
      FOREIGN KEY(sample_number) REFERENCES metadata(sample_number)
      ON DELETE CASCADE
      ON UPDATE CASCADE );
    ''')


    # # Import data from a CSV file
    # with open('GSE114724_metaData10X.csv', 'r') as f:
    #     cursor.execute(f"DELETE FROM table1")
    #     cursor.copy_from(f, 'table1', sep=',')


    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == '__main__':
    create_db_test()
