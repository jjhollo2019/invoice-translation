import sqlite3
import json
from typing import List, Dict, Any
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

def getAllInvoices():
    conn = sqlite3.connect('invoice_tables.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get invoices with status
    cur.execute("""
        SELECT i.*, s.status_code, s.mapped_from
        FROM invoices i
        JOIN invoice_status s ON i.invoice_id = s.invoice_id
    """)
    invoices = cur.fetchall()

    # Get line items
    cur.execute("SELECT * FROM invoice_line_items;")
    line_items = cur.fetchall()
    conn.close()

    # Build JSON in Python
    invoices_json = []
    for inv in invoices:
        inv_lines = [
            dict(li)
            for li in line_items
            if li["invoice_id"] == inv["invoice_id"]
        ]
        invoices_json.append({
            "invoice": {
                "id": inv["invoice_id"],
                "sourceSystem": inv["source_system"],
                "supplier": {
                    "code": inv["supplier_code"],
                    "name": inv["supplier_name"],
                    "address": inv["supplier_address"],
                    "contactEmail": inv["supplier_contact_email"]
                },
                "dates": {
                    "issueDate": inv["issue_date"],
                    "dueDate": inv["due_date"],
                    "postingDate": inv["posting_date"]
                },
                "currency": inv["currency"],
                "paymentTerms": {
                    "code": inv["payment_terms_code"],
                    "days": inv["payment_terms_days"]
                },
                "lineItems": inv_lines,
                "totals": {
                    "subtotal": inv["subtotal"],
                    "tax": inv["tax"],
                    "grandTotal": inv["grand_total"]
                },
                "status": {
                    "code": inv["status_code"],
                    "mappedFrom": inv["mapped_from"]
                }
            }
        })

    return invoices_json


