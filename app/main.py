from flask import Flask, request, jsonify
import subprocess, vendorTranslation

app = Flask(__name__)

@app.route('/vendorInvoice', methods=['POST'])
def returnResponse():
    return vendorTranslation.vendorInvoiceTranslation(request.json)

if __name__ == '__main__':
    app.run()