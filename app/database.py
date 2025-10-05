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



suppliers_table_create = """
    CREATE TABLE suppliers (
    supplier_code TEXT PRIMARY KEY,           
    supplier_name TEXT NOT NULL,             
    address_line1 TEXT,
    address_line2 TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    country TEXT DEFAULT 'USA',
    contact_name TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    payment_terms TEXT DEFAULT 'NET30',
    active INTEGER DEFAULT 1 CHECK (active IN (0,1)),  -- 1=active, 0=inactive
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);"""

insert_supplier_data = """
INSERT INTO suppliers (
    supplier_code, supplier_name, address_line1, city, state, postal_code,
    contact_name, contact_email, contact_phone, payment_terms
    ) VALUES
    ('SUP-ACME-001', 'Acme Supplies LLC', '123 Main St', 'Greenville', 'SC', '29601',
    'Jane Carter', 'billing@acmesupplies.com', '864-555-0101', 'NET30'),
    ('SUP-GLOBAL-002', 'Global Freight Solutions', '2100 Industrial Ave', 'Charlotte', 'NC', '28202',
    'Marcus Lee', 'mlee@globalfreight.com', '704-555-0144', 'NET45'),
    ('SUP-PAPER-003', 'Paper Depot Inc.', '880 Stationery Blvd', 'Atlanta', 'GA', '30303',
    'Lisa Tran', 'orders@paperdepot.com', '404-555-0199', 'NET15'),
    ('SUP-TECH-004', 'TechEdge Components', '500 Innovation Dr', 'Raleigh', 'NC', '27606',
    'Raj Patel', 'raj@techedge.com', '919-555-0122', 'NET30'),
    ('SUP-OFFICE-005', 'OfficePro Distributors', '75 Supply Park Rd', 'Knoxville', 'TN', '37902',
    'Erica Johnson', 'erica.j@officepro.com', '865-555-0188', 'NET60'
);"""


# Execute the CREATE TABLE statements
cursor.execute(invoice_table_create)
cursor.execute(invoice_line_item_create)
cursor.execute(invoice_status_create)
cursor.execute(suppliers_table_create)
cursor.execute(insert_supplier_data)

# Commit the changes and close the connection
conn.commit()
conn.close()