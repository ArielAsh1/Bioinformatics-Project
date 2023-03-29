import os
import pandas as pd
import hashlib



def add_contig_todb(contig_df, conn):
    # TODO: add try and catch
    try:
        contig_df.to_sql("experiment_Data", conn, if_exists="append", index=False)
        # Commit the changes to the database
        # conn.commit()

    except Exception as e:
        print("Error occurred while inserting data: ", e)
        raise e


def load_contig_files(parent_directory, conn):
    files_counter = 0
    # Loop through each folder in the parent directory
    failed_files = []
    for folder in os.listdir(parent_directory):
        folder_path = os.path.join(parent_directory, folder)
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
            for file in csv_files:
                try:
                    print(f"working on {file}, from {folder_name}")
                    contig_df = adjust_contig(file, folder_name)
                    files_counter += 1
                    add_contig_todb(contig_df, conn)
                    print(f"succesfully inserted {file} to db")
                except Exception as e:
                    failed_files.append(file)
                    print(f"Failed to insert data from {file}: {e}")

    print(f"worked on total of {files_counter} contig files")
    if failed_files:
        print("Failed to insert data from: " + "\n".join(list(map(lambda x: str(x), failed_files))))
        # print(f"failed working on files: {failed_files}")


def check_columns(df_columns):
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


def create_unique_barcode(contig_row):
    barcode = contig_row['barcode']
    sample_number = contig_row['sample_number']
    string_to_hash = f"{barcode}_{sample_number}"
    hash_object = hashlib.sha256(string_to_hash.encode())
    return hash_object.hexdigest()


def adjust_contig(csv_file, metadata_number):
    contig_table = pd.read_csv(csv_file)
    filename = os.path.basename(csv_file)
    is_legal_columns, missing_columns = check_columns(contig_table.columns)
    if not is_legal_columns:
        # missing column will be deleted.
        print(f"NOTICE: {filename} contains illegal columns: {missing_columns}.")
    sample_number = filename[:filename.index("_")]
    # TODO: load_contig_files function should also send the metadata name.
    series_number = metadata_number
    # inserts sample and series value to start of df
    contig_table.insert(0, "sample_number", sample_number, True)
    contig_table.insert(0, "series_number", series_number, True)
    contig_table['record_id'] = range(1, len(contig_table) + 1)
    col_order = ["record_id", "sample_number", "series_number", "barcode", "is_cell", "contig_id", "high_confidence",
                 "length", "chain", "v_gene", "d_gene", "j_gene", "c_gene", "full_length", "productive", "cdr3",
                 "cdr3_nt", "reads", "umis", "raw_clonotype_id", "raw_consensus_id"]
    # reindex contig_table according to database column order. missing column in df will be added with Nan values.
    # excess column in df will be removed.
    contig_table = contig_table.reindex(columns=col_order)
    # drops rows with no values, resulting from empty rows at the end of the csv file. setting inplace to
    # true will result in modifying the df rather than creating a new one.
    contig_table.dropna(how='all', axis=0, inplace=True)
    contig_table['barcode_unique'] = contig_table.apply(create_unique_barcode, axis=1)
    return contig_table


if __name__ == '__main__':
    pass




