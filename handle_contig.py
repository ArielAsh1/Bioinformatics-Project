import pandas as pd

def create_contig_df():
    # TODO: file name must be extracted from path. this attribute is not a built-in attribute of the DataFrame.
    csv_file = open('GSM3440855_GU0744_P_filtered_contig_annotations.csv')
    contig_table = pd.read_csv('GSM3440855_GU0744_P_filtered_contig_annotations.csv')
    name = csv_file.name
    sample_number = name[:name.index("_")]
    series_number = "GSE121638"
    # inserts sample and series value to start of df
    contig_table.insert(0, "sample_number", sample_number, True)
    contig_table.insert(0, "series_number", series_number, True)
    col_order = ["sample_number", "series_number", "barcode", "is_cell", "contig_id", "high_confidence", "length", "chain",
                 "v_gene", "d_gene", "j_gene", "c_gene", "full_length", "productive", "cdr3", "cdr3_nt", "reads", "umis",
                 "raw_clonotype_id", "raw_consensus_id"]
    # reindex contig_table according to database column order. missing column in df will be added with Nan values.
    # excess column in df will be removed.
    contig_table = contig_table.reindex(columns=col_order)

    # drops rows with no values, resulting from empty rows at the end of the csv file. inplace=true will result in
    # modifying the df rather than creating a new one.
    contig_table.dropna(how='all', axis=0, inplace=True)

    return contig_table
    # code for inserting a new column with given value
    # df = df.assign(new_column=value).reindex(columns=col_order)


if __name__ == '__main__':
    create_contig_df()