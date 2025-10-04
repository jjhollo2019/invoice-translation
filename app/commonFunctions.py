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
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    );"""

    cursor.execute(insertInvoice, (invoice['id'], invoice['sourceSystem'], supplier['code'], supplier['name'], supplier['address'], supplier['contactEmail'],
        dates['issueDate'], dates['dueDate'], dates['postingDate'], invoice['currency'], paymentTerms['code'], paymentTerms['days'],
        totals['subtotal'], totals['tax'], totals['grandTotal']))
    
    query = cursor.execute("""SELECT * FROM invoice""")

    conn.commit()
    conn.close()
    return query

    
    # Example for inserting multiple rows using executemany()
    # employees_data = [
    #     ('Bob', 25, 'IT'),
    #     ('Charlie', 35, 'Finance'),
    #     ('David', 28, 'Marketing')
    # ]
    # cursor.executemany("INSERT INTO employees (name, age, department) VALUES (?, ?, ?)",
    #                    employees_data)