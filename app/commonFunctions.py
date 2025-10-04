import sqlite3
from datetime import date

# Common function to calculate payment days between two dates
def calculatePaymentDays(fromDate, toDate):
    return (date.fromisoformat(toDate) - date.fromisoformat(fromDate)).days

# Function to insert a canonical invoice into the database
def insertInvoice(canonicalInvoice):
    # create helper variable
    invoice = canonicalInvoice['invoice']

    # connect to the SQLite database
    conn = sqlite3.connect('invoice_tables.db')
    # open a cursor to perform database operations
    cursor = conn.cursor()

    # SQL statement to insert the invoice data into the invoices table
    insertInvoice = """
        INSERT INTO invoices (
        invoice_id, source_system, supplier_code, supplier_name, supplier_address, supplier_contact_email,
        issue_date, due_date, posting_date, currency, payment_terms_code, payment_terms_days,
        subtotal, tax, grand_total
        ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    );"""

    # execute the insert statement with the invoice data
    cursor.execute(insertInvoice, (
        invoice['id'], invoice['sourceSystem'], invoice['supplier']['code'], invoice['supplier']['name'],
        invoice['supplier']['address'], invoice['supplier']['contactEmail'], invoice['dates']['issueDate'],
        invoice['dates']['dueDate'], invoice['dates']['postingDate'], invoice['currency'],
        invoice['paymentTerms']['code'], invoice['paymentTerms']['days'], invoice['totals']['subtotal'],
        invoice['totals']['tax'], invoice['totals']['grandTotal']
    ))
    
    # Debugging: Fetch and print all rows from the invoices table
    query = cursor.execute("""SELECT * FROM invoices""").fetchall()
    print(query)

    # Insert line items into the invoice_line_items table
    insertInvoiceLineItems = """INSERT INTO invoice_line_items (
    invoice_id, line_number, sku, description, uom, quantity, unit_price, tax_rate, line_total
    ) VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    # Prepare data for multiple line item insertion
    lineItemsData = []
    for item in invoice['lineItems']:
        lineItemsData.append((
            invoice['id'], item['lineNumber'], item['sku'], item['description'], item['uom'], item['quantity'],
            item['unitPrice'], item['taxRate'], item['lineTotal']
        ))

    # Execute the insertion of multiple line items
    cursor.executemany(insertInvoiceLineItems, lineItemsData).fetchall()

    # Debugging: Fetch and print all rows from the invoice_line_items table
    itemResponse = cursor.execute("""SELECT * FROM invoice_line_items""").fetchall()
    print(itemResponse)

    # Insert status into the invoice_status table
    insertInvoiceStatus = """INSERT INTO invoice_status (
    invoice_id, status_code, mapped_from
    ) VALUES
    (?, ?, ?);"""

    # Execute the insertion of the invoice status
    cursor.execute(insertInvoiceStatus, (invoice['id'], invoice['status']['code'], invoice['status']['mappedFrom']))

    # Debugging: Fetch and print all rows from the invoice_status table
    statusResponse = cursor.execute("""SELECT * FROM invoice_status""").fetchall()
    print(statusResponse)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    # return success
    return True