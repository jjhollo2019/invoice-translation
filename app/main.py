from flask import Flask, request, jsonify
from pathlib import Path
from flask_json_schema import JsonSchema
import vendorTranslation, erpTranslation, json


# Define the path to your JSON schema file
erpSchemaPath = Path("/schemas/invoice-b-schema.json") 

# Open and load the JSON schema
with open(erpSchemaPath, 'r') as f:
    erpSchema = json.load(f)

app = Flask(__name__)
schema = JsonSchema(app)

@app.route('/vendorInvoice', methods=['POST'])
def vendorResponse():
    return vendorTranslation.vendorInvoiceTranslation(request.json)

@app.route('/erpInvoice', methods=['POST'])
@schema.validate(erpSchema)
def erpResponse():
    return erpTranslation.erpInvoiceTranslation(request.json)

if __name__ == '__main__':
    app.run()