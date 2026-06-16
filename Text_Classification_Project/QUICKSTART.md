# Quick Start Guide - Text Classification with TensorFlow

Get the Text Classification model up and running in minutes!

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **Git** (optional, for cloning the repository)

Check your Python installation:
```bash
python --version
```

## 🚀 Start in 3 Steps

### Step 1: Setup Environment

**Windows:**
```cmd
start.bat flask
```

**macOS/Linux:**
```bash
bash start.sh flask
```

This will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Check for model files
- ✅ Start the Flask API

### Step 2: Test the API

**In a new terminal:**
```bash
python test_api.py
```

This will run comprehensive tests on the API.

### Step 3: Access the Web Interface

**Flask REST API:**
- Open browser: http://localhost:5000

**Streamlit Web App (in another terminal):**
```bash
# Windows
start.bat streamlit

# macOS/Linux
bash start.sh streamlit
```
- Open browser: http://localhost:8501

---

## 📦 Installation Details

### Option 1: Automated Setup (Recommended)

**Windows:**
```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements_deployment.txt

# Run Flask API
python flask_app.py
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_deployment.txt

# Run Flask API
python flask_app.py
```

### Option 2: Docker Setup

**Requirements:**
- Docker Desktop installed: https://www.docker.com/products/docker-desktop

**Start both services:**
```bash
docker-compose up -d
```

**Check status:**
```bash
docker-compose ps
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop services:**
```bash
docker-compose down
```

---

## 🎯 Usage Examples

### Using Flask API

**Single Prediction:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple announces new iPhone"}'
```

**Batch Prediction:**
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

**Check Health:**
```bash
curl http://localhost:5000/health
```

### Using Python Client

```python
import requests

# Single prediction
response = requests.post('http://localhost:5000/predict',
    json={'text': 'Apple announces new iPhone'})
print(response.json())

# Batch prediction
response = requests.post('http://localhost:5000/predict-batch',
    json={'texts': ['Text 1', 'Text 2', 'Text 3']})
print(response.json())
```

### Using Test Client

```bash
python test_api.py
```

Runs comprehensive tests including:
- ✅ Health checks
- ✅ Model information
- ✅ Single predictions
- ✅ Batch predictions
- ✅ Edge cases
- ✅ Performance testing

---

## 🌐 Web Interface (Streamlit)

Access at: http://localhost:8501

### Features:
1. **Predict Tab**
   - Single text classification
   - Real-time predictions
   - Confidence visualization
   - Detailed analysis

2. **Batch Predict Tab**
   - Process multiple texts at once
   - CSV download of results
   - Progress bar

3. **Model Info Tab**
   - Architecture details
   - Model parameters
   - Layer information
   - Configuration

4. **Examples Tab**
   - Pre-loaded examples by category
   - Quick testing with one click

---

## 📊 Expected Output

### Prediction Response:
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
  "timestamp": "2026-06-16T10:30:00"
}
```

---

## 🛠️ Troubleshooting

### "Model files not found"
```bash
# Train the model first by running the notebook
jupyter notebook Text_Classification_with_TensorFlow.ipynb

# Or restore from backup if available
```

### "Port already in use"
```bash
# Flask (change port 5000)
python -c "import flask; flask.run(port=5001)"

# Streamlit (change port 8501)
streamlit run streamlit_app.py --server.port=8502
```

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements_deployment.txt --force-reinstall
```

### "NLTK data not found"
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### "API not responding"
```bash
# Check if Flask is running
curl http://localhost:5000/health

# Check logs for errors
python flask_app.py
```

---

## 📚 Documentation

For detailed information, see:

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Full deployment guide
- **[README.md](README.md)** - Project overview and architecture
- **[KAGGLE_GUIDE.md](KAGGLE_GUIDE.md)** - How to use real datasets
- **[Notebook](Text_Classification_with_TensorFlow.ipynb)** - Complete code walkthrough

---

## 🔑 Model Information

| Property | Value |
|----------|-------|
| Architecture | Bidirectional LSTM with Embeddings |
| Parameters | ~600K+ |
| Classes | 3 (Business, Sports, Science/Technology) |
| Max Length | 100 words |
| Embedding Dim | 128 |
| Dropout | 20-30% |

---

## ⚡ Quick Commands Reference

```bash
# Setup
python -m venv venv              # Create virtual environment
source venv/bin/activate         # Activate (macOS/Linux)
venv\Scripts\activate            # Activate (Windows)
pip install -r requirements_deployment.txt

# Run Applications
python flask_app.py              # Start Flask API
streamlit run streamlit_app.py   # Start Streamlit app
python test_api.py              # Test the API

# Docker
docker-compose build            # Build image
docker-compose up -d            # Start containers
docker-compose logs -f          # View logs
docker-compose down             # Stop containers

# Check Status
curl http://localhost:5000/health       # API health
curl http://localhost:5000/model-info   # Model info
```

---

## 🎓 Next Steps

1. **Test the API** - Run `python test_api.py` to verify everything works
2. **Explore the Web UI** - Open Streamlit at http://localhost:8501
3. **Make Predictions** - Use the API or web interface
4. **Deploy to Cloud** - See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud options
5. **Use Real Data** - See [KAGGLE_GUIDE.md](KAGGLE_GUIDE.md) for datasets

---

## 💡 Pro Tips

### Performance
- Use batch predictions for multiple texts
- Deploy on GPU for faster inference
- Use caching for repeated predictions

### Integration
- Use REST API for backend integration
- Use Python client for direct integration
- Webhook support available with Flask

### Monitoring
- Check logs regularly: `docker-compose logs`
- Monitor performance: `docker stats`
- Set up alerts for errors

---

## 🆘 Getting Help

**Check these resources in order:**
1. This Quick Start Guide
2. [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment instructions
3. [README.md](README.md) - Project documentation
4. Run the notebook: See complete implementation example
5. Check logs: `python flask_app.py` and `streamlit run streamlit_app.py`

---

## 📝 Project Structure

```
Text_Classification_Project/
├── Text_Classification_with_TensorFlow.ipynb    # Main notebook
├── text_classification.py                       # Standalone script
├── flask_app.py                                 # REST API
├── streamlit_app.py                             # Web interface
├── saved_models/                                # Model files
│   ├── text_classification_model.h5
│   ├── tokenizer.pickle
│   └── config.pickle
├── Dockerfile                                   # Docker configuration
├── docker-compose.yml                           # Multi-service setup
├── requirements.txt                             # Core dependencies
├── requirements_deployment.txt                  # Production dependencies
├── start.sh                                     # Linux/Mac startup script
├── start.bat                                    # Windows startup script
├── test_api.py                                  # API testing
├── README.md                                    # Project overview
├── DEPLOYMENT.md                                # Deployment guide
├── KAGGLE_GUIDE.md                              # Dataset guide
└── .gitignore                                   # Git configuration
```

---

**Happy classifying! 🎉**

For the latest updates and documentation, check the project repository.
