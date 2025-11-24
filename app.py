from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "OK",
        "message": "Aplikace Tour de App (Flask) běží!",
        "faze": "Fáze 0 - Pripraveno pro Tour de Cloud"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
