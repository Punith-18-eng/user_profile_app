"""
Flask REST API for Text Classification
Run with: python flask_app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
from datetime import datetime
from functools import wraps
import json

app = Flask(__name__)
CORS(app)

# Load model and configuration
try:
    model = keras.models.load_model('saved_models/text_classification_model.h5')
    with open('saved_models/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('saved_models/config.pickle', 'rb') as handle:
        config = pickle.load(handle)
    
    MAX_LENGTH = config['MAX_LENGTH']
    label_names = config['label_names']
    num_classes = config['num_classes']
    model_loaded = True
except Exception as e:
    model_loaded = False
    error_msg = str(e)

# Text cleaning function
def clean_text(text):
    """Clean and preprocess text"""
    import re
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import nltk
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    try:
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
        cleaned_text = ' '.join(tokens)
    except:
        cleaned_text = text
    
    return cleaned_text

# Error handler
def check_model_loaded(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not model_loaded:
            return jsonify({
                'error': 'Model not loaded',
                'message': error_msg,
                'status': 'error'
            }), 500
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """API Home"""
    return jsonify({
        'name': 'Text Classification API',
        'version': '1.0',
        'status': 'running' if model_loaded else 'error',
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'GET /model-info': 'Model information',
            'POST /predict': 'Predict single text',
            'POST /predict-batch': 'Predict multiple texts'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if model_loaded else 'unhealthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/model-info', methods=['GET'])
@check_model_loaded
def model_info():
    """Get model information"""
    return jsonify({
        'architecture': 'Bidirectional LSTM',
        'parameters': int(model.count_params()),
        'vocab_size': config.get('MAX_FEATURES', 5000),
        'max_length': MAX_LENGTH,
        'embedding_dim': config.get('EMBEDDING_DIM', 128),
        'num_classes': num_classes,
        'classes': dict(label_names),
        'status': 'ready'
    })

@app.route('/predict', methods=['POST'])
@check_model_loaded
def predict():
    """Single text prediction endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Please provide "text" field',
                'status': 'error'
            }), 400
        
        text = data['text']
        
        if not isinstance(text, str) or len(text.strip()) == 0:
            return jsonify({
                'error': 'Invalid text',
                'message': 'Text must be a non-empty string',
                'status': 'error'
            }), 400
        
        # Clean and process text
        cleaned_text = clean_text(text)
        
        # Tokenize and pad
        sequence = tokenizer.texts_to_sequences([cleaned_text])
        padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
        
        # Get predictions
        predictions = model.predict(padded, verbose=0)[0]
        pred_class = int(np.argmax(predictions))
        confidence = float(predictions[pred_class])
        
        # Build response
        result = {
            'text': text,
            'cleaned_text': cleaned_text,
            'prediction': {
                'class': pred_class,
                'class_name': label_names[pred_class],
                'confidence': confidence
            },
            'probabilities': {
                label_names[i]: float(predictions[i])
                for i in range(num_classes)
            },
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Prediction error',
            'message': str(e),
            'status': 'error'
        }), 500

@app.route('/predict-batch', methods=['POST'])
@check_model_loaded
def predict_batch():
    """Batch text prediction endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Please provide "texts" field as a list',
                'status': 'error'
            }), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({
                'error': 'Invalid format',
                'message': '"texts" must be a list',
                'status': 'error'
            }), 400
        
        if len(texts) == 0:
            return jsonify({
                'error': 'Empty list',
                'message': 'Please provide at least one text',
                'status': 'error'
            }), 400
        
        if len(texts) > 1000:
            return jsonify({
                'error': 'Batch too large',
                'message': 'Maximum 1000 texts per request',
                'status': 'error'
            }), 400
        
        # Process texts
        results = []
        for text in texts:
            if not isinstance(text, str) or len(text.strip()) == 0:
                continue
            
            # Clean and process
            cleaned_text = clean_text(text)
            sequence = tokenizer.texts_to_sequences([cleaned_text])
            padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
            
            # Get predictions
            predictions = model.predict(padded, verbose=0)[0]
            pred_class = int(np.argmax(predictions))
            confidence = float(predictions[pred_class])
            
            results.append({
                'text': text,
                'prediction': label_names[pred_class],
                'confidence': confidence
            })
        
        return jsonify({
            'total': len(results),
            'results': results,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Batch prediction error',
            'message': str(e),
            'status': 'error'
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return jsonify({
        'error': 'Server error',
        'message': 'An internal server error occurred',
        'status': 'error'
    }), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("TEXT CLASSIFICATION API - FLASK SERVER")
    print("=" * 70)
    
    if model_loaded:
        print("✓ Model loaded successfully")
        print(f"✓ Total parameters: {model.count_params():,}")
        print(f"✓ Number of classes: {num_classes}")
        print("\n🚀 Starting Flask server...")
        print("📍 API available at: http://localhost:5000")
        print("\n📚 Documentation:")
        print("  - GET  /                      - API information")
        print("  - GET  /health                - Health check")
        print("  - GET  /model-info            - Model information")
        print("  - POST /predict               - Single prediction")
        print("  - POST /predict-batch         - Batch prediction")
        print("\n" + "=" * 70 + "\n")
        
        # Run development server
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load model")
        print(f"Error: {error_msg}")
        print("\nPlease ensure model files exist in 'saved_models/' directory:")
        print("  - saved_models/text_classification_model.h5")
        print("  - saved_models/tokenizer.pickle")
        print("  - saved_models/config.pickle")
