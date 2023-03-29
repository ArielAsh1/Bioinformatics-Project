import sqlite3
import handle_contig
import handle_metadata

# Connect to the database
conn = sqlite3.connect('new_database.db')

# Create a cursor
cursor = conn.cursor()

# creates the skeleton structure of the databases, without the actual data.
# only columns names are created here, so later the actual data can be added to this db.
def create_db_structure():
    # deletes previous existing tables
    # TODO: at the end, reconsider this drop, because we dont want to reload the whole db everytime...
    cursor.execute('''DROP TABLE metadata''')
    cursor.execute('''DROP TABLE experiment_Data''')

    # Create the metadata table
    cursor.execute('''CREATE TABLE metadata (series_number TEXT NOT NULL,
      sample_number TEXT NOT NULL,
      clinical_condition TEXT,
      treatment TEXT,
      sex TEXT,
      age TEXT, 
      tissue TEXT,
      patient_id TEXT,
      cell_type TEXT,
      smokers TEXT,
      notes TEXT,
      patient_id_unique TEXT,
      primary key (series_number, sample_number));
    ''')

    # Create the experiment_Data table
    cursor.execute('''CREATE TABLE experiment_Data (record_id INTEGER NOT NULL,
      series_number TEXT NOT NULL,
      sample_number TEXT NOT NULL,
      barcode TEXT,
      is_cell TEXT,
      contig_id TEXT,
      high_confidence TEXT,
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
      barcode_unique TEXT,
      primary key (record_id, series_number, sample_number)
      FOREIGN KEY(series_number) REFERENCES metadata(series_number) 
      ON DELETE CASCADE
      ON UPDATE CASCADE,
      FOREIGN KEY(sample_number) REFERENCES metadata(sample_number)
      ON DELETE CASCADE
      ON UPDATE CASCADE );
    ''')


def append_contig(contig_df):
    # TODO: add try and catch
    try:
        contig_df.to_sql("experiment_Data", conn, if_exists="append", index=False)
        # Commit the changes to the database
        # conn.commit()

    except Exception as e:
        print("Error occurred while inserting data: ", e)
        raise e


if __name__ == '__main__':
    cursor.execute('''DROP TABLE table1''')
    # create_db_structure()
    # todel = input("delete?\n")
    # if todel == 'y':
    #     cursor.execute("DELETE FROM metadata")
    #     cursor.execute("DELETE FROM experiment_Data")
    # parent_dir = '.'
    # handle_metadata.load_metaData_files(parent_dir, conn)
    # handle_contig.load_contig_files(parent_dir, conn)
    # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()
