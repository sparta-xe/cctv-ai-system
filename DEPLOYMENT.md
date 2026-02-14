# Deployment Guide

Complete guide for deploying the AI CCTV Intelligence System to production.

## 🚀 Deployment Options

### 1. Local Server Deployment

**Best for:** Development, testing, small-scale deployments

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python main.py

# Server runs on http://localhost:8000
```

### 2. Docker Deployment

**Best for:** Containerized deployments, cloud platforms

```bash
# Build image
docker build -t cctv-ai-system .

# Run container
docker run -p 8000:8000 -v $(pwd)/storage:/app/storage cctv-ai-system

# Or use docker-compose
docker-compose up -d
```

### 3. Cloud Deployment

#### AWS EC2

```bash
# 1. Launch EC2 instance (t3.large or better)
# 2. SSH into instance
ssh -i key.pem ubuntu@<instance-ip>

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# 4. Clone repository
git clone https://github.com/sparta-xe/cctv-ai-system.git
cd cctv-ai-system

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install requirements
pip install -r requirements.txt

# 7. Run with systemd (production)
sudo nano /etc/systemd/system/cctv-ai.service
```

**systemd service file:**
```ini
[Unit]
Description=AI CCTV Intelligence System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cctv-ai-system
Environment="PATH=/home/ubuntu/cctv-ai-system/venv/bin"
ExecStart=/home/ubuntu/cctv-ai-system/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cctv-ai
sudo systemctl start cctv-ai
sudo systemctl status cctv-ai
```

#### Azure App Service

```bash
# 1. Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. Login
az login

# 3. Create resource group
az group create --name cctv-rg --location eastus

# 4. Create App Service plan
az appservice plan create --name cctv-plan --resource-group cctv-rg --sku B2 --is-linux

# 5. Create web app
az webapp create --resource-group cctv-rg --plan cctv-plan --name cctv-ai-app --runtime "PYTHON:3.9"

# 6. Deploy code
az webapp up --name cctv-ai-app --resource-group cctv-rg
```

#### Google Cloud Run

```bash
# 1. Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# 2. Initialize
gcloud init

# 3. Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/cctv-ai
gcloud run deploy cctv-ai --image gcr.io/PROJECT_ID/cctv-ai --platform managed --region us-central1 --allow-unauthenticated
```

## 🔒 Production Configuration

### 1. Environment Variables

Create `.env` file:

```bash
# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Storage
STORAGE_PATH=/var/lib/cctv-ai/storage
MAX_UPLOAD_SIZE=524288000  # 500MB

# Performance
FRAME_SKIP=5
MAX_FRAME_WIDTH=640
DETECTION_CONFIDENCE=0.5

# Database (if using external DB)
DATABASE_URL=postgresql://user:pass@localhost/cctv_db

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0
```

### 2. Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/cctv-ai

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Max upload size
    client_max_body_size 500M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts for long uploads
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }

    # Static files
    location /static/ {
        alias /var/www/cctv-ai/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /storage/ {
        alias /var/www/cctv-ai/storage/;
        expires 1h;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/cctv-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## 📊 Performance Optimization

### 1. Use Gunicorn (Production WSGI)

```bash
# Install
pip install gunicorn uvicorn[standard]

# Run with multiple workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 600
```

### 2. Redis Caching

```python
# Add to requirements.txt
redis==4.5.1

# Update main.py
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=100)
def cached_search(query):
    # Cache search results
    pass
```

### 3. Database (PostgreSQL)

For production, use PostgreSQL instead of in-memory storage:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb cctv_db
sudo -u postgres createuser cctv_user

# Update database.py to use SQLAlchemy
pip install sqlalchemy psycopg2-binary
```

## 🔐 Security Hardening

### 1. Authentication

Replace simple auth with JWT:

```python
# Install
pip install python-jose[cryptography] passlib[bcrypt]

# Update auth.py
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
```

### 2. Rate Limiting

```python
# Install
pip install slowapi

# Add to main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/upload/")
@limiter.limit("5/hour")
async def upload_video(request: Request, file: UploadFile):
    pass
```

### 3. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 📈 Monitoring

### 1. Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)
```

### 2. Health Checks

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0"
    }
```

### 3. Prometheus Metrics

```bash
pip install prometheus-fastapi-instrumentator

# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🔄 Backup Strategy

### 1. Database Backup

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/var/backups/cctv-ai"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump cctv_db > $BACKUP_DIR/db_$DATE.sql

# Backup storage
tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /var/lib/cctv-ai/storage

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

### 2. Cron Job

```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /usr/local/bin/backup-cctv.sh
```

## 🚨 Troubleshooting

### High Memory Usage
- Reduce `MAX_FRAME_WIDTH`
- Increase `FRAME_SKIP`
- Add swap space
- Use external storage (S3, Azure Blob)

### Slow Processing
- Use GPU instance (AWS p3, Azure NC series)
- Increase worker count
- Implement job queue (Celery + Redis)

### Connection Timeouts
- Increase nginx timeouts
- Increase gunicorn timeout
- Use async processing for uploads

## 📞 Support

For deployment issues:
- Check logs: `sudo journalctl -u cctv-ai -f`
- Monitor resources: `htop`, `nvidia-smi`
- Review nginx logs: `/var/log/nginx/error.log`

---

**Production Checklist:**
- [ ] Environment variables configured
- [ ] SSL certificate installed
- [ ] Nginx reverse proxy setup
- [ ] Firewall configured
- [ ] Backups automated
- [ ] Monitoring enabled
- [ ] Rate limiting active
- [ ] Authentication secured
- [ ] Logs configured
- [ ] Health checks working
