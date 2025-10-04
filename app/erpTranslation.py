import commonFunctions



def convertLineItems(items, taxRate):
    lineItems = []
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

def findTaxPercentByCode(taxes, taxCode):
    for tax in taxes:
        if tax['taxCode'] == taxCode:
            return tax['taxPercent']
    return 0

def sumChargesByKey(charges, key):
    total = 0
    for charge in charges:
        total += charge[key]
    return total

def erpInvoiceTranslation(erpInvoice):
    salesTax = findTaxPercentByCode(erpInvoice['taxes'], "SALES")
    invoice = {
        'id': erpInvoice['documentNumber'],
        'sourceSystem': "ERP",
        'supplier': {
            'code': erpInvoice['supplierCode'],
            'name': erpInvoice['supplierName'],
            'address': '',
            'contactEmail': ''
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

    return {
        'invoice': invoice
    }