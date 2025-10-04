from flask import Flask, request, jsonify
import subprocess, vendorTranslation, erpTranslation

app = Flask(__name__)

@app.route('/vendorInvoice', methods=['POST'])
def vendorResponse():
    return vendorTranslation.vendorInvoiceTranslation(request.json)

@app.route('/erpInvoice', methods=['POST'])
def erpResponse():
    return erpTranslation.erpInvoiceTranslation(request.json)

if __name__ == '__main__':
    app.run()