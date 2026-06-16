# Text Classification Model - Deployment Guide

Complete guide for deploying the Text Classification model to production.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Streamlit Web App](#streamlit-web-app)
3. [Flask REST API](#flask-rest-api)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [API Documentation](#api-documentation)
7. [Monitoring & Troubleshooting](#monitoring--troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- TensorFlow 2.10+
- Flask & Streamlit installed
- Trained model files (in `saved_models/` directory)

### Installation

1. **Clone/Download the project**
```bash
cd Text_Classification_Project
```

2. **Install dependencies**
```bash
pip install -r requirements_deployment.txt
```

3. **Verify model files exist**
```bash
ls -la saved_models/
# Should contain:
# - text_classification_model.h5
# - tokenizer.pickle
# - config.pickle
```

---

## 🎨 Streamlit Web App

### Local Deployment

The easiest way to deploy - runs in your browser with a beautiful UI.

#### Start the App
```bash
streamlit run streamlit_app.py
```

#### Access
- **Local:** http://localhost:8501
- **Network:** http://<your-ip>:8501

#### Features
- ✅ Single text classification
- ✅ Batch text processing
- ✅ Real-time predictions
- ✅ Confidence visualization
- ✅ Model information
- ✅ Example gallery
- ✅ CSV export

#### Streamlit Cloud Deployment (FREE)

1. **Push to GitHub**
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `your-username/text-classification`
   - Select branch: `main`
   - Set main file path: `streamlit_app.py`
   - Click Deploy

3. **Your app is live at:** `https://<username>-text-classification.streamlit.app`

#### Configuration
Create `~/.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true
maxUploadSize = 200
runOnSave = true

[client]
showErrorDetails = true
```

---

## 🔌 Flask REST API

### Local Deployment

Production-grade REST API for integration with other systems.

#### Start the Server
```bash
python flask_app.py
```

#### Access
- **API:** http://localhost:5000
- **Swagger Docs:** http://localhost:5000/docs (with flask-swagger)

#### API Endpoints

**1. Health Check**
```bash
curl http://localhost:5000/health
```

**2. Single Prediction**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple announces new iPhone"}'
```

**3. Batch Prediction**
```bash
curl -X POST http://localhost:5000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Stock market rises today",
      "Football championship results",
      "New scientific discovery"
    ]
  }'
```

#### Response Format
```json
{
  "text": "Apple announces new iPhone",
  "cleaned_text": "apple announces iphone",
  "prediction": {
    "class": 0,
    "class_name": "Business",
    "confidence": 0.95
  },
  "probabilities": {
    "Business": 0.95,
    "Sports": 0.03,
    "Science/Technology": 0.02
  },
  "status": "success",
  "timestamp": "2026-06-16T10:30:00.000000"
}
```

#### Production Deployment

Use Gunicorn for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

---

## 🐳 Docker Deployment

### Build & Run Locally

#### 1. Build Docker Image
```bash
docker build -t text-classification:latest .
```

#### 2. Run Flask API
```bash
docker run -d \
  --name text-api \
  -p 5000:5000 \
  -v $(pwd)/saved_models:/app/saved_models \
  text-classification:latest \
  python flask_app.py
```

#### 3. Run Streamlit App
```bash
docker run -d \
  --name text-streamlit \
  -p 8501:8501 \
  -v $(pwd)/saved_models:/app/saved_models \
  text-classification:latest \
  streamlit run streamlit_app.py
```

### Docker Compose (Both Services)

#### Start Both Services
```bash
docker-compose up -d
```

#### Check Status
```bash
docker-compose ps
```

#### View Logs
```bash
docker-compose logs -f flask-api
docker-compose logs -f streamlit-app
```

#### Stop Services
```bash
docker-compose down
```

#### Access Services
- **API:** http://localhost:5000
- **Streamlit:** http://localhost:8501

---

## ☁️ Cloud Deployment

### AWS EC2 Deployment

#### 1. Launch EC2 Instance
```bash
# Select Ubuntu 20.04 LTS
# Security group: Allow ports 5000, 8501
```

#### 2. SSH into Instance
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### 3. Setup Environment
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & dependencies
sudo apt install -y python3-pip python3-venv
python3 -m venv env
source env/bin/activate

# Clone project
git clone your-repo-url
cd Text_Classification_Project
pip install -r requirements_deployment.txt
```

#### 4. Run Application
```bash
# Flask API with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app

# Or Streamlit
streamlit run streamlit_app.py
```

#### 5. Setup Nginx Reverse Proxy
```bash
sudo apt install nginx
```

Create `/etc/nginx/sites-available/default`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo systemctl restart nginx
```

### Google Cloud Run Deployment

#### 1. Setup Google Cloud CLI
```bash
curl https://sdk.cloud.google.com | bash
gcloud init
gcloud auth login
```

#### 2. Create `.gcloudignore`
```
__pycache__
*.pyc
.git
.gitignore
.venv
env
```

#### 3. Deploy
```bash
# Flask API
gcloud run deploy text-classification-api \
  --source . \
  --entry-point=flask_app \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 300

# Streamlit
gcloud run deploy text-classification-web \
  --source . \
  --entry-point='streamlit run streamlit_app.py' \
  --platform managed \
  --region us-central1 \
  --memory 2Gi
```

### Heroku Deployment

#### 1. Install Heroku CLI
```bash
curl https://cli.heroku.com/install.sh | sh
```

#### 2. Create Procfile
```
web: gunicorn flask_app:app
```

#### 3. Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku logs --tail
```

---

## 📚 API Documentation

### Request Headers
```
Content-Type: application/json
Accept: application/json
```

### Single Prediction Request
```json
{
  "text": "string (required) - Text to classify"
}
```

### Single Prediction Response (Success)
```json
{
  "text": "Apple announces new iPhone",
  "cleaned_text": "apple announces iphone",
  "prediction": {
    "class": 0,
    "class_name": "Business",
    "confidence": 0.95
  },
  "probabilities": {
    "Business": 0.95,
    "Sports": 0.03,
    "Science/Technology": 0.02
  },
  "status": "success",
  "timestamp": "2026-06-16T10:30:00.000000"
}
```

### Error Response
```json
{
  "error": "Error type",
  "message": "Error description",
  "status": "error"
}
```

### Batch Prediction Request
```json
{
  "texts": [
    "Text 1",
    "Text 2",
    "Text 3"
  ]
}
```

### Batch Prediction Response
```json
{
  "total": 3,
  "results": [
    {
      "text": "Text 1",
      "prediction": "Business",
      "confidence": 0.92
    },
    {
      "text": "Text 2",
      "prediction": "Sports",
      "confidence": 0.88
    },
    {
      "text": "Text 3",
      "prediction": "Science/Technology",
      "confidence": 0.91
    }
  ],
  "status": "success",
  "timestamp": "2026-06-16T10:30:00.000000"
}
```

---

## 🛠️ Monitoring & Troubleshooting

### Common Issues

#### 1. Model Files Not Found
**Error:** `FileNotFoundError: saved_models/text_classification_model.h5`

**Solution:**
```bash
# Ensure model files exist
ls -la saved_models/

# If missing, train the model first by running the notebook
jupyter notebook Text_Classification_with_TensorFlow.ipynb
```

#### 2. Out of Memory
**Error:** `MemoryError` or `ResourceExhausted`

**Solution:**
```bash
# For Docker, increase memory
docker run -m 4g -d ...

# For Kubernetes
resources:
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

#### 3. Slow Predictions
**Solution:**
- Use batch predictions instead of single
- Deploy on GPU-enabled machine
- Implement caching
- Use model quantization

#### 4. NLTK Data Missing
**Error:** `LookupError: Resource punkt not found`

**Solution:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Performance Monitoring

#### Flask
```python
from flask import request
import time

@app.before_request
def log_request():
    request.start_time = time.time()

@app.after_request
def log_response(response):
    duration = time.time() - request.start_time
    print(f"Request took {duration:.2f}s")
    return response
```

#### Docker Logs
```bash
# View logs
docker logs text-api

# Follow logs
docker logs -f text-api

# Last N lines
docker logs --tail 100 text-api
```

#### Health Checks
```bash
# API health
curl http://localhost:5000/health

# Continuous monitoring
watch -n 5 'curl -s http://localhost:5000/health | jq'
```

### Load Testing

#### Using Apache Bench
```bash
# Single request per second, 1000 total
ab -n 1000 -c 10 http://localhost:5000/health
```

#### Using Locust
```python
# locustfile.py
from locust import HttpUser, task, between
import json

class User(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict(self):
        self.client.post("/predict", json={
            "text": "Stock market rises today"
        })
```

```bash
locust -f locustfile.py --host=http://localhost:5000
```

---

## 📊 Environment Variables

Create `.env` file:
```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key

# TensorFlow
TF_CPP_MIN_LOG_LEVEL=2
TF_FORCE_GPU_ALLOW_GROWTH=true

# Streamlit
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

---

## ✅ Deployment Checklist

- [ ] Model files exist in `saved_models/`
- [ ] Dependencies installed: `pip install -r requirements_deployment.txt`
- [ ] Model works locally: Run notebook cells
- [ ] Test Flask API: `curl http://localhost:5000/health`
- [ ] Test Streamlit: Access `http://localhost:8501`
- [ ] Docker image builds: `docker build -t text-classification .`
- [ ] Environment variables configured
- [ ] HTTPS/SSL certificates configured (for production)
- [ ] Monitoring & logging setup
- [ ] Backup of model files
- [ ] Documentation updated
- [ ] Team trained on deployment

---

## 📞 Support

For issues or questions:
- Check logs: `docker logs container-name`
- Review error messages carefully
- Test with curl before using web UI
- Check system resources: `docker stats`

---

**Deployment Guide Version:** 1.0
**Last Updated:** 2026-06-16
