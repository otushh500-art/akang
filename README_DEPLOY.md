# RubyMine Backend — Production Deployment Guide
**Version:** v1.0.0 | **Status:** Production Ready

---

## Prerequisites

- Ubuntu 22.04 LTS (or newer)
- 4 GB RAM minimum (8 GB recommended)
- 20 GB SSD storage
- Docker 24+ and Docker Compose v2

> **Note on repository structure:** After restructuring, all backend code is in the `backend/` directory.
> Run `docker compose` commands from the `backend/` directory, or use `-f backend/docker-compose.yml` from the project root.

---

## 1. Server Setup (Ubuntu 22.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker compose version
```

---

## 2. Deploy RubyMine Backend

```bash
# Clone / upload project to server
mkdir -p /opt/rubymine
cd /opt/rubymine
# Upload RubyMine_Backend_v1.0.0.zip here, then:
unzip RubyMine_Backend_v1.0.0.zip
cd case_analytics_project/backend

# Configure environment
cp .env.production.example .env
nano .env   # Fill in all required values (see section 3)

# Start all services (single command)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 3. Required Environment Variables

Edit `.env` and set:

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | JWT signing key (32+ chars) | `openssl rand -hex 32` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://rubymine:PASS@rubymine-postgres:5432/rubymine` |
| `REDIS_URL` | Redis connection string | `redis://:PASS@rubymine-redis:6379/0` |
| `POSTGRES_PASSWORD` | DB password | strong password |
| `REDIS_PASSWORD` | Redis password | strong password |
| `TELEGRAM_BOT_TOKEN` | From @BotFather | `1234567890:ABC...` |
| `TELEGRAM_BOT_USERNAME` | Bot username | `rubymine_bot` |
| `TELEGRAM_WEBAPP_URL` | Mini App URL | `https://t.me/rubymine_bot/app` |
| `CORS_ORIGINS` | Allowed origins | `https://your-domain.com` |
| `CDN_BASE_URL` | Asset CDN URL | `https://cdn.your-domain.com` |

---

## 4. Docker Services

| Container | Role | Auto-restart |
|---|---|---|
| `rubymine-api` | FastAPI (4 workers) | ✅ always |
| `rubymine-postgres` | PostgreSQL 16 | ✅ always |
| `rubymine-redis` | Redis 7 | ✅ always |
| `rubymine-nginx` | Reverse proxy + WebSocket | ✅ always |
| `rubymine-worker-economy` | RTP + economy jobs | ✅ always |
| `rubymine-worker-payment` | Payment processing | ✅ always |
| `rubymine-worker-security` | Security sweeps | ✅ always |
| `rubymine-worker-creator` | Creator analytics | ✅ always |
| `rubymine-worker-user` | Session cleanup | ✅ always |
| `rubymine-worker-assets` | Image pipeline jobs | ✅ always |
| `rubymine-worker-bot` | Telegram bot polling | ✅ always |
| `rubymine-backup` | Daily DB backup scheduler | ✅ unless-stopped |

---

## 5. Database Commands

```bash
# Run migrations manually
docker compose exec rubymine-api alembic upgrade head

# Check migration status
docker compose exec rubymine-api alembic current

# Connect to DB shell
docker compose exec rubymine-postgres psql -U rubymine -d rubymine
```

---

## 6. Backup & Restore

> **Automated daily backups** are provided by the `rubymine-backup` service.
> It runs `backup.sh` every 24 hours (first run ~04:00 UTC) and stores
> `.sql.gz` files in the `backups-data` named volume, retaining the last
> 7 days.  Backups are **local to this server** — periodically copy them
> off-server (e.g. rsync/S3) to protect against full server loss.

```bash
# Create backup (manual)
docker compose exec rubymine-postgres bash /scripts/backup.sh

# Or trigger a backup in the scheduler container immediately:
docker compose exec rubymine-backup sh /scripts/backup.sh

# List backup files in the named volume:
docker compose run --rm rubymine-backup ls -lh /backups

# Restore from backup
docker compose exec rubymine-postgres bash /scripts/restore.sh /backups/rubymine_20240101_120000.sql.gz
```

---

## 7. Health Checks

```bash
# Full health check
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/health/redis
curl http://localhost:8000/api/v1/health/workers

# Using healthcheck script
bash docker/scripts/healthcheck.sh
```

---

## 8. View Logs

```bash
# API logs
docker compose logs -f rubymine-api

# Bot logs
docker compose logs -f rubymine-worker-bot

# Worker logs
docker compose logs -f rubymine-worker-economy

# Nginx access log
docker compose logs -f rubymine-nginx

# All services
docker compose logs -f
```

---

## 9. Updates / Redeployment

```bash
cd /opt/rubymine/case_analytics_project/backend

# Pull new image and restart
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run new migrations
docker compose exec rubymine-api alembic upgrade head
```

---

## 10. Systemd (auto-start on reboot)

```bash
sudo cp docker/systemd/rubymine.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now rubymine
sudo systemctl status rubymine
```

---

## 11. SSL / HTTPS Setup

```bash
# Install certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy to docker ssl dir (relative to backend/)
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem docker/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem docker/ssl/

# Restart nginx
docker compose restart rubymine-nginx
```

---

## 12. Troubleshooting

```bash
# Check all container status
docker compose ps

# Restart specific service
docker compose restart rubymine-api

# Force recreate
docker compose up -d --force-recreate rubymine-api

# Check disk space
df -h

# Check memory
free -h
```

---

## Architecture Overview

```
Internet → Nginx (80/443) → FastAPI API (8000)
                  ↓               ↓
            WebSocket /ws    PostgreSQL 16
                  ↓               ↓
            Redis PubSub    ARQ Workers (6)
                  ↓
            Telegram Bot
```

---

*RubyMine Backend v1.0.0 — Built with FastAPI, PostgreSQL 16, Redis 7, aiogram 3.x*
