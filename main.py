import sqlite3
import re
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
    # Get the count of lymph node samples
    cursor.execute("""
        SELECT COUNT(DISTINCT sample_number)
        FROM metadata
        WHERE LOWER(tissue) LIKE '%lymph node%'
    """)
    lymph_node_count = cursor.fetchone()[0]

    # Get the count of tumor samples
    cursor.execute("""
        SELECT COUNT(DISTINCT sample_number)
        FROM metadata
        WHERE LOWER(tissue) LIKE '%tumor%'
    """)
    tumor_count = cursor.fetchone()[0]

    # Get the v_genes and their percentages in lymph node samples
    cursor.execute("""
        SELECT v_gene, (COUNT(*) * 100.0 / ?) AS percentage
        FROM experiment_Data
        WHERE sample_number IN (
            SELECT sample_number
            FROM metadata
            WHERE LOWER(tissue) LIKE '%lymph node%'
        )
        GROUP BY v_gene
    """, (lymph_node_count,))  # Pass lymph_node_count as a parameter

    lymph_node_results = cursor.fetchall()

    # Get the v_genes and their percentages in tumor samples
    cursor.execute("""
        SELECT v_gene, (COUNT(*) * 100.0 / ?) AS percentage
        FROM experiment_Data
        WHERE sample_number IN (
            SELECT sample_number
            FROM metadata
            WHERE LOWER(tissue) LIKE '%tumor%'
        )
        GROUP BY v_gene
    """, (tumor_count,))  # Pass tumor_count as a parameter

    tumor_results = cursor.fetchall()

    # Create sets of v_genes for lymph node and tumor samples
    lymph_node_genes = set(result[0] for result in lymph_node_results)
    tumor_genes = set(result[0] for result in tumor_results)

    # Find the common v_genes in both lymph node and tumor samples
    common_genes = lymph_node_genes.intersection(tumor_genes)

    # Find the unique v_genes in lymph node and tumor samples
    unique_lymph_node_genes = lymph_node_genes - common_genes
    unique_tumor_genes = tumor_genes - common_genes

    # Compare the v_gene variety based on the common genes
    lymph_node_variety = len(common_genes)
    tumor_variety = len(common_genes)

    if lymph_node_variety > tumor_variety:
        print("There is a greater variety of common v_genes in lymph node samples compared to tumor samples.")
    elif lymph_node_variety < tumor_variety:
        print("There is a greater variety of common v_genes in tumor samples compared to lymph node samples.")
    else:
        print("The variety of common v_genes is the same between lymph node and tumor samples.")

    # Compare the v_gene percentages for each common gene
    for gene in common_genes:
        lymph_node_percentage = next(result[1] for result in lymph_node_results if result[0] == gene)
        tumor_percentage = next(result[1] for result in tumor_results if result[0] == gene)

        if lymph_node_percentage > tumor_percentage:
            print(f"The v_gene {gene} has a higher percentage in lymph node samples.")
        elif lymph_node_percentage < tumor_percentage:
            print(f"The v_gene {gene} has a higher percentage in tumor samples.")
        else:
            print(f"The v_gene {gene} has the same percentage in lymph node and tumor samples.")

    # Print the unique v_genes in lymph node samples
    print("Unique v_genes in lymph node samples:")
    for gene in unique_lymph_node_genes:
        print(gene)

    # Print the unique v_genes in tumor samples
    print("Unique v_genes in tumor samples:")
    for gene, percent in unique_tumor_genes:
        print(gene)
    # Close the connection
    conn.close()
