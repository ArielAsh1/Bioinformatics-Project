import os
import pandas as pd


def fill_metadata_db(conn):
    """ fills the metadata database with all the metadata files from 'metadatas_csv_from_mobax' dir.
        Loops through all the CSV files in the directory and appends their content to growing metadata db.
        for each CSV file, only the content (without column names) is added.
        the column names appear only once, at the top of metadata database """
    for metadata_file in os.listdir('metadatas_csv_from_mobax'):
        if metadata_file.endswith('.csv'):
            # Read the CSV file into a DataFrame
            metadata_df = pd.read_csv(os.path.join('metadatas_csv_from_mobax', metadata_file))

            # adjust the current dataframe before adding it to the metadata database
            adjust_data(metadata_df)

            # add the current dataframe to the metadata database
            add_data(metadata_df, conn)


# TODO? add an option to directly add adjusted new files that aren't stored in the metadata dir (for future usage)
#
def add_data(metadata_df, conn):
    """ adding the current dataframe to the metadata database. """
    # Insert the data into the metadata database
    metadata_df.to_sql("metadata", conn, if_exists="append", index=False)


def adjust_data(metadata_df):
    """ adjusts the current dataframe, so it's fits the metadata database before adding it.
        rename all column names, so whitespace " " will be replaced with underscore "_" to fit db structure.
        e.g: change 'series number' to 'series_number' so it matches with the column name in our metadata db.
    """
    metadata_df.rename(columns={'series number': 'series_number'}, inplace=True)
    metadata_df.rename(columns={'sample number': 'sample_number'}, inplace=True)
    metadata_df.rename(columns={'clinical condition': 'clinical_condition'}, inplace=True)
    metadata_df.rename(columns={'patient id': 'patient_id'}, inplace=True)
    metadata_df.rename(columns={'cell type': 'cell_type'}, inplace=True)

    # if a line is empty (all NULL) so remove it
    metadata_df.dropna(how='all', axis=0, inplace=True)


# TODO? should allow removing data from metadata table
def remove_data():
    pass


# should allow changing data from metadata table - rethink about this one if it's really needed
def change_data():
    pass

