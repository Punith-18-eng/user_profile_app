"""
Text Classification with TensorFlow
Complete implementation of text classification using Bidirectional LSTM

This script demonstrates:
- Data loading and preprocessing
- Text cleaning and tokenization
- Building and training a neural network
- Model evaluation and predictions
- Visualization of results
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import warnings

warnings.filterwarnings('ignore')

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("=" * 80)
print("TEXT CLASSIFICATION WITH TENSORFLOW - COMPLETE PIPELINE")
print("=" * 80)

# ============================================================================
# SECTION 1: LOAD AND EXPLORE DATASET
# ============================================================================
print("\n[1] Loading Dataset...")

# Create sample dataset
sample_texts = [
    "The stock market rose today with technology stocks leading the gains",
    "Manchester United defeated Liverpool 2-1 in an exciting match",
    "Scientists discover new species of deep sea fish",
    "Bitcoin price surges past $50,000 mark",
    "World leaders meet to discuss climate change",
    "New vaccine shows promising results in trials",
    "Apple announces new iPhone 15 with advanced features",
    "Artificial intelligence transforms healthcare industry",
    "Soccer World Cup finals draw record viewership",
    "Economic growth accelerates in developing nations"
]

sample_labels = [0, 1, 2, 0, 2, 2, 0, 2, 1, 0]  # 0=Business, 1=Sports, 2=Science/Tech

# Duplicate to create larger dataset
texts = sample_texts * 100
labels = sample_labels * 100

df = pd.DataFrame({'text': texts, 'label': labels})

print(f"Dataset Shape: {df.shape}")
print(f"\nFirst 5 records:")
print(df.head())

label_names = {0: 'Business', 1: 'Sports', 2: 'Science/Technology'}
df['category'] = df['label'].map(label_names)

print(f"\nClass Distribution:")
print(df['category'].value_counts())

# ============================================================================
# SECTION 2: DATA PREPROCESSING AND CLEANING
# ============================================================================
print("\n[2] Preprocessing and Cleaning Text Data...")

def clean_text(text):
    """Clean text data by removing special characters, stopwords, etc."""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
    
    return ' '.join(tokens)

# Remove missing values
df = df.dropna(subset=['text'])

# Apply cleaning
df['cleaned_text'] = df['text'].apply(clean_text)
df = df[df['cleaned_text'].str.len() > 0]

print(f"Dataset shape after cleaning: {df.shape}")
print(f"Sample cleaned texts:")
for i in range(2):
    print(f"  Original: {df['text'].iloc[i][:70]}...")
    print(f"  Cleaned:  {df['cleaned_text'].iloc[i][:70]}...")

# ============================================================================
# SECTION 3: TOKENIZATION AND VECTORIZATION
# ============================================================================
print("\n[3] Tokenizing and Vectorizing Text...")

MAX_FEATURES = 5000
MAX_LENGTH = 100

# Create tokenizer
tokenizer = Tokenizer(num_words=MAX_FEATURES, oov_token='<OOV>')
tokenizer.fit_on_texts(df['cleaned_text'])

# Convert texts to sequences
X = tokenizer.texts_to_sequences(df['cleaned_text'])

# Pad sequences
X = pad_sequences(X, maxlen=MAX_LENGTH, padding='post')

# Prepare labels
y = df['label'].values

print(f"Tokenizer vocabulary size: {len(tokenizer.word_index)}")
print(f"Shape of X after padding: {X.shape}")
print(f"Shape of y: {y.shape}")

# Split the data
print("\n[3a] Splitting Data into Train/Validation/Test...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

# Convert labels to categorical
num_classes = len(np.unique(y))
y_train_cat = keras.utils.to_categorical(y_train, num_classes)
y_val_cat = keras.utils.to_categorical(y_val, num_classes)
y_test_cat = keras.utils.to_categorical(y_test, num_classes)

print(f"Training set shape: X_train={X_train.shape}, y_train={y_train.shape}")
print(f"Validation set shape: X_val={X_val.shape}, y_val={y_val.shape}")
print(f"Test set shape: X_test={X_test.shape}, y_test={y_test.shape}")
print(f"Number of classes: {num_classes}")

# ============================================================================
# SECTION 4: BUILD NEURAL NETWORK MODEL
# ============================================================================
print("\n[4] Building Neural Network Model...")

EMBEDDING_DIM = 128

model = models.Sequential([
    layers.Embedding(MAX_FEATURES, EMBEDDING_DIM, input_length=MAX_LENGTH),
    layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.2)),
    layers.GlobalAveragePooling1D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(
    loss='categorical_crossentropy',
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)

print("\nModel Architecture:")
model.summary()

# ============================================================================
# SECTION 5: TRAIN THE MODEL
# ============================================================================
print("\n[5] Training the Model...")

early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    X_train, y_train_cat,
    epochs=15,
    batch_size=32,
    validation_data=(X_val, y_val_cat),
    callbacks=[early_stopping],
    verbose=1
)

print("\nModel training completed!")

# ============================================================================
# SECTION 6: EVALUATE MODEL PERFORMANCE
# ============================================================================
print("\n[6] Evaluating Model Performance...")

y_pred_probs = model.predict(X_test, verbose=0)
y_pred = np.argmax(y_pred_probs, axis=1)

test_loss, test_accuracy = model.evaluate(X_test, y_test_cat, verbose=0)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"\nTest Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Precision (weighted): {precision:.4f}")
print(f"Recall (weighted): {recall:.4f}")
print(f"F1-Score (weighted): {f1:.4f}")

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=label_names.values()))

# Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_names.values(),
            yticklabels=label_names.values())
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.show()

# ============================================================================
# SECTION 7: MAKE PREDICTIONS ON NEW TEXT
# ============================================================================
print("\n[7] Making Predictions on New Text...")

def predict_text(text):
    """Predict the class of new text"""
    cleaned = clean_text(text)
    sequence = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
    prediction = model.predict(padded, verbose=0)
    pred_class = np.argmax(prediction[0])
    confidence = np.max(prediction[0])
    return pred_class, confidence

test_samples = [
    "Apple Stock Price Reaches New All-Time High",
    "Argentina Wins Soccer Championship Match",
    "Breakthrough in Quantum Computing Technology",
    "Tech Giant Announces New Product Launch",
    "Football Team Advances to Finals"
]

print("\nPredictions on New Text Samples:")
for sample in test_samples:
    pred_class, confidence = predict_text(sample)
    pred_category = label_names.get(pred_class, 'Unknown')
    print(f"Text: {sample}")
    print(f"Category: {pred_category} | Confidence: {confidence:.4f}\n")

# ============================================================================
# SECTION 8: VISUALIZE TRAINING HISTORY
# ============================================================================
print("[8] Visualizing Training History...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(history.history['accuracy'], label='Training Accuracy')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
axes[0].set_title('Model Accuracy Over Epochs')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history.history['loss'], label='Training Loss')
axes[1].plot(history.history['val_loss'], label='Validation Loss')
axes[1].set_title('Model Loss Over Epochs')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("PROJECT SUMMARY")
print("=" * 80)
print(f"""
✓ Dataset loaded and explored
✓ Text preprocessing and cleaning completed
✓ Tokenization and vectorization performed
✓ Neural network model built and trained
✓ Model evaluated on test set
✓ Predictions made on new samples
✓ Training history visualized

Model Performance:
- Test Accuracy: {test_accuracy:.4f}
- Precision: {precision:.4f}
- Recall: {recall:.4f}
- F1-Score: {f1:.4f}

The model is ready for deployment or further optimization!
""")
print("=" * 80)
