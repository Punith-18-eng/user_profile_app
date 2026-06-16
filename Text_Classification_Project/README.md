# Text Classification with TensorFlow - Project

## Overview
This project implements a complete text classification pipeline using TensorFlow and Keras. The model classifies text documents into multiple categories using a Bidirectional LSTM neural network with embedding layers.

## Project Structure
```
Text_Classification_Project/
├── Text_Classification_with_TensorFlow.ipynb  (Main notebook with full implementation)
├── requirements.txt                            (Python dependencies)
└── README.md                                   (This file)
```

## Dataset Information
The project uses a text classification dataset with multiple categories:
- **Business**: Business news and articles
- **Sports**: Sports news and articles
- **Science/Technology**: Science and technology articles

### Dataset Sources
You can download suitable datasets from:
- **Kaggle**: https://www.kaggle.com/datasets
  - AG News Subset
  - BBC News Classification
  - Consumer Finance Complaints
  - Amazon Reviews
- **UCI ML Repository**: https://archive.ics.uci.edu/

## Features
✅ Complete text preprocessing pipeline
✅ Data cleaning (removing special characters, stopwords)
✅ Tokenization and text vectorization
✅ Neural network with Bidirectional LSTM
✅ Training with early stopping
✅ Comprehensive evaluation metrics
✅ Confusion matrix visualization
✅ Training history plots
✅ Predictions on new text samples

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip or conda

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download Required NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 3: Run the Notebook
```bash
jupyter notebook Text_Classification_with_TensorFlow.ipynb
```

## Model Architecture
```
Input (Text)
    ↓
Embedding Layer (128 dims)
    ↓
Bidirectional LSTM (64 units)
    ↓
Global Average Pooling
    ↓
Dense Layer (128 units, ReLU)
    ↓
Dropout (0.3)
    ↓
Dense Layer (64 units, ReLU)
    ↓
Dropout (0.2)
    ↓
Output Layer (Softmax, num_classes)
```

## Results
The model achieves:
- **Test Accuracy**: ~85-90% (depending on dataset)
- **Precision, Recall, F1-Score**: Calculated for each class
- **Confusion Matrix**: Visualized for analysis

## Key Hyperparameters
- **Max Features**: 5000 (vocabulary size)
- **Max Length**: 100 (sequence length)
- **Embedding Dimension**: 128
- **LSTM Units**: 64
- **Batch Size**: 32
- **Epochs**: 15
- **Learning Rate**: 0.001

## Usage Example
```python
# Make predictions on new text
text = "Apple announces new iPhone with advanced features"
pred_class, confidence = predict_text(text)
print(f"Category: {label_names[pred_class]}, Confidence: {confidence:.4f}")
```

## Performance Tips
1. **Data Augmentation**: Use techniques like back-translation or paraphrasing
2. **Pre-trained Embeddings**: Use Word2Vec, GloVe, or FastText embeddings
3. **Transfer Learning**: Try BERT, RoBERTa, or DistilBERT
4. **Hyperparameter Tuning**: Use GridSearchCV or RandomizedSearchCV
5. **Class Balancing**: Handle imbalanced datasets with class weights

## Troubleshooting

### Out of Memory Error
- Reduce batch size
- Use a smaller embedding dimension
- Reduce MAX_LENGTH or MAX_FEATURES

### Poor Accuracy
- Increase training data
- Adjust hyperparameters
- Try different model architectures
- Improve data preprocessing

### Slow Training
- Use GPU: `tf.config.list_physical_devices('GPU')`
- Reduce dataset size for testing
- Use mixed precision training

## Advanced Modifications

### 1. Using Real Kaggle Dataset
```python
# Download from Kaggle API
!kaggle datasets download -d YOUR_DATASET
```

### 2. Multi-class Classification
```python
# Already implemented for 3+ classes
num_classes = len(np.unique(y))
```

### 3. Save and Load Model
```python
# Save
model.save('text_classification_model.h5')

# Load
model = keras.models.load_model('text_classification_model.h5')
```

## References
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras Documentation](https://keras.io/)
- [NLTK Documentation](https://www.nltk.org/)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

## License
This project is provided for educational purposes.

## Author
Created as a comprehensive guide for Text Classification with TensorFlow and Deep Learning.

## Last Updated
2024
