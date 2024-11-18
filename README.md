# pdf-to-database

## The problem
A company regularly receives invoices in PDF format. The PDF invoices are the main record by which the company is compensated by their various servicers. The number of servicers is known and limited. The invoices contain the dollar amount distributed to the company for a particular service, called an 'account' internally. Additional information pertaining to the account, the date, and the servicer's name, among other data, are also included.  

### Current methodology
These invoice data are currently manually copied and entered into a spreadhseet. This spreadsheet holds information on the accounts and the expected payment from the servicer to the account. These payments are estimated to be wrong 20% of the time and thus require immense scrutiny. The accounts are associated with personell and other aspects of the company and defined by internal business logic which is not in the scope of this project. 

#### Downsides and Upsides of current methodology
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


### Proposed methodology

