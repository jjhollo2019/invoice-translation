Sample Invoice API Translation

Scenerio: Vendors and Company ERP need to send invoices to financial system

Design Considerations
    - Using distinct endpoints allows for schema based validation 
    - Schema based validation is simpler to maintain than business rules
    - Canonical Invoice allows for simplified data processing

Implementation
    - created /vendorInvoice endpoint with JSON schema validation
    - created /erpInvoice endpoint with JSON schema validation

Usage
    I created a very light db for this just to show data going into a table,
    noramlly I would want to use a stored procedure or internal API for inserts.
    Start the virtual environment and call the database.py script to start up a 
    db with the required tables.
    Run main.py and use your localhost to make api calls from an API client like 
    postman to interact with the endpoints.
    I created sample payloads and yaml so you have something to start with and 
    options to create more sample use cases.
    When completed use dropTables.py to clean everything from the db.