import os
import pandas as pd
import sqlite3

# Connect to the database
conn = sqlite3.connect('new_database.db')

# Create a cursor
cursor = conn.cursor()


def append_contig(contig_df):
    # TODO: add try and catch
    try:
        contig_df.to_sql("experiment_Data", conn, if_exists="append", index=False)
        # Commit the changes to the database
        # conn.commit()

    except Exception as e:
        print("Error occurred while inserting data: ", e)
        raise e


def load_contig_files(parent_directory):
    files_counter = 0
    # Loop through each folder in the parent directory
    for folder in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder)
        # I assume folder name is the METADATA serial number.
        folder_name = os.path.basename(folder_path)
        # Check if the item in the parent directory is a folder
        # TODO: currently, all relevant folder start with GSE (code for metadata). should consider the possibility of
        #  different name for the folder!
        if os.path.isdir(folder_path):
            # Get a list of all the contig.csv files in the folder
            csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
                         file.endswith('.csv') and 'contig' in file]
            # Loop through each CSV file and load it into a Pandas dataframe
            df_list = [] # only for testing
            for file in csv_files:
                print (f"working on {file}, from {folder_name}")
                contig_df = create_contig_df(file, folder_name)
                df_list.append(contig_df)
                files_counter += 1
                # TODO: insert df to database. main.append_contig(contig_df)
                try:
                    append_contig(contig_df)
                    print(f"succesfully inserted {file} to db")
                except Exception as e:
                    print(f"Failed to insert data from {file}: {e}")

    print(f"worked on total of {files_counter} contig files")


def check_column(df_columns):
    """
    function will check if column names of input file are the same as instructed by the database.
    NOTICE: files does not contain "record_id", "sample_number", "series_number" column at this stage, for we add them
    manually later on.
    :param df_columns: list of input contig file columns
    :return: boolean variable indicating if columns are the same as they should, and a list containing the illegal
    names (can be empty if none are).
    """
    exp_columns = ["barcode", "is_cell", "contig_id", "high_confidence", "length", "chain", "v_gene",
                 "d_gene", "j_gene", "c_gene", "full_length", "productive", "cdr3", "cdr3_nt", "reads", "umis",
                 "raw_clonotype_id", "raw_consensus_id"]
    missing_columns = []
    for col in df_columns:
        if col not in exp_columns:
            missing_columns.append(col)
    if missing_columns:
        return False, missing_columns
    else:
        return True, missing_columns


def create_contig_df(csv_file, metadata_number):
    # TODO: file name must be extracted from path. this attribute is not a built-in attribute of the DataFrame.
    contig_table = pd.read_csv(csv_file)
    # TODO: varify name has "filtered_contig_annotations" to make sure its the correct file
    filename = os.path.basename(csv_file)
    is_legal_columns, missing_columns = check_column(contig_table.columns)
    if not is_legal_columns:
        raise Exception(f"{filename} contains illegal columns: {missing_columns}")
    sample_number = filename[:filename.index("_")]
    # TODO: load_contig_files function should also send the metadata name.
    series_number = metadata_number
    # inserts sample and series value to start of df
    contig_table.insert(0, "sample_number", sample_number, True)
    contig_table.insert(0, "series_number", series_number, True)
    contig_table['record_id'] = range(1, len(contig_table) + 1)
    col_order = ["record_id", "sample_number", "series_number", "barcode", "is_cell", "contig_id", "high_confidence", "length", "chain",
                 "v_gene", "d_gene", "j_gene", "c_gene", "full_length", "productive", "cdr3", "cdr3_nt", "reads", "umis",
                 "raw_clonotype_id", "raw_consensus_id"]
    # reindex contig_table according to database column order. missing column in df will be added with Nan values.
    # excess column in df will be removed.
    contig_table = contig_table.reindex(columns=col_order)

    # drops rows with no values, resulting from empty rows at the end of the csv file. setting inplace to
    # true will result in modifying the df rather than creating a new one.
    contig_table.dropna(how='all', axis=0, inplace=True)

    return contig_table
    # code for inserting a new column with given value
    # df = df.assign(new_column=value).reindex(columns=col_order)


if __name__ == '__main__':
    # Set the path to the parent directory containing the folders
    todel = input("delete?\n")
    if todel == 'y':
        cursor.execute("DELETE FROM experiment_Data")
    else:
        parent_dir = '..'
        load_contig_files(parent_dir)
    # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()



