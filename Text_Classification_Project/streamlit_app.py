"""
Streamlit Web Application for Text Classification
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

# Set page configuration
st.set_page_config(
    page_title="Text Classification with TensorFlow",
    page_icon="📝",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and configuration
@st.cache_resource
def load_model_and_config():
    """Load trained model, tokenizer, and configuration"""
    try:
        model = keras.models.load_model('saved_models/text_classification_model.h5')
        
        with open('saved_models/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        
        with open('saved_models/config.pickle', 'rb') as handle:
            config = pickle.load(handle)
        
        return model, tokenizer, config
    except FileNotFoundError:
        st.error("❌ Model files not found! Please train the model first by running the Jupyter notebook.")
        st.stop()

# Load model
model, tokenizer, config = load_model_and_config()

# Extract configuration
MAX_LENGTH = config['MAX_LENGTH']
label_names = config['label_names']
num_classes = config['num_classes']

# Title and description
st.title("📝 Text Classification with TensorFlow")
st.markdown("Classify text into categories using a trained Deep Learning model")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    **Text Classification Model**
    - Architecture: Bidirectional LSTM
    - Categories: Business, Sports, Science/Technology
    - Framework: TensorFlow & Keras
    """)
    
    st.divider()
    
    st.header("Settings")
    show_details = st.checkbox("Show detailed analysis", value=True)
    show_probabilities = st.checkbox("Show all class probabilities", value=True)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Predict", "Batch Predict", "Model Info", "Examples"])

