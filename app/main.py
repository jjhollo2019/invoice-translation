from flask import Flask, request, jsonify
from pathlib import Path
from flask_json_schema import JsonSchema, JsonValidationError
import vendorTranslation, erpTranslation, json


erpSchemaPath = Path("/home/jeremy/Documents/invoice-translation/app/schemas/invoice-b-schema.json") 

with open(erpSchemaPath, 'r') as f:
    erpSchema = json.load(f)

app = Flask(__name__)
schema = JsonSchema(app)

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

@app.route('/vendorInvoice', methods=['POST'])
def vendorResponse():
    return vendorTranslation.vendorInvoiceTranslation(request.json)

@app.route('/erpInvoice', methods=['POST'])
@schema.validate(erpSchema)
def erpResponse():
    return erpTranslation.erpInvoiceTranslation(request.json)

if __name__ == '__main__':
    app.run()