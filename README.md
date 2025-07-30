# Flask-API

Uma API RESTful moderna construída com Flask, seguindo as melhores práticas de engenharia de software.

## 🚀 Características

- **Arquitetura Limpa**: Separação clara de responsabilidades
- **Documentação Completa**: Swagger/OpenAPI integrado
- **Testes Automatizados**: Cobertura de testes unitários e de integração
- **Validação de Dados**: Schemas de validação robustos
- **Autenticação**: Sistema de autenticação JWT
- **Logs Estruturados**: Sistema de logging profissional
- **Configuração Flexível**: Múltiplos ambientes (dev, staging, prod)
- **Docker**: Containerização para deploy consistente

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Docker (opcional)

## 🛠️ Instalação

### Desenvolvimento Local

```bash
# Clone o repositório
git clone https://github.com/eduardowanderleyde/Flask-API.git
cd Flask-API

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute as migrações (se aplicável)
flask db upgrade

# Inicie o servidor
flask run
```

### Docker

```bash
# Construa a imagem
docker build -t flask-api .

# Execute o container
docker run -p 5000:5000 flask-api
```

## 📚 Documentação da API

Acesse a documentação interativa da API em:

- **Swagger UI**: <http://localhost:5000/api/docs>
- **ReDoc**: <http://localhost:5000/api/redoc>

## 🧪 Testes

```bash
# Execute todos os testes
pytest

# Execute com cobertura
pytest --cov=app

# Execute testes específicos
pytest tests/test_users.py
```

## 📁 Estrutura do Projeto

```
flask-api/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│   └── utils/
├── tests/
├── migrations/
├── docs/
├── docker/
├── requirements.txt
├── config.py
├── .env.example
└── README.md
```

## 🔧 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=your-jwt-secret
```

## 🚀 Deploy

### Heroku

```bash
# Configure o Heroku CLI
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

### Docker Compose

```bash
docker-compose up -d
```

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, envie um email para [seu-email@exemplo.com](mailto:seu-email@exemplo.com)
