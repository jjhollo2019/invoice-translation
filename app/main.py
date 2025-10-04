from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/invoice', methods=['POST'])
def returnResponse():
    return "api response"

if __name__ == '__main__':
    app.run()