import sys_pdf
import pdf_functions as pdf
import os

# Move PDF files to working directory
source_dir = "pdf_inbox"
target_dir = "pdf_examples"
sys_pdf.move_pdf_files(source_dir, target_dir)

file_counter = 0

# for filename in target_dir
for file_name in os.listdir(source_dir):
    
    scanned_text = pdf.read_pdf(file_name)

    # add the contents for each page into a list
    contents = pdf.text_to_list(scanned_text)

    # iterate over each page
    by_line = []
    for page in range(0, len(scanned_text.pages)):  # create a flat list of strings
        by_line += contents[page].split('\n')       # remove the line breaks

    # create a dictionary of search terms
    table_1_search, table_1_type = pdf.table_1_search_dict()
    table_2_search, table_2_type = pdf.table_2_search_dict()

    # create tables with pulled data
    table_1 = pdf.one_table(table_1_search, by_line)
    table_2 = pdf.many_table(table_2_search, by_line)  

    # 
    table_1_df = pdf.one_table_df(table_1)
    table_2_df = pdf.many_table_df(table_2)  # verifies that the length of each value list is the same in a many table

    # add a column of invoice numbers for each table_2 entry
    #table_2_df['invoice_number'] = table_1['invoice_number'][0]
    table_2_df.insert(0, 'invoice_number', table_1['invoice_number'][0])

    # format dates to standard YYYY-MM-DD
    formatted_date_str = pdf.format_date(table_1['invoice_date'][0], '%B %d, %Y')  # November 11, 2015
    name_base = table_1['company_name'][0].replace('.', '_') + '_' + formatted_date_str

    pdf.save_as_csv(table_1, table_1_df, name_base, 'overview')
    pdf.save_as_csv(table_1, table_2_df, name_base, 'products')

    file_counter += 1