# ============================================================================
# TAB 1: SINGLE PREDICTION
# ============================================================================
with tab1:
    st.header("🎯 Single Text Classification")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_text = st.text_area(
            "Enter text to classify:",
            placeholder="e.g., Apple announces new iPhone with advanced features",
            height=150
        )
    
    with col2:
        st.write("**Quick Examples:**")
        examples = [
            "Stock market rises today",
            "Football match results",
            "New vaccine discovered",
            "Tech company merger",
            "Baseball championship"
        ]
        for example in examples:
            if st.button(example, key=example):
                user_text = example

    if st.button("Classify Text", type="primary", use_container_width=True):
        if user_text.strip():
            # Preprocess text
            from nltk.corpus import stopwords
            from nltk.tokenize import word_tokenize
            import re
            
            # Clean text
            text = user_text.lower()
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
            
            # Tokenize and pad
            sequence = tokenizer.texts_to_sequences([cleaned_text])
            padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
            
            # Get predictions
            predictions = model.predict(padded, verbose=0)[0]
            pred_class = np.argmax(predictions)
            confidence = predictions[pred_class]
            
            # Display results
            st.success(f"✅ Classification Complete")
            
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.metric("Predicted Category", label_names[pred_class])
                st.metric("Confidence", f"{confidence:.2%}")
            
            with result_col2:
                st.metric("Text Length", len(user_text.split()))
                st.metric("Cleaned Text Length", len(cleaned_text.split()))
            
            if show_details:
                st.divider()
                st.subheader("📊 Detailed Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original Text:**")
                    st.info(user_text)
                
                with col2:
                    st.write("**Cleaned Text:**")
                    st.info(cleaned_text if cleaned_text else "(Empty after cleaning)")
            
            if show_probabilities:
                st.divider()
                st.subheader("📈 Confidence Scores")
                
                prob_data = {}
                for i, class_name in enumerate(label_names.values()):
                    prob_data[class_name] = float(predictions[i])
                
                # Create chart
                prob_df = pd.DataFrame(list(prob_data.items()), columns=['Category', 'Probability'])
                st.bar_chart(data=prob_df.set_index('Category'), use_container_width=True)
                
                # Create table
                st.dataframe(
                    prob_df.assign(**{'Probability': prob_df['Probability'].apply(lambda x: f"{x:.4f}")}),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.warning("Please enter some text to classify")

# ============================================================================
# TAB 2: BATCH PREDICTION
# ============================================================================
with tab2:
    st.header("📦 Batch Text Classification")
    
    st.write("Classify multiple texts at once")
    
    batch_text = st.text_area(
        "Enter texts (one per line):",
        placeholder="Line 1: Stock market rises\nLine 2: Football match today\nLine 3: New discovery in science",
        height=200
    )
    
    if st.button("Classify Batch", type="primary", use_container_width=True):
        if batch_text.strip():
            texts = [t.strip() for t in batch_text.split('\n') if t.strip()]
            
            import pandas as pd
            from nltk.corpus import stopwords
            from nltk.tokenize import word_tokenize
            import re
            
            results = []
            progress_bar = st.progress(0)
            
            for idx, text in enumerate(texts):
                # Clean text
                cleaned = text.lower()
                cleaned = re.sub(r'http\S+|www\S+|https\S+', '', cleaned, flags=re.MULTILINE)
                cleaned = re.sub(r'\S+@\S+', '', cleaned)
                cleaned = re.sub(r'[^a-zA-Z\s]', '', cleaned)
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                
                try:
                    tokens = word_tokenize(cleaned)
                    stop_words = set(stopwords.words('english'))
                    tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
                    cleaned = ' '.join(tokens)
                except:
                    pass
                
                # Predict
                sequence = tokenizer.texts_to_sequences([cleaned])
                padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
                predictions = model.predict(padded, verbose=0)[0]
                
                pred_class = np.argmax(predictions)
                confidence = predictions[pred_class]
                
                results.append({
                    'Text': text,
                    'Predicted Class': label_names[pred_class],
                    'Confidence': f"{confidence:.2%}"
                })
                
                progress_bar.progress((idx + 1) / len(texts))
            
            # Display results
            st.success(f"✅ Classified {len(results)} texts")
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True,
                hide_index=True
            )
            
            # Download results
            csv = pd.DataFrame(results).to_csv(index=False)
            st.download_button(
                label="Download Results (CSV)",
                data=csv,
                file_name="classification_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("Please enter at least one text")

# ============================================================================
# TAB 3: MODEL INFORMATION
# ============================================================================
with tab3:
    st.header("ℹ️ Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Architecture")
        st.info(f"""
        **Architecture Type:** Bidirectional LSTM
        
        **Layers:**
        - Embedding (5000 features × 128 dims)
        - Bidirectional LSTM (64 units)
        - Global Average Pooling
        - Dense (128 units, ReLU)
        - Dropout (0.3)
        - Dense (64 units, ReLU)
        - Dropout (0.2)
        - Output (3 classes, Softmax)
        
        **Total Parameters:** {model.count_params():,}
        """)
    
    with col2:
        st.subheader("Configuration")
        st.info(f"""
        **Vocabulary Size:** {config.get('MAX_FEATURES', 5000):,}
        **Max Sequence Length:** {MAX_LENGTH}
        **Embedding Dimension:** {config.get('EMBEDDING_DIM', 128)}
        **Number of Classes:** {num_classes}
        
        **Classes:**
        {chr(10).join([f"• {label_names[i]}" for i in range(num_classes)])}
        """)
    
    st.divider()
    
    st.subheader("Model Summary")
    model_summary = []
    for layer in model.layers:
        model_summary.append({
            'Layer': layer.__class__.__name__,
            'Output Shape': str(layer.output_shape),
            'Parameters': layer.count_params()
        })
    
    import pandas as pd
    st.dataframe(
        pd.DataFrame(model_summary),
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# TAB 4: EXAMPLES
# ============================================================================
with tab4:
    st.header("📚 Classification Examples")
    
    examples = {
        "Business": [
            "Apple stock reaches all-time high",
            "Federal Reserve raises interest rates",
            "Tesla announces quarterly earnings",
            "Amazon opens new distribution center",
            "Cryptocurrency market volatility continues"
        ],
        "Sports": [
            "Manchester United wins 3-0 victory",
            "Olympic games begin in Paris",
            "LeBron James scores 40 points",
            "Champions League final results",
            "Tennis tournament draws record crowds"
        ],
        "Science/Technology": [
            "Scientists discover new exoplanet",
            "Breakthrough in quantum computing",
            "AI model shows promising results",
            "Space agency launches new mission",
            "Medical researchers develop vaccine"
        ]
    }
    
    for category, texts in examples.items():
        with st.expander(f"📌 {category} Examples", expanded=False):
            for text in texts:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{text}**")
                with col2:
                    if st.button("Try", key=f"example_{text}"):
                        st.session_state.example_text = text
                        st.switch_page("pages/page_1.py") if "pages" in os.listdir() else None

# Footer
st.divider()
st.markdown("""
---
**Text Classification with TensorFlow** | Built with Streamlit
- Framework: TensorFlow & Keras
- Deployment: Streamlit Cloud
- Last Updated: 2026-06-16
""")
