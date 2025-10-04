import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('invoice_tables.db')
cursor = conn.cursor()

# Define the CREATE TABLE SQL statement
invoice_table_create = """
    CREATE TABLE invoices (
    invoice_id TEXT PRIMARY KEY,
    source_system TEXT,
    supplier_code TEXT NOT NULL,
    supplier_name TEXT NOT NULL,
    supplier_address TEXT,
    supplier_contact_email TEXT,
    issue_date TEXT NOT NULL,    
    due_date TEXT NOT NULL,
    posting_date TEXT,
    currency TEXT NOT NULL,
    payment_terms_code TEXT,
    payment_terms_days INTEGER,
    subtotal REAL,
    tax REAL,
    grand_total REAL
);"""

# Define the CREATE TABLE SQL statement for line items
invoice_line_item_create = """
    CREATE TABLE invoice_line_items (
    line_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    sku TEXT,
    description TEXT,
    uom TEXT,
    quantity REAL,
    unit_price REAL,
    tax_rate REAL,
    line_total REAL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
);"""

# Define the CREATE TABLE SQL statement for invoice status
invoice_status_create = """
    CREATE TABLE invoice_status (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT NOT NULL,
    status_code TEXT NOT NULL,
    mapped_from TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
);"""

# Execute the CREATE TABLE statements
cursor.execute(invoice_table_create)
cursor.execute(invoice_line_item_create)
cursor.execute(invoice_status_create)

# Commit the changes and close the connection
conn.commit()
conn.close()