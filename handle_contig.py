import pandas as pd

def create_contig_df():
    # TODO: file name must be extracted from path. this attribute is not a built-in attribute of the DataFrame.
    csv_file = open('GSM3148584_BC11_TUMOR2_filtered_contig_annotations.csv')
    contig_table = pd.read_csv('GSM3148584_BC11_TUMOR2_filtered_contig_annotations.csv')
    name = csv_file.name
    sample_number = name[:name.index("_")]
    series_number = "GSM3148584"
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
    # true will result in
    # modifying the df rather than creating a new one.
    contig_table.dropna(how='all', axis=0, inplace=True)

    return contig_table
    # code for inserting a new column with given value
    # df = df.assign(new_column=value).reindex(columns=col_order)


if __name__ == '__main__':
    create_contig_df()


"""
def create_db_test():
    # # Import data from a CSV file
    # with open('import.sql', 'r') as f:
    #     cursor.executescript(f.read())
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

    # # Create an index on the foreign key columns
    # cursor.execute('''CREATE INDEX series_contig_fk1 ON experiment_Data(series_number)''')
    # cursor.execute('''CREATE INDEX sample_contig_fk2 ON experiment_Data(sample_number)''')
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
"""