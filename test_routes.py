from app import app

print("Rotas registradas:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}")

print("\nTestando rota raiz...")
with app.test_client() as client:
    response = client.get('/')
    print(f"Status: {response.status_code}")
    print(f"Conteúdo: {response.data[:200]}...") 