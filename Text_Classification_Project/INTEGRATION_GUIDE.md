# Integration Guide - Text Classification API

How to integrate the Text Classification model into your applications.

## 🔌 Integration Methods

Choose the method that best fits your use case:

| Method | Best For | Complexity |
|--------|----------|-----------|
| **REST API** | Backend services, microservices | Low |
| **Python Client** | Python applications | Very Low |
| **Docker** | Cloud deployment, scalability | Medium |
| **Streamlit** | Internal dashboards, demos | Low |
| **Direct Model Loading** | Custom integration, embedded | High |

---

## 1️⃣ REST API Integration (Recommended)

The easiest way to integrate - your app makes HTTP requests to the API.

### Setup

```bash
# Terminal 1: Start Flask API
python flask_app.py
# API running at: http://localhost:5000
```

### Python Integration

```python
import requests

# Single prediction
response = requests.post('http://localhost:5000/predict', json={
    'text': 'Apple announces new iPhone'
})

result = response.json()
print(result['prediction']['class_name'])  # Output: Business
print(result['prediction']['confidence'])   # Output: 0.95
```

### JavaScript/Node.js Integration

```javascript
// Single prediction
const response = await fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Apple announces new iPhone' })
});

const result = await response.json();
console.log(result.prediction.class_name); // Output: Business
```

### cURL Integration

```bash
# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple announces new iPhone"}'

# Batch prediction
curl -X POST http://localhost:5000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Text 1", "Text 2", "Text 3"]}'
```

### Error Handling

```python
import requests

try:
    response = requests.post(
        'http://localhost:5000/predict',
        json={'text': 'Your text here'},
        timeout=10
    )
    response.raise_for_status()  # Raise exception for bad status
    result = response.json()
    
    if result['status'] == 'success':
        print(result['prediction']['class_name'])
    else:
        print(f"Error: {result['error']}")
        
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Could not connect to API")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## 2️⃣ Python Client Library

Use the provided Python client for easy integration in Python projects.

### Installation

```python
# Copy api_client.py to your project
from api_client import TextClassificationClient

# Create client
client = TextClassificationClient('http://localhost:5000')
```

### Single Prediction

```python
# Simple prediction
result = client.predict('Apple announces new iPhone')
print(result['prediction']['class_name'])
```

### Batch Processing

```python
# Predict multiple texts
texts = ['Text 1', 'Text 2', 'Text 3']
results = client.predict_batch(texts)

for r in results['results']:
    print(f"{r['text']}: {r['prediction']}")
```

### Filtering

```python
# Get only business-related texts
business_texts = client.filter_by_class(texts, 'Business')
```

### Distribution Analysis

```python
# Analyze class distribution
distribution = client.get_class_distribution(texts)
print(distribution)
# Output: {'Business': 5, 'Sports': 3, 'Science/Technology': 2}
```

### Error Handling

```python
result = client.predict('Some text')

if 'error' in result:
    print(f"Prediction failed: {result['error']}")
else:
    print(f"Class: {result['prediction']['class_name']}")
```

---

## 3️⃣ Django Integration

Example: Add text classification to your Django application.

### Setup

```bash
pip install requests
```

### Create a Model

```python
# models.py
from django.db import models

class ClassifiedText(models.Model):
    original_text = models.TextField()
    predicted_class = models.CharField(max_length=50)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

### Create a Service

```python
# services.py
import requests
from django.conf import settings

class TextClassificationService:
    def __init__(self):
        self.api_url = getattr(settings, 'TEXT_CLASS_API_URL', 
                              'http://localhost:5000')
    
    def classify(self, text):
        """Classify text and return result"""
        try:
            response = requests.post(
                f'{self.api_url}/predict',
                json={'text': text},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}
    
    def classify_and_save(self, text):
        """Classify text and save to database"""
        from .models import ClassifiedText
        
        result = self.classify(text)
        
        if 'error' not in result:
            return ClassifiedText.objects.create(
                original_text=text,
                predicted_class=result['prediction']['class_name'],
                confidence=result['prediction']['confidence']
            )
        return None
```

### Use in Views

```python
# views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import TextClassificationService

class ClassifyView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        
        service = TextClassificationService()
        result = service.classify(text)
        
        if 'error' in result:
            return Response({'error': result['error']}, status=400)
        
        return Response(result)
```

### Django Settings

```python
# settings.py
TEXT_CLASS_API_URL = os.getenv(
    'TEXT_CLASS_API_URL',
    'http://localhost:5000'
)
```

---

## 4️⃣ FastAPI Integration

Create a wrapper API with FastAPI.

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class TextInput(BaseModel):
    text: str

class PredictionResult(BaseModel):
    text: str
    class_name: str
    confidence: float

