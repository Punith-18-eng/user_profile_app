# Using Real Kaggle Datasets - Guide

## Overview
This guide explains how to download and use real datasets from Kaggle for the Text Classification project.

## Recommended Datasets from Kaggle

### 1. AG News Classification Dataset
- **URL**: https://www.kaggle.com/datasets/amananandrai/ag-news-classification-dataset
- **Size**: 120,000 training samples
- **Classes**: 4 (World, Sports, Business, Science/Technology)
- **Description**: News articles with category labels

### 2. BBC News Classification
- **URL**: https://www.kaggle.com/datasets/hamishdickson/bbc-news-classification
- **Size**: 2,225 articles
- **Classes**: 5 (tech, business, sport, entertainment, politics)
- **Description**: BBC news articles with categories

### 3. Amazon Reviews for Sentiment Analysis
- **URL**: https://www.kaggle.com/datasets/bittlingmayer/amazonreviews
- **Size**: 3.6M reviews
- **Classes**: 2 (positive, negative)
- **Description**: Product reviews with sentiment labels

### 4. Consumer Finance Complaints
- **URL**: https://www.kaggle.com/datasets/jboysen/sf-crime
- **Size**: 100,000+ complaints
- **Classes**: Multiple complaint categories
- **Description**: Financial complaint texts with categories

## Installation - Kaggle API

### Step 1: Install Kaggle API
```bash
pip install kaggle
```

### Step 2: Get Your API Token
1. Go to https://www.kaggle.com/settings/account
2. Click "Create New Token"
3. This will download `kaggle.json`

### Step 3: Setup Kaggle Configuration
```bash
# Windows
mkdir %USERPROFILE%\.kaggle
move kaggle.json %USERPROFILE%\.kaggle\

# Linux/Mac
mkdir ~/.kaggle
mv kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

## Downloading Datasets

### Option 1: Using Kaggle API (Recommended)
```bash
# Download AG News
kaggle datasets download -d amananandrai/ag-news-classification-dataset

# Download BBC News
kaggle datasets download -d hamishdickson/bbc-news-classification

# Unzip the downloaded file
unzip ag-news-classification-dataset.zip
```

### Option 2: Manual Download
1. Visit the Kaggle dataset page
2. Click "Download" button
3. Unzip the file in your project directory

## Loading Kaggle Datasets in Python

### Loading AG News Dataset
```python
import pandas as pd

# Load the CSV file
df = pd.read_csv('train.csv', header=None, names=['label', 'title', 'description'])

# Combine title and description for full text
df['text'] = df['title'] + ' ' + df['description']

print(df.shape)
print(df.head())
```

### Loading BBC News Dataset
```python
import pandas as pd

# Load the CSV file
df = pd.read_csv('BBC News Train.csv')

# The dataset should have 'Text' and 'Category' columns
print(df.head())
print(df['Category'].value_counts())
```

### Loading Amazon Reviews
```python
import pandas as pd

# Load training data
df_train = pd.read_csv('train.ft.txt.bz2', compression='bz2', header=None, names=['label', 'text'])

# Convert labels (1,2 to 0,1 for binary classification)
df_train['label'] = df_train['label'].apply(lambda x: 0 if x == 1 else 1)

print(df_train.shape)
```

## Integrating with Text Classification Script

### Modify the `clean_text` section:
```python
# Load your Kaggle dataset
df = pd.read_csv('your_dataset.csv')

# Ensure you have 'text' and 'label' columns
# If column names are different, rename them:
df = df.rename(columns={'your_text_column': 'text', 'your_label_column': 'label'})

# Convert labels to numeric if they're strings
label_mapping = {label: idx for idx, label in enumerate(df['label'].unique())}
df['label'] = df['label'].map(label_mapping)

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print(f"Labels: {df['label'].unique()}")
print(df.head())

# Continue with the rest of the pipeline...
```

## Dataset Statistics

### AG News
- Training samples: 120,000
- Test samples: 7,600
- Classes: 4
- Average text length: ~50 words

### BBC News
- Total samples: 2,225
- Classes: 5
- Average text length: ~400 words
- No predefined train/test split (you need to create it)

### Amazon Reviews
- Training samples: 3,600,000
- Test samples: 400,000
- Classes: 2 (binary classification)
- Average text length: ~100 words

## Tips for Using Kaggle Data

### 1. Data Exploration
```python
# Check dataset info
print(df.info())
print(df.describe())

# Check class distribution
print(df['label'].value_counts())

# Check for missing values
print(df.isnull().sum())

# Sample texts
for i, row in df.head(10).iterrows():
    print(f"Label: {row['label']}, Text: {row['text'][:100]}...")
```

### 2. Handle Imbalanced Data
```python
from sklearn.utils import class_weight

class_weights = class_weight.compute_class_weight(
    'balanced',
    classes=np.unique(y),
    y=y
)

model.fit(X_train, y_train_cat, class_weight=dict(enumerate(class_weights)))
```

### 3. Data Augmentation
```python
# Use libraries for augmentation
from nlpaug.augmenter.word import SynonymAug
from nlpaug.augmenter.sentence import ContextualWordEmbsAug

aug = SynonymAug(aug_src='wordnet')

# Augment text
augmented_texts = [aug.augment(text) for text in df['text']]
```

### 4. Handling Large Datasets
```python
# Use chunking to read large files
chunk_size = 10000
for chunk in pd.read_csv('large_dataset.csv', chunksize=chunk_size):
    # Process each chunk
    process(chunk)
```

## Kaggle Competition Datasets

Some datasets are from Kaggle competitions:

### AG News Competition
- **URL**: https://www.kaggle.com/competitions/nips-2018-papers
- **Download**: `kaggle competitions download -c nips-2018-papers`

### Toxic Comment Classification
- **URL**: https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge
- **Classes**: Multi-label text classification

## Troubleshooting

### Issue: Kaggle API Not Found
```bash
# Reinstall kaggle
pip uninstall kaggle -y
pip install kaggle
```

### Issue: Permission Denied
```bash
# Fix file permissions (Linux/Mac)
chmod 600 ~/.kaggle/kaggle.json
chmod 700 ~/.kaggle
```

### Issue: Dataset Download Fails
```bash
# Check internet connection
# Try again after some time
# Or manually download from Kaggle website
```

### Issue: CSV File Has Wrong Encoding
```python
# Specify encoding when reading
df = pd.read_csv('file.csv', encoding='utf-8')
# or
df = pd.read_csv('file.csv', encoding='latin1')
```

## Next Steps

1. **Download a Kaggle dataset** using the Kaggle API
2. **Explore the data** to understand its structure
3. **Modify the notebook** to load your specific dataset
4. **Run the complete pipeline** with real data
5. **Evaluate results** and tune hyperparameters
6. **Deploy the model** for production use

## References
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Kaggle API Documentation](https://github.com/Kaggle/kaggle-api)
- [Natural Language Processing with Deep Learning](https://www.coursera.org/)

---
**Note**: Always respect the dataset licenses and terms of use when downloading from Kaggle.
