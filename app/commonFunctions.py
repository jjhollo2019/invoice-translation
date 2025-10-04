import sqlite3
from datetime import date

def calculatePaymentDays(fromDate, toDate):
    return (date.fromisoformat(toDate) - date.fromisoformat(fromDate)).days

def insertInvoice(canonicalInvoice):
    invoice = canonicalInvoice['invoice']
    supplier = invoice['supplier']
    paymentTerms = invoice['paymentTerms']
    dates = invoice['dates']
    totals = invoice['totals']

    conn = sqlite3.connect('invoice_tables.db')
    cursor = conn.cursor()

    insertInvoice = """
        INSERT INTO invoices (
        invoice_id, source_system, supplier_code, supplier_name, supplier_address, supplier_contact_email,
        issue_date, due_date, posting_date, currency, payment_terms_code, payment_terms_days,
        subtotal, tax, grand_total
        ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    );"""

    cursor.execute(insertInvoice, (invoice['id'], invoice['sourceSystem'], supplier['code'], supplier['name'], supplier['address'], supplier['contactEmail'],
        dates['issueDate'], dates['dueDate'], dates['postingDate'], invoice['currency'], paymentTerms['code'], paymentTerms['days'],
        totals['subtotal'], totals['tax'], totals['grandTotal'])
    )
    
    query = cursor.execute("""SELECT * FROM invoices""").fetchall()
    print(query)

    insertInvoiceLineItems = """INSERT INTO invoice_line_items (
    invoice_id, line_number, sku, description, uom, quantity, unit_price, tax_rate, line_total
    ) VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    lineItemsData = []
    for item in invoice['lineItems']:
        lineItemsData.append((
            invoice['id'], item['lineNumber'], item['sku'], item['description'], item['uom'], item['quantity'],
            item['unitPrice'], item['taxRate'], item['lineTotal']
        ))

    cursor.executemany(insertInvoiceLineItems, lineItemsData).fetchall()

    itemResponse = cursor.execute("""SELECT * FROM invoice_line_items""").fetchall()
    print(itemResponse)

    insertInvoiceStatus = """INSERT INTO invoice_status (
    invoice_id, status_code, mapped_from
    ) VALUES
    (?, ?, ?);"""

    cursor.execute(insertInvoiceStatus, (invoice['id'], invoice['status']['code'], invoice['status']['mappedFrom']))

    statusResponse = cursor.execute("""SELECT * FROM invoice_status""").fetchall()
    print(statusResponse)

    conn.commit()
    conn.close()
    return True
    # if query[0].id == invoice['id']:
    #     return True
    # else:
    #     return False

    
    # Example for inserting multiple rows using executemany()
    # employees_data = [
    #     ('Bob', 25, 'IT'),
    #     ('Charlie', 35, 'Finance'),
    #     ('David', 28, 'Marketing')
    # ]
    # cursor.executemany("INSERT INTO employees (name, age, department) VALUES (?, ?, ?)",
    #                    employees_data)