@app.post("/classify", response_model=PredictionResult)
async def classify(input: TextInput):
    """Classify text using the Text Classification API"""
    try:
        response = requests.post(
            'http://localhost:5000/predict',
            json={'text': input.text},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        if result['status'] != 'success':
            raise HTTPException(status_code=400, 
                              detail=result.get('error'))
        
        return PredictionResult(
            text=result['text'],
            class_name=result['prediction']['class_name'],
            confidence=result['prediction']['confidence']
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=503, 
                          detail=f"Classification service error: {e}")

# Run with: uvicorn main:app --reload
```

---

## 5️⃣ Docker Integration

Integrate the containerized model into a larger application.

### docker-compose.yml with Other Services

```yaml
version: '3.8'

services:
  text-api:
    build: ./text-classification
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./text-classification/saved_models:/app/saved_models

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - text-api
    environment:
      - TEXT_CLASSIFICATION_API=http://text-api:5000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  database:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Service Communication

```python
# When running in Docker, use service name instead of localhost
API_URL = os.getenv('TEXT_CLASSIFICATION_API', 
                    'http://text-api:5000')

response = requests.post(f'{API_URL}/predict', 
                        json={'text': 'Your text'})
```

---

## 6️⃣ Streaming/Real-time Integration

Process text streams in real-time.

```python
# Stream processor
from api_client import TextClassificationClient
from queue import Queue
import threading

class StreamProcessor:
    def __init__(self):
        self.client = TextClassificationClient()
        self.queue = Queue()
        self.running = True
    
    def process_stream(self):
        """Process items from queue"""
        while self.running:
            item = self.queue.get()
            if item is None:
                break
            
            result = self.client.predict(item['text'])
            item['callback'](result)
    
    def add_text(self, text, callback):
        """Add text to processing queue"""
        self.queue.put({'text': text, 'callback': callback})
    
    def start(self):
        """Start processing thread"""
        thread = threading.Thread(target=self.process_stream)
        thread.start()
    
    def stop(self):
        """Stop processing"""
        self.running = False
        self.queue.put(None)

# Usage
processor = StreamProcessor()
processor.start()

def on_result(result):
    print(f"Result: {result['prediction']['class_name']}")

processor.add_text("Your text", on_result)
```

---

## 7️⃣ Caching Integration

Improve performance with caching.

```python
from functools import lru_cache
import hashlib
import requests

class CachedClassificationClient:
    def __init__(self, cache_size=1000):
        self.cache_size = cache_size
        self.cache = {}
    
    def _hash_text(self, text):
        """Create hash of text for caching"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def predict(self, text):
        """Predict with caching"""
        text_hash = self._hash_text(text)
        
        # Check cache
        if text_hash in self.cache:
            return self.cache[text_hash]
        
        # Make request
        response = requests.post(
            'http://localhost:5000/predict',
            json={'text': text}
        )
        result = response.json()
        
        # Cache result
        if len(self.cache) >= self.cache_size:
            # Remove oldest item
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[text_hash] = result
        return result

# Usage
client = CachedClassificationClient(cache_size=500)
result = client.predict("Apple announces new iPhone")  # API call
result = client.predict("Apple announces new iPhone")  # From cache
```

---

## 8️⃣ Async Integration

Use async/await for non-blocking requests.

```python
import aiohttp
import asyncio

class AsyncClassificationClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    async def predict(self, text):
        """Async single prediction"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{self.base_url}/predict',
                json={'text': text}
            ) as response:
                return await response.json()
    
    async def predict_batch(self, texts):
        """Async batch prediction"""
        tasks = [self.predict(text) for text in texts]
        return await asyncio.gather(*tasks)

# Usage
async def main():
    client = AsyncClassificationClient()
    
    texts = ['Text 1', 'Text 2', 'Text 3']
    results = await client.predict_batch(texts)
    
    for result in results:
        print(result['prediction']['class_name'])

asyncio.run(main())
```

---

## 🔐 Security Best Practices

### API Key Authentication

```python
# Add to Flask API
from functools import wraps

API_KEYS = {'your-secret-key-here'}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key not in API_KEYS:
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    # ... your code
```

### HTTPS in Production

```bash
# Use nginx with SSL
# See DEPLOYMENT.md for complete setup
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/predict', methods=['POST'])
@limiter.limit("100 per hour")
def predict():
    # ... your code
```

---

## 📊 Monitoring Integration

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    result = client.predict(text)
    logger.info(f"Prediction: {result['prediction']['class_name']}")
except Exception as e:
    logger.error(f"Prediction failed: {e}", exc_info=True)
```

### Metrics Collection

```python
from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.predictions = []
    
    def record_prediction(self, text, result):
        self.predictions.append({
            'timestamp': datetime.now(),
            'text_length': len(text),
            'class': result['prediction']['class_name'],
            'confidence': result['prediction']['confidence']
        })
    
    def get_stats(self):
        if not self.predictions:
            return {}
        
        classes = {}
        for p in self.predictions:
            classes[p['class']] = classes.get(p['class'], 0) + 1
        
        return {
            'total_predictions': len(self.predictions),
            'class_distribution': classes,
            'avg_confidence': sum(p['confidence'] 
                                 for p in self.predictions) / len(self.predictions)
        }
```

---

## ✅ Testing Integration

```python
import unittest
from unittest.mock import patch, MagicMock

class TestClassificationIntegration(unittest.TestCase):
    
    def setUp(self):
        self.client = TextClassificationClient()
    
    @patch('requests.post')
    def test_predict(self, mock_post):
        # Mock API response
        mock_post.return_value.json.return_value = {
            'prediction': {
                'class_name': 'Business',
                'confidence': 0.95
            }
        }
        
        result = self.client.predict('Apple news')
        self.assertEqual(result['prediction']['class_name'], 'Business')
    
    def test_api_available(self):
        """Test if API is available"""
        self.assertTrue(self.client.is_available())

if __name__ == '__main__':
    unittest.main()
```

---

## 🚀 Deployment Integration

### GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python test_api.py
      - name: Deploy to production
        run: docker-compose -f docker-compose.prod.yml up -d
```

---

## 📚 Common Integration Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Request-Response** | Single classification | Web form submission |
| **Batch Processing** | Bulk classification | CSV import |
| **Streaming** | Real-time processing | Event stream |
| **Webhook** | Async notification | Background job |
| **Cache Layer** | High frequency queries | Dashboard |

---

## 🎯 Next Steps

1. **Choose your integration method** from above
2. **Start with the REST API** (simplest)
3. **Use the Python client** for Python projects
4. **Deploy with Docker** for production
5. **Monitor and optimize** performance

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

**Need help?** Check QUICKSTART.md or run `python test_api.py` to verify setup.
