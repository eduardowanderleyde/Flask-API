from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Bem-vindo à API Flask!',
        'status': 'success'
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando corretamente'
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000) 