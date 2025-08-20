from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # ✅ Corrigido: pega a variável de ambiente corretamente
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("[WARN] DATABASE_URL não encontrada nas variáveis de ambiente. "
              "Defina-a no painel do Railway (Settings → Variables).")

    def get_conn():
        return psycopg2.connect(DATABASE_URL)

    def init_db():
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("[OK] Tabela 'users' verificada/criada.")
        except Exception as e:
            print(f"[ERRO] init_db falhou: {e}")

    @app.route("/", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "flask-demo", "message": "up"}), 200

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json(force=True, silent=True) or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"status": "error", "message": "username e password são obrigatórios"}), 400

        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "ok", "message": "Usuário cadastrado com sucesso"}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json(force=True, silent=True) or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"status": "error", "message": "username e password são obrigatórios"}), 400

        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

        if user:
            return jsonify({"status": "ok", "message": f"Bem-vindo, {username}!"}), 200
        else:
            return jsonify({"status": "error", "message": "Credenciais inválidas"}), 401

    init_db()
    return app

# Inicializa o app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
