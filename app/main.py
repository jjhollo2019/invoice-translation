from flask import Flask, request, jsonify, Response
from pathlib import Path
from flask_json_schema import JsonSchema, JsonValidationError
from commonFunctions import insertInvoice
import vendorTranslation, erpTranslation, json


erpSchemaPath = Path("app/schemas/invoice-b-schema.json")
vendorSchemaPath = Path("app/schemas/invoice-a-schema.json")

with open(erpSchemaPath, 'r') as f:
    erpSchema = json.load(f)

with open(vendorSchemaPath, 'r') as f:
    vendorSchema = json.load(f)

app = Flask(__name__)
schema = JsonSchema(app)

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}), 400

@app.route('/vendorInvoice', methods=['POST'])
@schema.validate(vendorSchema)
def vendorResponse():
    vendorInvoice = vendorTranslation.vendorInvoiceTranslation(request.json)
    return insertInvoice(vendorInvoice)
    return 200



@app.route('/erpInvoice', methods=['POST'])
@schema.validate(erpSchema)
def erpResponse():
    return erpTranslation.erpInvoiceTranslation(request.json)

if __name__ == '__main__':
    app.run()