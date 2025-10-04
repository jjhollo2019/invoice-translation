



def convertVendor(vendor):
    return {
        'code': vendor['vendor_id'],
        'name': vendor['name'],
        'address': vendor['address'],
        'contactEmail': vendor['contact_email']
    }


def vendorInvoiceTranslation(vendorInvoice):
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
        'paymentTerms': 
    }
    
    return {
        'invoice': invoice
    }