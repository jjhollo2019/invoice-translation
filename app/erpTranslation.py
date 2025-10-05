import commonFunctions
import sqlite3

# ERP Invoice Translation Functions

# Converts line items from ERP format to standard format
def convertLineItems(items, taxRate):
    lineItems = []
    # convert tax rate percentage to decimal
    taxRate = taxRate / 100.0
    for item in items:
        itemTax = round(item['price'] * taxRate, 2)
        lineItems.append({
            'lineNumber': items.index(item) + 1,
            'sku': item['sku'],
            'description': item['description'],
            'uom': item['uom'],
            'quantity': item['qty'],
            'unitPrice': item['price'],
            'taxRate': itemTax,
            'lineTotal': round(item['lineAmount'] + itemTax, 2)
        })
    return lineItems

# Finds the tax percentage for a given tax code
def findTaxPercentByCode(taxes, taxCode):
    for tax in taxes:
        if tax['taxCode'] == taxCode:
            return tax['taxPercent']
    return 0

# Sums charges by a specified key in a list of charges
def sumChargesByKey(charges, key):
    total = 0
    for charge in charges:
        total += charge[key]
    return total

def getSupplierDetails(supplierCode):
    print("Fetching supplier details for code:", supplierCode)
    # Fetch supplier details from the suppliers table
    # Connect to the database
    conn = sqlite3.connect('invoice_tables.db')
    cursor = conn.cursor()
    # Query the suppliers table
    cursor.execute("SELECT * FROM suppliers WHERE supplier_code = ?", (supplierCode,))
    # Fetch one result
    supplier = cursor.fetchone()
    print(supplier)
    # Close the connection
    conn.close()
    # Return supplier details or default values if not found
    if supplier:
        return {
            'code': supplier[0],
            'name': supplier[1],
            'address': f"{supplier[2]}, {supplier[3]}, {supplier[4]}, {supplier[5]} {supplier[6]}, {supplier[7]}",
            'contactEmail': supplier[8]
        }
    else:
        return {
            'code': supplierCode,
            'name': 'Unknown Supplier',
            'address': '',
            'contactEmail': ''
        }

# Main function to translate ERP invoice to standard format
def erpInvoiceTranslation(erpInvoice):
    # Assume sales tax is identified by the code "SALES"
    salesTax = findTaxPercentByCode(erpInvoice['taxes'], "SALES")
    # Get supplier details from the suppliers table
    supplierCode = erpInvoice['supplierCode']
    supplierDetails = getSupplierDetails(supplierCode)
    # Build the standardized invoice structure
    invoice = {
        'id': erpInvoice['documentNumber'],
        'sourceSystem': "ERP",
        'supplier': {
            'code': supplierCode,
            'name': erpInvoice['supplierName'],
            'address': supplierDetails['address'],
            'contactEmail': supplierDetails['contactEmail']
        },
        'dates': {
            'issueDate': erpInvoice['postingDate'],
            'dueDate': erpInvoice['dueDate'],
            'postingDate': erpInvoice['postingDate']
        },
        'currency': erpInvoice['currencyCode'],
        'paymentTerms': {
            'code': erpInvoice['paymentTermCode'],
            'days': commonFunctions.calculatePaymentDays(erpInvoice['postingDate'], erpInvoice['dueDate'])
        },
        'lineItems': convertLineItems(erpInvoice['items'], salesTax),
        'totals': {
            'subtotal': sumChargesByKey(erpInvoice['items'], 'lineAmount'),
            'tax': sumChargesByKey(erpInvoice['taxes'], 'taxAmount'),
            'grandTotal': erpInvoice['totalAmount']
        },
        'status': {
            'code': 'OPEN',
            'mappedFrom': "ERP"
        }
    }

    # Return the standardized invoice
    return {
        'invoice': invoice
    }