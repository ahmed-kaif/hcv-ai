#!/bin/bash

# === Variables ===
FRONTEND_REPO="https://github.com/ahmed-kaif/hcv-frontend.git"
BACKEND_REPO="https://github.com/ahmed-kaif/hcv-ai.git"
PROJECT_DIR="$HOME/hcv-project"
NGINX_CONF_DIR="$PROJECT_DIR/nginx/conf.d"
SSL_DIR="$PROJECT_DIR/ssl"

# === Create project directories ===
mkdir -p "$PROJECT_DIR"
mkdir -p "$NGINX_CONF_DIR"
mkdir -p "$SSL_DIR"

cd "$PROJECT_DIR" || exit

# === Clone frontend and backend repos ===
echo "Cloning repositories..."
git clone "$FRONTEND_REPO"
git clone "$BACKEND_REPO"

# === Generate self-signed SSL certificate ===
echo "Generating self-signed SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$SSL_DIR/privkey.pem" \
  -out "$SSL_DIR/cert.pem" \
  -subj "/C=US/ST=State/L=City/O=HCV-AI/CN=localhost"

# === Create Nginx default.conf ===
echo "Creating Nginx configuration..."
cat > "$NGINX_CONF_DIR/default.conf" <<EOL
server {
    listen 80;
    server_name _;

    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate     /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/privkey.pem;

    # Proxy Next.js frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header   Host \$host;
        proxy_set_header   X-Real-IP \$remote_addr;
        proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto \$scheme;
    }

    # Proxy FastAPI backend
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header   Host \$host;
        proxy_set_header   X-Real-IP \$remote_addr;
        proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto \$scheme;
    }
}
EOL

# === Create docker-compose.yml ===
echo "Creating docker-compose.yml..."
cat > "$PROJECT_DIR/docker-compose.yml" <<EOL
version: '3.8'

services:
  backend:
    build: ./hcv-ai
    container_name: hcv-backend
    expose:
      - "8000"
    environment:
      - SECRET_KEY=\${SECRET_KEY}
      - DATABASE_URL=sqlite:////app/data/hcvai.db
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
      - DEFAULT_ADMIN_EMAIL=\${DEFAULT_ADMIN_EMAIL}
      - DEFAULT_ADMIN_PASSWORD=\${DEFAULT_ADMIN_PASSWORD}
      - GOOGLE_CLIENT_ID=\${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=\${GOOGLE_CLIENT_SECRET}
      - GOOGLE_REDIRECT_URI=\${GOOGLE_REDIRECT_URI}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build: ./hcv-frontend
    container_name: hcv-frontend
    expose:
      - "3000"
    restart: unless-stopped

  nginx:
    image: nginx:stable-alpine
    container_name: hcv-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./ssl:/etc/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
EOL

echo "Setup complete! Next steps:"
echo "1. Set your SECRET_KEY in an .env file in $PROJECT_DIR"
echo "2. Run 'docker compose up -d --build' inside $PROJECT_DIR"
echo "3. Run 'docker logs -f hcv-nginx | hcv-frontend | hcv-backend' to monitor the services"
echo "4. Run 'docker compose down -v' to stop the services"