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
import os

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


def find_string(line, search_str, position, del_chars):
    ''' 
    Search a string for matching text.
    Arguments
    line:   
    search_str:   
    position:   
    del_chars:   

    Returns:   string. 
    '''
    # find character position of matching text
    char_location = line.find(search_str)  # -1 if string not found, positive int otherwise
    
    if char_location >= 0: 
        
        if position == 0:    # desired text follows the search text, ie. 'search wanted delete'
            x = line[char_location + len(search_str) : ]  # grab the characters starting at this point to the end
            if del_chars != '':
                x = x[0 : x.find(del_chars)]
                x = x.strip()  
            return x
        
        elif position == -1:    # desired text precedes the search text, ie. 'delete wanted search'
            x = line[0 : char_location]
            if del_chars != '':
                x = x.replace( del_chars, '')
                x = x.strip()
            return x

    else:
        return None
    
def clean_text(matching_string):
    # remove end white spaces
    clean = matching_string.strip()
    
    # remove special characters
    bad_chars = [';', '!', "*"]
    for i in bad_chars:
        clean = clean.replace(i, '')

    # replace . with _
    #clean = clean.replace('.', '_')

    return clean

def one_table(search_dict, by_line):
    '''This funciton takes in a dictionary of search terms and a list of text strings.
    The function searches over the lists of text and compares to string values. Matching strings are added
    to a dictionary of results.
    Input: 
        
    Returns:   result_dict. dictionary
    '''
    
    # create dictionary to hold results
    result_dict = {}
    
    # iterate over each line
    for line in by_line:
    
        # iterate over dictionary of search terms for each table
        for search_key, value in search_dict.items():
            search_str = value[0]
            position = value[1]
            del_chars = value[2]
            
            # is there a match between the search string and the line?
            # if so return the match
            matching_string = find_string(line, search_str, position, del_chars)
    
            if matching_string != None:
                # clean up the string
                clean_string = clean_text(matching_string)

                # in a one table there is only ever one value per search string
                # add the found text to a dictionary
                # but first determine if there are multiple occurences of the same key
                if search_key not in result_dict.keys():  # new entry
                    result_dict[search_key] = [clean_string]
                else:
                    for i in range(0,50):  # existing key found
                        new_key = search_key+"_"+str(i+2)
                        if new_key not in result_dict.keys():
                            result_dict[new_key] = [matching_string]
                            break
                            
    return result_dict

def many_table(search_dict, by_line):
    # create dictionary to hold results
    result_dict = {}

    # iterate over dictionary of search terms for each table
    for search_key, value in search_dict.items():
        search_str = value[0]
        position = value[1]
        del_chars = value[2]

        temp_list = []
        
        # iterate over each line
        for line in by_line:

            # is there a match between the search string and the line?
            # if so return the match
            matching_string = find_string(line, search_str, position, del_chars)

            if matching_string != None:
                # clean up the string
                clean_string = clean_text(matching_string)
                temp_list.append(clean_string)

        # after running through each line then add the list to the dictionary
        # and clear the temp list
        result_dict[search_key] = temp_list
    return result_dict        

def many_table_df(result_dict):
    counter = -1
    check = True
    for key, value in result_dict.items():
        if counter == -1:
            counter = len(value)
        elif counter != len(value):
            check = False
            break
    if check == True:
        return pd.DataFrame(result_dict)
    else:
        return pd.DataFrame({"Error": ["Error, number of values in the collection do not align"],
            "Text": [str(result_dict)]})

def one_table_df(result_dict):
    return pd.DataFrame(result_dict)

def format_date(date_string, current_date_format):
    date_obj = datetime.strptime(date_string, current_date_format)
    formatted_date_str = (date_obj.strftime('%Y-%m-%d'))
    return formatted_date_str


def save_as_csv(table, df, file_base, table_name):
    # format dates to standard YYYY-MM-DD
    formatted_date_str = format_date(table['invoice_date'][0], '%B %d, %Y') # November 11, 2015

    # add timestamp to filename
    file_name = "example_output_files/" + file_base + " " + table_name + datetime.now().strftime("%Y%m%d_%H%M%S") + '.csv'
    df.to_csv(file_name, index= False)



def auto_read():
    '''
    This funciton needs to be compared to beta.py before running. 
    '''
    
    # File location
    
    # File name
    scanned_text = read_pdf('amazon_111215.pdf')

    # add the contents for each page into a list
    contents = text_to_list(scanned_text)

    # iterate over each page
    by_line = []
    for page in range(0, len(scanned_text.pages)):  # create a flat list of strings
        by_line += contents[page].split('\n')       # remove the line breaks

    # create a dictionary of search terms
    table_1_search, table_1_type = table_1_search_dict()
    table_2_search, table_2_type = table_2_search_dict()

    # create 
    table_1 = one_table(table_1_search, by_line)
    table_2 = many_table(table_2_search, by_line)  

    table_1_df = one_table_df(table_1)
    table_2_df = many_table_df(table_2)  # verifies that the length of each value list is the same in a many table

    # add a column of invoice numbers for each table_2 entry
    #table_2_df['invoice_number'] = table_1['invoice_number'][0]
    table_2_df.insert(0, 'invoice_number', table_1['invoice_number'][0])

    # format dates to standard YYYY-MM-DD
    formatted_date_str = format_date(table_1['invoice_date'][0], '%B %d, %Y')  # November 11, 2015
    name_base = table_1['company_name'][0].replace('.', '_') + '_' + formatted_date_str

    save_as_csv(table_1_df, name_base, 'overview')
    save_as_csv(table_2_df, name_base, 'products')

    return "All OK."

if __name__ == "__main__":
    auto_read()