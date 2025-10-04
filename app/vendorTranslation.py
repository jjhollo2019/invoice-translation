import commonFunctions

# Translates vendor invoice data into a standardized format

# Converts vendor information
def convertVendor(vendor):
    return {
        'code': vendor['vendor_id'],
        'name': vendor['name'],
        'address': vendor['address'],
        'contactEmail': vendor['contact_email']
    }

# Calculates line total including tax
def calculateTotal(taxRate, unitPrice, quantity):
    unitTotal = unitPrice * quantity
    taxTotal = unitTotal * taxRate
    return round(unitTotal + taxTotal, 2)

# Converts line items from vendor format to standardized format
def convertLineItems(items):
    lineItems = []
    for item in items:
        lineItems.append({
            'lineNumber': item['line_id'],
            'sku': '',
            'description': item['description'],
            'uom': 'EA',
            'quantity': item['quantity'],
            'unitPrice': item['unit_price'],
            'taxRate': item['tax_rate'],
            'lineTotal': calculateTotal(item['tax_rate'], item['unit_price'], item['quantity'])
        })
    return lineItems

# Converts totals from vendor format to standardized format
def convertTotals(totals):
    return {
        'subtotal': totals['subtotal'],
        'tax': totals['tax'],
        'grandTotal': totals['grand_total']
    }

# Main function to translate vendor invoice
def vendorInvoiceTranslation(vendorInvoice):
    # Build the standardized invoice structure
    invoice = {
        'id': vendorInvoice['invoice_id'],
        'sourceSystem': "Vendor_Invoice",
        'supplier': convertVendor(vendorInvoice['vendor']),
        'dates': {
            'issueDate': vendorInvoice['invoice_date'],
            'dueDate': vendorInvoice['due_date'],
            'postingDate': vendorInvoice['invoice_date']
        },
        'currency': vendorInvoice['currency'],
        'paymentTerms': {
            'code': vendorInvoice['payment_terms'],
            'days': commonFunctions.calculatePaymentDays(vendorInvoice['invoice_date'], vendorInvoice['due_date'])
        },
        'lineItems': convertLineItems(vendorInvoice['line_items']),
        'totals': convertTotals(vendorInvoice['totals']),
        'status': {
            'code': 'OPEN',
            'mappedFrom': 'VENDOR'
        }
    }
    
    # Return the translated invoice
    return {
        'invoice': invoice
    }