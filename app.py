from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def api_endpoint():
    response = {
        "organization": "Student Cyber Games"
    }
    return jsonify(response)


