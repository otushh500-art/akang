# RubyMine — Backend

**Version:** v1.0.0 — Production Ready

FastAPI-based backend for the CS Case Telegram Mini App.  
Serves the REST API, WebSocket connections, Telegram bot, and background workers.

---

## Quick Start

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env — fill in TELEGRAM_BOT_TOKEN, SECRET_KEY, etc.

# 4. Run database migrations
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload
```

Or with Docker:

```bash
cd backend
docker compose up -d
```

---

## Tech Stack

| Layer       | Technology              |
|-------------|------------------------|
| Framework   | FastAPI                 |
| Python      | 3.12                    |
| Database    | PostgreSQL 16           |
| Cache / Queue | Redis 7 + ARQ        |
| ORM         | SQLAlchemy (async)      |
| Auth        | JWT + Telegram HMAC     |
| Bot         | aiogram 3.13            |
| Tests       | pytest (1813/1813 ✅)   |

---

## Project Structure

```
backend/
├── app/                     # Python package
│   ├── api/v1/              # 33 HTTP route modules
│   ├── bot/                 # Telegram bot (aiogram)
│   ├── core/                # Config, DB, auth deps
│   ├── events/              # Redis pub/sub
│   ├── models/              # 37 SQLAlchemy models
│   ├── repositories/        # Data access layer
│   ├── schemas/             # Pydantic request/response
│   ├── services/            # 87 business logic modules
│   ├── utils/               # Helpers
│   ├── websocket/           # WebSocket handlers
│   ├── workers/             # 13 ARQ background workers
│   └── main.py              # FastAPI app entry point
├── alembic/                 # DB migrations (30 files)
├── tests/                   # 78 test files (1813 tests)
├── docker/                  # Nginx, Postgres, scripts
├── scripts/                 # Admin + documentation generators
├── Dockerfile
├── docker-compose.yml
└── docker-compose.prod.yml
```

---

## API Overview

- **HTTP Routes:** 239
- **WebSocket Routes:** 9
- **WS Events:** 86
- **Redis Channels:** 82

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/telegram` | Telegram initData → JWT |
| GET | `/api/v1/cases/` | List active cases |
| POST | `/api/v1/cases/{id}/open` | Open a case |
| POST | `/api/v1/battle/create` | Create battle |
| WebSocket | `/ws/game/{battle_id}` | Real-time battle |
| GET | `/api/v1/admin/*` | Admin panel (23 sections) |

---

## Background Workers (13)

- Economy, Payment, Security, Battle, Battle Cleanup
- Creator, User Control, Asset, Notification, Admin
- Local Payment, Fake Drop, Cleanup
- Telegram Bot (polling)

---

## Testing

```bash
cd backend
pytest                       # 1813 tests, serial mode
pytest -n auto --dist=loadscope  # parallel (Linux/Docker)
```

---

## Deployment

See [`README_DEPLOY.md`](./README_DEPLOY.md) for production setup.

---

## Systems

- ✅ Telegram WebApp Authentication (HMAC-SHA256)
- ✅ Provably Fair Case Opening
- ✅ Battle System (PvP + Bot)
- ✅ Upgrade System
- ✅ Battle Pass / RubyPass
- ✅ Economy Engine V2 (Shadow RTP)
- ✅ Security Hardening (12 services)
- ✅ Local Payment (UzCard/Humo)
- ✅ Creator + Referral Quality System
- ✅ Admin Panel (23 sections)
- ✅ Telegram Bot + WebApp
- ✅ Skin Image Pipeline
- ✅ WebSocket + Redis PubSub
- ✅ 13 ARQ Workers
- ✅ Docker Deployment (12 containers)
