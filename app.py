from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'], strict_slashes=False) 
def api_endpoint():
    response = {
        "organization": "Student Cyber Games"
    }
    return jsonify(response)

@app.route('/courses')
def courses():
    return render_template('courses.html')
