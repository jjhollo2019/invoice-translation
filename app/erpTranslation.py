



def erpInvoiceTranslation(erpInvoice):
    invoice = {
        'id': erpInvoice['documentNumber'],
        'sourceSystem': "ERP",
        'supplier': {
            'code': erpInvoice['supplierCode'],
            'name': erpInvoice['supplierName']
        },
        'dates': {
            'issuedDate': erpInvoice['postingDate'],
            'dueDate': erpInvoice['dueDate'],
            'postingDate': erpInvoice['postingDate']
        },
        'currency': erpInvoice,
        'paymentTerms': {
            'code': erpInvoice,
            'days': erpInvoice
        }
    }

    return {
        'invoice': invoice
    }