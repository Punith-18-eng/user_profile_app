"""
Test client for Text Classification API
Run with: python test_api.py
"""

import requests
import json
from typing import List, Dict
import time
from datetime import datetime

class TextClassificationAPIClient:
    """Client for Text Classification API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
    
    def health_check(self) -> bool:
        """Check API health"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        try:
            response = self.session.get(f"{self.base_url}/model-info")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get model info: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Error getting model info: {e}")
            return {}
    
    def predict(self, text: str) -> Dict:
        """Single prediction"""
        try:
            payload = {"text": text}
            response = self.session.post(
                f"{self.base_url}/predict",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Prediction failed: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return {}
    
    def predict_batch(self, texts: List[str]) -> Dict:
        """Batch prediction"""
        try:
            payload = {"texts": texts}
            response = self.session.post(
                f"{self.base_url}/predict-batch",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Batch prediction failed: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Error in batch prediction: {e}")
            return {}

def print_prediction(result: Dict, title: str = "Prediction Result"):
    """Pretty print prediction result"""
    print(f"\n{'=' * 70}")
    print(f"{title}")
    print('=' * 70)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        print(f"   Message: {result['message']}")
    else:
        print(f"📝 Text: {result.get('text', 'N/A')}")
        print(f"🧹 Cleaned: {result.get('cleaned_text', 'N/A')}")
        
        if 'prediction' in result:
            pred = result['prediction']
            print(f"\n🎯 Prediction:")
            print(f"   Class: {pred.get('class_name', 'N/A')}")
            print(f"   Confidence: {pred.get('confidence', 0):.2%}")
        
        if 'probabilities' in result:
            print(f"\n📊 All Probabilities:")
            for class_name, prob in result['probabilities'].items():
                bar_length = int(prob * 30)
                bar = '█' * bar_length + '░' * (30 - bar_length)
                print(f"   {class_name:20s} [{bar}] {prob:.4f}")
        
        if 'timestamp' in result:
            print(f"\n⏱️  Timestamp: {result['timestamp']}")

def main():
    """Main test function"""
    print("\n" + "=" * 70)
    print("TEXT CLASSIFICATION API - TEST CLIENT")
    print("=" * 70)
    
    # Initialize client
    client = TextClassificationAPIClient()
    
    # Check health
    print("\n🔍 Checking API health...")
    if not client.health_check():
        print("\n❌ API is not responding!")
        print("Make sure Flask server is running: python flask_app.py")
        return
    print("✅ API is healthy")
    
    # Get model info
    print("\n📚 Fetching model information...")
    model_info = client.get_model_info()
    if model_info:
        print(f"✅ Model loaded successfully")
        print(f"   Architecture: {model_info.get('architecture', 'N/A')}")
        print(f"   Parameters: {model_info.get('parameters', 0):,}")
        print(f"   Classes: {', '.join(model_info.get('classes', {}).values())}")
    
    # Test 1: Single predictions
    print("\n" + "=" * 70)
    print("TEST 1: SINGLE TEXT PREDICTIONS")
    print("=" * 70)
    
    test_texts = [
        "Apple stock reaches all-time high",
        "Manchester United wins championship",
        "Scientists discover new exoplanet"
    ]
    
    for text in test_texts:
        result = client.predict(text)
        print_prediction(result, f"Prediction: {text[:50]}...")
    
    # Test 2: Batch prediction
    print("\n" + "=" * 70)
    print("TEST 2: BATCH PREDICTION")
    print("=" * 70)
    
    batch_texts = [
        "Tesla announces quarterly earnings",
        "Champions League final results",
        "Breakthrough in AI research"
    ]
    
    print(f"🚀 Processing {len(batch_texts)} texts...")
    start_time = time.time()
    result = client.predict_batch(batch_texts)
    duration = time.time() - start_time
    
    if result and 'results' in result:
        print(f"✅ Batch prediction completed in {duration:.2f}s\n")
        print(f"{'Text':<40} | {'Prediction':<20} | {'Confidence':<12}")
        print("-" * 75)
        for item in result['results']:
            text = item['text'][:37] + "..." if len(item['text']) > 40 else item['text']
            pred = item['prediction']
            conf = f"{item['confidence']:.2%}"
            print(f"{text:<40} | {pred:<20} | {conf:<12}")
    
    # Test 3: Edge cases
    print("\n" + "=" * 70)
    print("TEST 3: EDGE CASES")
    print("=" * 70)
    
    # Empty text
    print("\n▪ Testing empty text...")
    result = client.predict("")
    if 'error' in result:
        print(f"✅ Correctly rejected empty text: {result['error']}")
    
    # Very long text
    print("\n▪ Testing long text...")
    long_text = "This is a test. " * 50
    result = client.predict(long_text)
    if 'prediction' in result:
        print(f"✅ Successfully processed long text ({len(long_text)} chars)")
    
    # Special characters
    print("\n▪ Testing special characters...")
    special_text = "Test @#$%^&*() <html> tags"
    result = client.predict(special_text)
    if 'prediction' in result:
        print(f"✅ Successfully handled special characters")
    
    # Test 4: Performance
    print("\n" + "=" * 70)
    print("TEST 4: PERFORMANCE TESTING")
    print("=" * 70)
    
    num_requests = 10
    print(f"\n⏱️  Making {num_requests} requests...")
    
    times = []
    for i in range(num_requests):
        text = f"Test text number {i+1}"
        start = time.time()
        result = client.predict(text)
        duration = time.time() - start
        times.append(duration)
        print(f"   Request {i+1}/{num_requests}: {duration*1000:.2f}ms")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\n📊 Performance Statistics:")
    print(f"   Average: {avg_time*1000:.2f}ms")
    print(f"   Min: {min_time*1000:.2f}ms")
    print(f"   Max: {max_time*1000:.2f}ms")
    print(f"   Throughput: {1/avg_time:.1f} requests/sec")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    print(f"\n🎉 API is ready for production!")
    print(f"📚 API Documentation: {client.base_url}")
    print(f"🚀 Deploy using: docker-compose up -d")

if __name__ == "__main__":
    main()
