"""
Text Classification API - Python Client
Example usage for integrating the API into your application
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TextClassificationClient:
    """
    Python client for Text Classification API
    
    Example:
        >>> client = TextClassificationClient('http://localhost:5000')
        >>> result = client.predict('Apple announces new iPhone')
        >>> print(result['prediction']['class_name'])
        'Business'
    """
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 30):
        """
        Initialize the client
        
        Args:
            base_url: API base URL (default: http://localhost:5000)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
        
        logger.info(f"Initialized client for {self.base_url}")
    
    def is_available(self) -> bool:
        """
        Check if API is available
        
        Returns:
            True if API is responding, False otherwise
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API not available: {e}")
            return False
    
    def get_model_info(self) -> Dict:
        """
        Get model information
        
        Returns:
            Dictionary with model details
        """
        try:
            response = self.session.get(
                f"{self.base_url}/model-info",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get model info: {e}")
            return {}
    
    def predict(self, text: str) -> Dict:
        """
        Predict class for a single text
        
        Args:
            text: Text to classify
        
        Returns:
            Dictionary with prediction results:
            {
                'text': original text,
                'cleaned_text': preprocessed text,
                'prediction': {
                    'class': int,
                    'class_name': str,
                    'confidence': float
                },
                'probabilities': {
                    'class_name': confidence_score
                }
            }
        
        Example:
            >>> result = client.predict('Apple stock rises today')
            >>> print(result['prediction']['class_name'])
            'Business'
            >>> print(result['prediction']['confidence'])
            0.95
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            payload = {"text": text}
            response = self.session.post(
                f"{self.base_url}/predict",
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Prediction error: {e}")
            return {"error": str(e), "status": "error"}
    
    def predict_batch(
        self,
        texts: List[str],
        return_confidences: bool = True
    ) -> Dict:
        """
        Predict classes for multiple texts
        
        Args:
            texts: List of texts to classify (max 1000)
            return_confidences: Include confidence scores
        
        Returns:
            Dictionary with batch results:
            {
                'total': number of texts,
                'results': [
                    {
                        'text': original,
                        'prediction': class_name,
                        'confidence': score
                    },
                    ...
                ]
            }
        
        Example:
            >>> texts = ['Apple news', 'Game result', 'Science discovery']
            >>> results = client.predict_batch(texts)
            >>> for r in results['results']:
            ...     print(f"{r['text']}: {r['prediction']}")
            Apple news: Business
            Game result: Sports
            Science discovery: Science/Technology
        """
        try:
            if not texts:
                raise ValueError("Texts list cannot be empty")
            
            if len(texts) > 1000:
                raise ValueError("Maximum 1000 texts per request")
            
            payload = {"texts": texts}
            response = self.session.post(
                f"{self.base_url}/predict-batch",
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Batch prediction error: {e}")
            return {"error": str(e), "status": "error"}
    
    def predict_with_details(self, text: str) -> Optional[Dict]:
        """
        Get detailed prediction information
        
        Returns:
            Dictionary with detailed results or None on error
        """
        result = self.predict(text)
        
        if "error" in result:
            return None
        
        return {
            "original_text": result.get("text", ""),
            "cleaned_text": result.get("cleaned_text", ""),
            "predicted_class": result["prediction"]["class"],
            "predicted_name": result["prediction"]["class_name"],
            "confidence": result["prediction"]["confidence"],
            "all_probabilities": result.get("probabilities", {}),
            "timestamp": result.get("timestamp", "")
        }
    
    def get_top_predictions(
        self,
        text: str,
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Get top K predictions sorted by confidence
        
        Args:
            text: Text to classify
            top_k: Number of top predictions to return
        
        Returns:
            List of (class_name, confidence) tuples
        """
        result = self.predict(text)
        
        if "error" in result or "probabilities" not in result:
            return []
        
        predictions = [
            (name, prob)
            for name, prob in result["probabilities"].items()
        ]
        
        # Sort by confidence descending
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return predictions[:top_k]
    
    def bulk_classify(
        self,
        texts: List[str],
        chunk_size: int = 100
    ) -> List[Dict]:
        """
        Classify many texts by chunking into batches
        
        Args:
            texts: List of texts to classify
            chunk_size: Size of each batch (max 1000)
        
        Returns:
            Flattened list of results
        """
        if chunk_size > 1000:
            chunk_size = 1000
        
        all_results = []
        
        for i in range(0, len(texts), chunk_size):
            chunk = texts[i:i + chunk_size]
            logger.info(f"Processing chunk {i//chunk_size + 1}")
            
            result = self.predict_batch(chunk)
            
            if "results" in result:
                all_results.extend(result["results"])
            else:
                logger.error(f"Error in batch {i//chunk_size + 1}")
        
        return all_results
    
    def filter_by_class(
        self,
        texts: List[str],
        target_class: str
    ) -> List[str]:
        """
        Filter texts that belong to a specific class
        
        Args:
            texts: Texts to filter
            target_class: Target class name
        
        Returns:
            List of texts classified as target_class
        """
        results = self.bulk_classify(texts)
        
        return [
            r["text"]
            for r in results
            if r["prediction"] == target_class
        ]
    
    def get_class_distribution(
        self,
        texts: List[str]
    ) -> Dict[str, int]:
        """
        Get count of texts per class
        
        Args:
            texts: Texts to classify
        
        Returns:
            Dictionary with class distribution
        """
        results = self.bulk_classify(texts)
        distribution = {}
        
        for result in results:
            class_name = result["prediction"]
            distribution[class_name] = distribution.get(class_name, 0) + 1
        
        return distribution


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_single_prediction():
    """Example: Single text classification"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Single Text Prediction")
    print("="*70)
    
    client = TextClassificationClient()
    
    text = "Apple announces new iPhone and iPad models"
    result = client.predict(text)
    
    if "error" not in result:
        print(f"Text: {result['text']}")
        print(f"Class: {result['prediction']['class_name']}")
        print(f"Confidence: {result['prediction']['confidence']:.2%}")
        print(f"Probabilities: {result['probabilities']}")
    else:
        print(f"Error: {result['error']}")


def example_batch_prediction():
    """Example: Batch text classification"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Batch Text Prediction")
    print("="*70)
    
    client = TextClassificationClient()
    
    texts = [
        "Stock market reaches record high",
        "Liverpool wins championship",
        "Scientists discover new particle"
    ]
    
    results = client.predict_batch(texts)
    
    print(f"Processed {results['total']} texts:")
    for r in results.get('results', []):
        print(f"  • {r['text'][:50]:<50} → {r['prediction']}")


def example_top_predictions():
    """Example: Get top predictions"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Top Predictions")
    print("="*70)
    
    client = TextClassificationClient()
    
    text = "Tech company announces breakthrough"
    top_3 = client.get_top_predictions(text, top_k=3)
    
    print(f"Text: {text}\n")
    print("Top predictions:")
    for i, (class_name, confidence) in enumerate(top_3, 1):
        print(f"  {i}. {class_name}: {confidence:.2%}")


def example_filter_by_class():
    """Example: Filter texts by class"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Filter by Class")
    print("="*70)
    
    client = TextClassificationClient()
    
    texts = [
        "Apple announces new iPhone",
        "Manchester United wins match",
        "New cancer treatment discovered",
        "Microsoft stock rises",
        "Olympic Games results"
    ]
    
    business_texts = client.filter_by_class(texts, "Business")
    
    print(f"Texts classified as 'Business':")
    for text in business_texts:
        print(f"  • {text}")


def example_class_distribution():
    """Example: Get class distribution"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Class Distribution")
    print("="*70)
    
    client = TextClassificationClient()
    
    texts = [
        "Apple announces new iPhone",
        "Manchester United wins match",
        "New cancer treatment discovered",
        "Microsoft stock rises",
        "Olympic Games results",
        "Google releases new AI model"
    ]
    
    distribution = client.get_class_distribution(texts)
    
    print(f"Class distribution for {len(texts)} texts:")
    for class_name, count in distribution.items():
        percentage = (count / len(texts)) * 100
        print(f"  {class_name}: {count} ({percentage:.1f}%)")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║   Text Classification API - Python Client Examples           ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    # Run examples
    try:
        example_single_prediction()
        example_batch_prediction()
        example_top_predictions()
        example_filter_by_class()
        example_class_distribution()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the Flask API is running:")
        print("  python flask_app.py")
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70 + "\n")
