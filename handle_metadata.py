import os
import pandas as pd


# creates the metadata database, using all metadata files from 'metadatas_csv_from_mobax' dir
def create_metadata_db(conn):
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


# should allow adding data from metadata table
def add_data():
    pass


# should allow removing data from metadata table
def remove_data():
    pass


# should allow changing data from metadata table - rethink about this one if it's really needed
def change_data():
    pass

