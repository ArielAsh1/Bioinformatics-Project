import os
import sqlite3
import pandas as pd
import handle_contig

# Connect to the database
conn = sqlite3.connect('new_database.db')

# Create a cursor
cursor = conn.cursor()


def create_db_test():
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
      primary key (record_id, series_number, sample_number)
      FOREIGN KEY(series_number) REFERENCES metadata(series_number) 
      ON DELETE CASCADE
      ON UPDATE CASCADE,
      FOREIGN KEY(sample_number) REFERENCES metadata(sample_number)
      ON DELETE CASCADE
      ON UPDATE CASCADE );
    ''')

def append_meta():
    # Loop through all the CSV files in the directory and appends their content to growing metadata db
    # for each CSV file, only the content (without column names) is added.
    # the column names appear only once, at the top of metadata database
    for file_name in os.listdir('metadatas_csv_from_mobax'):
        if file_name.endswith('.csv'):

            # Read the CSV file into a DataFrame
            metadata_df = pd.read_csv(os.path.join('metadatas_csv_from_mobax', file_name))

            # rename all column names, so whitespace " " will be replaced with underscore "_"
            # e.g: change 'series number' to 'series_number' so it matches with the column in our metadata db
            metadata_df.rename(columns={'series number': 'series_number'}, inplace=True)
            metadata_df.rename(columns={'sample number': 'sample_number'}, inplace=True)
            metadata_df.rename(columns={'clinical condition': 'clinical_condition'}, inplace=True)
            metadata_df.rename(columns={'patient id': 'patient_id'}, inplace=True)
            metadata_df.rename(columns={'cell type': 'cell_type'}, inplace=True)

            # if a line is empty (all NULL) so don't append it to metadata db
            metadata_df.dropna(how='all', axis=0, inplace=True)

            # Insert the data into the metadata table
            metadata_df.to_sql("metadata", conn, if_exists="append", index=False)

    # # Create an index on the foreign key columns
    # cursor.execute('''CREATE INDEX series_contig_fk1 ON experiment_Data(series_number)''')
    # cursor.execute('''CREATE INDEX sample_contig_fk2 ON experiment_Data(sample_number)''')

    ## a test to check that it added the data to 'metadata' db
    # metadata_df_from_db = pd.read_sql_query("SELECT * from metadata", conn)
    # print(metadata_df_from_db)


def append_contig(contig_df):
    contig_df.to_sql("experiment_Data", conn, if_exists="append", index=False)


if __name__ == '__main__':
    create_db_test()
    contig_df = handle_contig.create_contig_df()
    append_contig(contig_df)
    append_meta()
    # contig_df_from_db = pd.read_sql_query("SELECT * from experiment_data", conn)
    # print(contig_df_from_db)
    test_df = pd.read_sql_query("SELECT metadata.sample_number FROM metadata, experiment_data "
                                "WHERE metadata.series_number = experiment_data.series_number AND metadata.sample_number = experiment_data.sample_number", conn)
    # Commit the transaction
    print(test_df)
    conn.commit()
    # Close the connection
    conn.close()
