# Flask + PostgreSQL (Railway) — Demo Seguro

Endpoints:
- `GET /` → saúde
- `POST /register` → { "username": "...", "password": "..." }
- `POST /login` → { "username": "...", "password": "..." }

## Deploy no Railway
1. Crie um projeto **Empty Project**.
2. Adicione um serviço **PostgreSQL**.
3. Em **Variables** do seu serviço Flask, adicione `DATABASE_URL` (copie do serviço do Postgres).
4. Faça deploy deste ZIP (Deploy → Deploy from Zip).

## Testes (curl)
```bash
curl -X POST "postgresql://postgres:TXoIEiWtwSjlkjWAFUnHvkZeOkkdPNzz@postgres.railway.internal:5432/railway/register"   -H "Content-Type: application/json"   -d '{"username":"demo@local.test","password":"Passw0rd!"}'

curl -X POST "postgresql://postgres:TXoIEiWtwSjlkjWAFUnHvkZeOkkdPNzz@postgres.railway.internal:5432/railway/login"   -H "Content-Type: application/json"   -d '{"username":"demo@local.test","password":"Passw0rd!"}'
