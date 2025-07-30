from flask import jsonify
from app.routes import api_bp


@api_bp.route('/', methods=['GET'])
def home():
    """Home endpoint."""
    return jsonify({
        'message': 'Bem-vindo à API Flask!',
        'status': 'success',
        'version': '1.0.0'
    })


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando corretamente',
        'version': '1.0.0'
    }) 