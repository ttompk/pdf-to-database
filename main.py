import sys_pdf
import pdf_functions as pdf
import os
import dotenv
import openai

# Move PDF files to working directory
#source_dir = "pdf_inbox"
#target_dir = "pdf_examples"
#sys_pdf.move_pdf_files(source_dir, target_dir)


######
'''
Using openai's model to extract the data from the table.
'''

# Load environment variables from the .env file
dotenv.load_dotenv()

# instantiate the openai class with key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# File path to the PDF
file_path = "working_dir/amazon_111215.pdf"

# Step 1: Extract text from the PDF
pdf_text = pdf.extract_text_from_pdf(file_path)

# Step 2: Extract specific invoice details using OpenAI ChatCompletion
# 'response' is the unformated data
response, invoice_data = pdf.overview_extract_invoice_data(pdf_text)

# Step 3: Create a table with the extracted data
invoice_table = pdf.create_invoice_table(invoice_data)

# Step 4: Save the table to a CSV file
invoice_table.to_csv("example-output_files/invoice_table.csv", index=False)

print("Invoice data extracted and saved to 'invoice_table.csv'.")

