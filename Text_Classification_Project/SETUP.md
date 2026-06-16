# Project Setup Guide

Complete setup instructions for the Text Classification with TensorFlow project.

## 🚀 Quick Setup (5 minutes)

### Windows
```cmd
start.bat flask
```

### macOS/Linux
```bash
bash start.sh flask
```

---

## 🔧 Manual Setup

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)
- Git (for version control)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Punith-18-eng/user_profile_app.git
cd Text_Classification_Project
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements_deployment.txt
```

### Step 4: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional)
```

### Step 5: Run the Application

#### Option A: Flask API Only
```bash
python flask_app.py
# API available at: http://localhost:5000
```

#### Option B: Streamlit Web App
```bash
streamlit run streamlit_app.py
# Web app available at: http://localhost:8501
```

#### Option C: Both with Docker
```bash
docker-compose up -d
# API at http://localhost:5000
# Web at http://localhost:8501
```

---

## 📊 Training the Model

To train the model before running the API:

```bash
jupyter notebook Text_Classification_with_TensorFlow.ipynb
```

Run all cells to:
1. Load/create training data
2. Preprocess text
3. Build and train the Bi-LSTM model
4. Evaluate performance
5. Save model files to `saved_models/`

**Required model files:**
- `saved_models/text_classification_model.h5`
- `saved_models/tokenizer.pickle`
- `saved_models/config.pickle`

---

## 🧪 Testing

### Run API Tests
```bash
python test_api.py
```

### Test Single Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple announces new iPhone"}'
```

### Test with Python Client
```bash
python -c "
from api_client import TextClassificationClient
client = TextClassificationClient()
result = client.predict('Your text here')
print(result)
"
```

---

## 🐳 Docker Setup

### Build Image
```bash
docker build -t text-classification:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Run Individual Service
```bash
docker run -p 5000:5000 text-classification:latest python flask_app.py
```

---

## 📁 Project Structure

```
Text_Classification_Project/
├── Text_Classification_with_TensorFlow.ipynb    # Main notebook
├── flask_app.py                                 # REST API
├── streamlit_app.py                             # Web interface
├── text_classification.py                       # Standalone script
├── api_client.py                                # Python client
├── test_api.py                                  # Tests
├── saved_models/                                # Model files (after training)
├── logs/                                        # Application logs
├── Dockerfile                                   # Container config
├── docker-compose.yml                           # Multi-service config
├── requirements.txt                             # Core dependencies
├── requirements_deployment.txt                  # Production deps
├── requirements-dev.txt                         # Development deps
├── start.sh                                     # Linux/Mac startup
├── start.bat                                    # Windows startup
├── README.md                                    # Project overview
├── QUICKSTART.md                                # Quick start guide
├── DEPLOYMENT.md                                # Cloud deployment
├── INTEGRATION_GUIDE.md                         # Integration patterns
├── KAGGLE_GUIDE.md                              # Dataset guide
├── .env.example                                 # Env template
└── .gitignore                                   # Git config
```

---

## 🔑 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-key-change-in-production

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# TensorFlow
TF_CPP_MIN_LOG_LEVEL=2
```

---

## 📦 Dependencies

### Core (ML & Data)
- TensorFlow 2.10+
- Keras 2.10+
- NumPy, Pandas
- scikit-learn, NLTK

### Web & API
- Flask 2.0+
- Streamlit 1.20+
- Requests

### Deployment
- Docker
- Gunicorn (WSGI server)

See `requirements.txt` and `requirements_deployment.txt` for full lists.

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'tensorflow'"
```bash
pip install tensorflow keras --upgrade
```

### "Port 5000 already in use"
```bash
# Change port in flask_app.py or use environment variable
export FLASK_PORT=5001
python flask_app.py
```

### "Model files not found"
Train the model first by running the Jupyter notebook:
```bash
jupyter notebook Text_Classification_with_TensorFlow.ipynb
```

### "NLTK data not found"
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### "Docker daemon not running"
Start Docker Desktop or Docker service before running docker-compose.

---

## 📚 Next Steps

1. **Read QUICKSTART.md** for 3-step setup
2. **Follow DEPLOYMENT.md** for cloud deployment
3. **Check INTEGRATION_GUIDE.md** for integration patterns
4. **Run test_api.py** to verify setup
5. **Train model** using the Jupyter notebook

---

## 🔗 Useful Links

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras Guide](https://keras.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Model files present in saved_models/ (after training)
- [ ] Flask API starts without errors
- [ ] Streamlit app loads
- [ ] API responds to /health endpoint
- [ ] Test suite passes

---

## 💡 Tips

- Use `start.sh` or `start.bat` for automated setup
- Always activate virtual environment before working
- Check logs for debugging issues
- Use Docker for consistent environments
- Keep .env file with secrets out of version control

---

**For detailed instructions, see individual documentation files.**
