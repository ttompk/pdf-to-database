# PDF-to-Database

## The problem
A company regularly receives invoices in PDF format. The PDF invoices are the main record by which the company is compensated by their various servicers. The number of servicers is known and limited. The invoices contain the dollar amount distributed to the company for a particular service, called an 'account' internally. Additional information pertaining to the account, the date, and the servicer's name, among other data, are also included.  

## Current methodology
These invoice data are currently manually copied and entered into a spreadhseet. This spreadsheet holds information on the accounts and the expected payment from the servicer to the account. These payments are estimated to be wrong 20% of the time and thus require immense scrutiny. The accounts are associated with personell and other aspects of the company and defined by internal business logic which is not in the scope of this project. 

### Downsides and Upsides of current methodology
The current methodolology has several DOWNSIDES:  
1. Human error - copy and pasting into excel spreadsheets can introduce human error however the number of acount payments evaluated weekly is small (n=?) and presumably is of low risk.
2. No immutable record - unless spreadsheets are being saved as flat files at regular intervals, then all invoice history is editable. The original invoices are presevered but the basis for business decisioning (the purpose of the spreadsheet) remains editable.
3. Lack of organized persistant memory - A loss of a spreadsheet could mean the loss of transactional history.
4. Inefficiency - Maintaining spreadhseets, opening PDF files, hand entering values into a sheet, reasoning on the values, and taking downstream actions are time wasters.
5. Lack of downstream analytical value - There could be value in analyzing invoice and account information over time, or many other analyses, but without a central, organized, longitudinal data depository it is likely the effort will be too great for unknown rewards.

The following UPSIDES are observed:  
1. No need for infrastructure beyond current file server. 
2. No need for maintanence of coding files. 
3. No technical skills required.


## Proposed methodology
#### Overview
Manual
1. Manually save PDFs to directory 
Auto, nightly
2. lock directory
3. Read PDF, format data, save to database
5. Read next file until empty
6. Unlock directory

### Flow
1. Manually save PDF to directory. Currently, files are downloaded from servicers and saved to MS OneDrive. A user manually downloads PDF files from servicers into a ‘downloads’ directory. If there are any emails this is easy to automate as well. This can be at any time, any day of the week.

2. Every night at 12am a bash program runs that temporarily locks the directory with the PDF files.
3. A python program then opens a PDF, reads the data, and decides automatically which table(s) to create. 
The program performs validation checks to be certain the data were collected and formatted as intended. If there is an error, a file will be saved stating such and an email or other means of notification can be sent stating there was an issue with the read.
4. The original PDF is moved to the proper directory for storage. If it threw an error then it goes to the ‘Error’ pile for manual entry :(
5. The newly created table(s) is saved as a CSV files in the assigned directory.
6. The data in memory is upload to an existing table in a postgres relational database. Proper upload is validated. If an error is thrown then the error will be logged in a separate table in the database or logged elsewhere as needed.
7. Program then moves to the next PDF until all are read and uploaded to the database.

### What to do with these database tables? 
- View with Power BI (or whatever tool you use currently)
- If investing in the data visualization software is not desirable, then an automatic export from the database to excel files as needed, weekly or whatever, can be performed. 

### Required Infrastructure
- A sever to securely save the files (you are doing this already presumably). On the same server as above you’ll save: python files (logic files) and a bash file (the automation file).
- A postgres database (free).

### MAINTENANCE
- The python files need to be maintained when: PDF files from new vendors are added or there is a significant change in existing PDF formatting. 
- Database needs to be ‘cleaned’ at least twice a year. This is just a review of the database health to prevent any issues.
- Data visualization software...I’m thinking it’s really cheap - $5 a month per user? - ...needs to be set up to see the data and perform analysis. However, the free/nearly free version of power BI does not allow one to update data in the underlying database. If there are needs to update the database, a separate program would be needed. 
