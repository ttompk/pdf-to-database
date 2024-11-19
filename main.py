'''
pdf-to-csv
Min objectives:
- Read a PDF file into memory. 
- Extract and format the text from within the file
- Create csv file(s) with the data (artifact)
- Load the data into a postgres database.
'''

from pypdf import PdfReader
import pandas as pd
from datetime import datetime

def read_pdf(file_name: str):
    ''' 
    Utilize pydf library to open pdf files and 'read' the contents.
    file_name:  string. pathway to file
    '''
    reader = PdfReader(file_name)
    print(f'The file has ' + str(len(reader.pages)) + ' pages.')
    return reader

def text_to_list(reader) -> list: 
    '''
    convert text from rader into a list, each item being the text from each page.
    reader:  pypdf.PdfReader object. 
    '''
    contents = []
    for i in range(0,len(reader.pages)):
        contents.append(reader.pages[i].extract_text())
    return contents

# create a dictionary with words to search for
def table_1_search_dict():
    '''
    The search dictionary defines which strings are important for our tables, i.e. the values we 
    want to 'extract' from the PDF file.
    This dictionary is user defined and specified prior to running the program.
    This process is currently embedded in the program but should be extracted away from the logic, using
    some other user friendly notation.

    The dictionary follows this scheme: 
        column_header, search_term, term_position, additional_characters
        - term_position: 0 = the search term precedes the desired text, -1 = the search term follows the desired text
        - replacement characters always dependent on position, 
            - 0 = remove characters after the desired string,
            - -1 = remove characters in front of the desired string 
    '''
    table_type = 'one'   # 
    search_dict = {
        'invoice_date': ['Order Placed: ', 0, ''],
        'invoice_number': ['order number:', 0, ''],
        'company_name': ['order number', -1, ''],
        'invoice_total': ['Grand Total:$', 0, 'Total paid']
        }
    return search_dict, table_type

# create a dictionary with words to search for
def table_2_search_dict():
    '''
    The dictionary follows this scheme: column header, search term, search term position
    # Position: 0 = the search term precedes the desired text, -1 = the search term follows the desired text
    '''
    table_type = 'many'
    search_dict = {
        'product_name': ['1 of:', 0, ''],
        'product_company': ['Sold by:', 0, ''],
        'product_amount': ['New$', 0, '']
        }
    return search_dict, table_type