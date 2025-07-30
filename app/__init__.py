from flask import Flask, render_template_string
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from app.models.user import db, bcrypt


def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Root route - Welcome page
    @app.route('/')
    def home():
        html_template = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Flask API - Backend Profissional</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }
                
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    max-width: 600px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                
                h1 {
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    background: linear-gradient(45deg, #fff, #f0f0f0);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                
                .subtitle {
                    font-size: 1.2em;
                    margin-bottom: 30px;
                    opacity: 0.9;
                }
                
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                
                .feature {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                
                .feature h3 {
                    margin-bottom: 10px;
                    color: #fff;
                }
                
                .feature p {
                    opacity: 0.8;
                    font-size: 0.9em;
                }
                
                .endpoints {
                    background: rgba(0, 0, 0, 0.2);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    text-align: left;
                }
                
                .endpoint {
                    margin: 10px 0;
                    font-family: 'Courier New', monospace;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 8px 12px;
                    border-radius: 5px;
                    display: inline-block;
                }
                
                .status {
                    display: inline-block;
                    background: #4CAF50;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.8em;
                    margin-top: 10px;
                }
                
                .github {
                    margin-top: 30px;
                }
                
                .github a {
                    color: #fff;
                    text-decoration: none;
                    background: rgba(255, 255, 255, 0.2);
                    padding: 10px 20px;
                    border-radius: 25px;
                    transition: all 0.3s ease;
                }
                
                .github a:hover {
                    background: rgba(255, 255, 255, 0.3);
                    transform: translateY(-2px);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Flask API</h1>
                <p class="subtitle">Backend profissional construído com Flask</p>
                
                <div class="status">✅ ONLINE</div>
                
                <div class="features">
                    <div class="feature">
                        <h3>🔐 Autenticação</h3>
                        <p>Sistema completo de login e registro com JWT</p>
                    </div>
                    <div class="feature">
                        <h3>📊 RESTful API</h3>
                        <p>Endpoints organizados e documentados</p>
                    </div>
                    <div class="feature">
                        <h3>🛡️ Segurança</h3>
                        <p>Senhas criptografadas e tokens seguros</p>
                    </div>
                </div>
                
                <div class="endpoints">
                    <h3>📡 Endpoints Disponíveis:</h3>
                    <div class="endpoint">GET /api/</div>
                    <div class="endpoint">GET /api/health</div>
                    <div class="endpoint">POST /api/auth/register</div>
                    <div class="endpoint">POST /api/auth/login</div>
                    <div class="endpoint">GET /api/auth/profile</div>
                </div>
                
                <div class="github">
                    <a href="https://github.com/eduardowanderleyde/Flask-API" target="_blank">
                        📁 Ver no GitHub
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        return html_template
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


# Create app instance for gunicorn
app = create_app() 