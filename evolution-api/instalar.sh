#!/usr/bin/env bash
# Instala Evolution API (Postgres + Redis + Caddy HTTPS) num Ubuntu limpo. Pacheco Studios.
set -euo pipefail
IP=$(curl -4 -fsS https://api.ipify.org)
DOMINIO="evo.${IP}.sslip.io"
DIR=/opt/evolution
mkdir -p "$DIR" && cd "$DIR"

if ! command -v docker >/dev/null; then curl -fsSL https://get.docker.com | sh; fi

# Firewall: só SSH, HTTP e HTTPS
if command -v ufw >/dev/null; then ufw allow OpenSSH >/dev/null; ufw allow 80/tcp >/dev/null; ufw allow 443/tcp >/dev/null; ufw --force enable >/dev/null; fi

if [ ! -f .env ]; then
API_KEY=$(openssl rand -hex 24)
PG_PASS=$(openssl rand -hex 16)
cat > .env <<EOF
DOMINIO=${DOMINIO}
SERVER_URL=https://${DOMINIO}
AUTHENTICATION_API_KEY=${API_KEY}
AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true
POSTGRES_PASSWORD=${PG_PASS}
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI=postgresql://evolution:${PG_PASS}@postgres:5432/evolution?schema=public
DATABASE_CONNECTION_CLIENT_NAME=evolution_exchange
DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=true
DATABASE_SAVE_MESSAGE_UPDATE=true
DATABASE_SAVE_DATA_CONTACTS=true
DATABASE_SAVE_DATA_CHATS=true
DATABASE_SAVE_DATA_LABELS=true
DATABASE_SAVE_DATA_HISTORIC=false
CACHE_REDIS_ENABLED=true
CACHE_REDIS_URI=redis://redis:6379/6
CACHE_REDIS_PREFIX_KEY=evolution
CACHE_REDIS_SAVE_INSTANCES=false
CACHE_LOCAL_ENABLED=false
CONFIG_SESSION_PHONE_CLIENT=Pacheco Studios
CONFIG_SESSION_PHONE_NAME=Chrome
DEL_INSTANCE=false
LANGUAGE=pt-BR
WEBHOOK_GLOBAL_ENABLED=false
EOF
chmod 600 .env
fi

cat > Caddyfile <<'EOF'
{$DOMINIO} {
	reverse_proxy evolution-api:8080
}
EOF

cat > docker-compose.yml <<'EOF'
services:
  evolution-api:
    image: evoapicloud/evolution-api:v2.3.7
    container_name: evolution_api
    restart: always
    env_file: .env
    volumes:
      - evolution_instances:/evolution/instances
    depends_on:
      - postgres
      - redis
  postgres:
    image: postgres:16-alpine
    container_name: evolution_postgres
    restart: always
    environment:
      POSTGRES_USER: evolution
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: evolution
    volumes:
      - postgres_data:/var/lib/postgresql/data
  redis:
    image: redis:7-alpine
    container_name: evolution_redis
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
  caddy:
    image: caddy:2-alpine
    container_name: evolution_caddy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    environment:
      DOMINIO: ${DOMINIO}
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on:
      - evolution-api
volumes:
  evolution_instances:
  postgres_data:
  redis_data:
  caddy_data:
EOF

docker compose up -d
echo "A arrancar (até 2 minutos)..."
for i in $(seq 1 40); do
  if curl -fsS "https://${DOMINIO}/" >/dev/null 2>&1; then break; fi
  sleep 3
done

echo
echo "================ PRONTO ================"
echo "Painel:     https://${DOMINIO}/manager"
echo "Chave API:  $(grep ^AUTHENTICATION_API_KEY .env | cut -d= -f2)"
echo "Guarda a chave num sítio seguro. Não a envies por mensagem."
echo "========================================"
curl -fsS "https://${DOMINIO}/" || echo "(Ainda a arrancar: abre o painel daqui a 1 minuto.)"
