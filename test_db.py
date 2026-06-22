from database import engine

try:
    with engine.connect() as connection:
        print("✅ Conectado com sucesso ao banco!")
except Exception as e:
    print("❌ Erro ao conectar:", e)