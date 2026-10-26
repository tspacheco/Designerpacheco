#!/usr/bin/env bash
# Junta o n8n ao servidor da Evolution API (mesma rede, HTTPS pelo Caddy). Pacheco Studios.
set -euo pipefail
DIR=/opt/evolution
cd "$DIR"
[ -f .env ] || { echo "Falta $DIR/.env: corre primeiro o instalar.sh"; exit 1; }

IP=$(curl -4 -fsS https://api.ipify.org)
DOMINIO_N8N="n8n.${IP}.sslip.io"

if ! grep -q '^N8N_ENCRYPTION_KEY=' .env; then
cat >> .env <<EOF
DOMINIO_N8N=${DOMINIO_N8N}
N8N_ENCRYPTION_KEY=$(openssl rand -hex 24)
EOF
fi

cat > Caddyfile <<'EOF'
{$DOMINIO} {
	reverse_proxy evolution-api:8080
}

{$DOMINIO_N8N} {
	reverse_proxy n8n:5678
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
  n8n:
    image: n8nio/n8n:2.44.6
    container_name: n8n
    restart: always
    environment:
      N8N_HOST: ${DOMINIO_N8N}
      N8N_PROTOCOL: https
      N8N_PORT: 5678
      WEBHOOK_URL: https://${DOMINIO_N8N}/
      N8N_PROXY_HOPS: 1
      N8N_ENCRYPTION_KEY: ${N8N_ENCRYPTION_KEY}
      GENERIC_TIMEZONE: Europe/Bucharest
      TZ: Europe/Bucharest
      N8N_COMMUNITY_PACKAGES_ENABLED: "true"
      N8N_DIAGNOSTICS_ENABLED: "false"
    volumes:
      - n8n_data:/home/node/.n8n
  caddy:
    image: caddy:2-alpine
    container_name: evolution_caddy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    environment:
      DOMINIO: ${DOMINIO}
      DOMINIO_N8N: ${DOMINIO_N8N}
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on:
      - evolution-api
      - n8n
volumes:
  evolution_instances:
  postgres_data:
  redis_data:
  n8n_data:
  caddy_data:
EOF

docker compose up -d
docker compose restart caddy >/dev/null
echo "A arrancar o n8n (até 2 minutos)..."
for i in $(seq 1 40); do
  if curl -fsS "https://${DOMINIO_N8N}/healthz" >/dev/null 2>&1; then break; fi
  sleep 3
done

echo
echo "================ PRONTO ================"
echo "n8n:        https://${DOMINIO_N8N}"
echo "Abre o link e cria a conta de dono (email + palavra-passe)."
echo "Dentro do n8n, a Evolution está em: http://evolution-api:8080"
echo "========================================"
curl -fsS "https://${DOMINIO_N8N}/healthz" || echo "(Ainda a arrancar: abre o link daqui a 1 minuto.)"
