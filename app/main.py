from flask import Flask, request, jsonify, Response
from pathlib import Path
from flask_json_schema import JsonSchema, JsonValidationError
from commonFunctions import insertInvoice, getAllInvoices, getInvoiceById
import vendorTranslation, erpTranslation, json

# create relative paths to the schema files
erpSchemaPath = Path("app/schemas/invoice-b-schema.json")
vendorSchemaPath = Path("app/schemas/invoice-a-schema.json")

# open each schema file and load the JSON data
with open(erpSchemaPath, 'r') as f:
    erpSchema = json.load(f)

with open(vendorSchemaPath, 'r') as f:
    vendorSchema = json.load(f)

# Initialize Flask app and JsonSchema
app = Flask(__name__)
schema = JsonSchema(app)

# Error handler for JSON schema validation errors
@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}), 400

# Define routes for vendor and ERP invoice processing
@app.route('/vendorInvoice', methods=['POST'])
@schema.validate(vendorSchema)
def vendorResponse():
    vendorInvoice = vendorTranslation.vendorInvoiceTranslation(request.json)
    print(vendorInvoice)
    insertSuccess = insertInvoice(vendorInvoice)
    print(insertSuccess)
    if insertSuccess:
        return getInvoiceById(vendorInvoice['invoice']['id']), 201
    else:
        return 400



@app.route('/erpInvoice', methods=['POST'])
@schema.validate(erpSchema)
def erpResponse():
    erpInvoice = erpTranslation.erpInvoiceTranslation(request.json)
    insertSuccess = insertInvoice(erpInvoice)
    if insertSuccess:
        return getInvoiceById(erpInvoice['invoice']['id']), 201
    else:
        return 400

@app.route('/getAllInvoices', methods=['GET'])
def getInvoices():
    allInvoices = getAllInvoices()
    return allInvoices, 200

@app.route('/getInvoiceById/<invoiceId>', methods=['GET'])
def getInvoice(invoiceId):
    invoice = getInvoiceById(invoiceId)
    if invoice:
        return invoice, 200
    else:
        return 404

# Run the Flask app
if __name__ == '__main__':
    app.run()