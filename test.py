import pandas as pd

csv_file = open('GSM3148584_BC11_TUMOR2_filtered_contig_annotations.csv')
name = csv_file.name
name = name[:name.index("_")]
print (name)
