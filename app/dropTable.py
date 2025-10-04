import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('invoice_tables.db')
# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = cursor.fetchall()

# Drop each table
for table_name in tables:
    table_name = table_name[0]  # Extract the table name from the tuple
    drop_statement = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_statement)
    print(f"Dropped table: {table_name}")

# Commit changes and close the connection
conn.commit()
print("All user-defined tables dropped successfully.")
conn.close()