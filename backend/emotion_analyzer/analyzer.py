# backend/api/analyzer.py

import os
import joblib
import numpy as np
from django.conf import settings
from collections import OrderedDict
import tensorflow as tf # Keep this line if you installed 'tensorflow'. If you only installed 'torch', you might remove this.
import spacy
from sentence_transformers import SentenceTransformer

# NEW IMPORTS FOR HUGGING FACE
from transformers import pipeline
import torch # Keep this line if you installed 'torch'. If you only installed 'tensorflow', you might remove this.
# import accelerate # Uncomment this line if you installed 'accelerate'

# Define paths to your model and vectorizer
MODEL_DIR = os.path.join(settings.BASE_DIR, 'emotion_analyzer', 'models')
TF_MODEL_PATH = os.path.join(MODEL_DIR, 'tensorflow_emotion_classifier.h5')
SENTENCE_TRANSFORMER_NAME_PATH = os.path.join(MODEL_DIR, 'sentence_transformer_name.txt')
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.joblib')

# Global variables for loaded models and components
tf_classifier = None
sentence_model = None
label_encoder = None
nlp = None
EMOTION_LABELS = []

# NEW GLOBAL VARIABLE FOR HUGGING FACE PIPELINE
hf_emotion_pipeline = None

# Load models and components only once when the module is loaded
def load_hybrid_models():
    global tf_classifier, sentence_model, label_encoder, nlp, EMOTION_LABELS, hf_emotion_pipeline
    print("Analyzer: Attempting to load models...") # Added for debugging
    try: # Broad try-except to catch any unexpected error during the entire model loading process
        # Load SpaCy model (less critical, can be skipped if not found)
        try:
            nlp = spacy.load("en_core_web_sm")
            print("Analyzer: SpaCy 'en_core_web_sm' model loaded successfully.")
        except OSError as e:
            print(f"Analyzer: WARNING: SpaCy 'en_core_web_sm' model not found or failed to load: {e}. Emotion analysis will proceed without SpaCy.")
            # If spacy model is not found, the nlp object will be None.

        # Attempt to load your custom TF classifier (trained by train_and_import_test_data.py)
        if os.path.exists(TF_MODEL_PATH) and os.path.exists(LABEL_ENCODER_PATH) and os.path.exists(SENTENCE_TRANSFORMER_NAME_PATH):
            print("Analyzer: Found custom TensorFlow model components. Attempting to load...")
            try:
                label_encoder = joblib.load(LABEL_ENCODER_PATH)
                EMOTION_LABELS = label_encoder.classes_.tolist()
                # Ensure you're calling load_model from tf.keras if you're using tensorflow
                tf_classifier = tf.keras.models.load_model(TF_MODEL_PATH)
                with open(SENTENCE_TRANSFORMER_NAME_PATH, 'r') as f:
                    sbert_model_name = f.read().strip()
                sentence_model = SentenceTransformer(sbert_model_name)
                print("Analyzer: Custom TensorFlow Emotion Classifier and SentenceTransformer loaded successfully.")
            except Exception as e:
                print(f"Analyzer: ERROR: Failed to load custom TensorFlow model/components: {e}. This model path might be incorrect or files corrupted. Falling back to Hugging Face for emotion analysis.")
                tf_classifier = None # Ensure it's None if loading fails
        else:
            print("Analyzer: Custom TensorFlow model or its components not found. Will attempt to use Hugging Face for emotion analysis.")

        # Load Hugging Face emotion classification pipeline as a fallback or primary pseudo-labeler
        # Only attempt to load if the custom TF classifier is NOT loaded or if you always want HF
        if tf_classifier is None and hf_emotion_pipeline is None:
            print("Analyzer: Attempting to load Hugging Face emotion classification pipeline...")
            try:
                # 'bhadresh-savani/bert-base-uncased-emotion' is a good starting point.
                # Ensure internet connection is available for initial download.
                # Specify the device if you have a GPU: device=0 for GPU, device=-1 for CPU
                hf_emotion_pipeline = pipeline("sentiment-analysis", model="bhadresh-savani/bert-base-uncased-emotion",
                                              # device=0 if torch.cuda.is_available() else -1 # Uncomment for GPU usage
                                              )
                print("Analyzer: Hugging Face emotion classification pipeline loaded successfully.")
            except Exception as e:
                print(f"Analyzer: ERROR: Failed to load Hugging Face emotion pipeline: {e}. Please ensure you have internet access and have installed 'transformers', 'torch' (or 'tensorflow'), and potentially 'accelerate'. Emotion analysis might be limited.")
                hf_emotion_pipeline = None

    except Exception as e: # Catch any other unexpected errors from the entire loading process
        print(f"Analyzer: CRITICAL ERROR during model loading in load_hybrid_models(): {e}")
        # This will catch errors that occur outside the specific try-except blocks above.

# Call load_hybrid_models once when this module is imported
load_hybrid_models()

def analyze_emotion(text_content):
    if not isinstance(text_content, str) or not text_content.strip():
        return {"emotion_primary": "Neutral", "emotion_score": 0.0, "secondary_emotions_json": {}}

    try:
        processed_text = text_content.lower() # Basic cleaning

        # Prioritize your custom TensorFlow model if it's loaded and ready
        if tf_classifier is not None and sentence_model is not None and EMOTION_LABELS:
            # Existing logic for your TF classifier
            text_embedding = sentence_model.encode([processed_text])[0]
            emotion_probabilities = tf_classifier.predict(np.expand_dims(text_embedding, axis=0))[0]
            emotion_scores = dict(zip(EMOTION_LABELS, emotion_probabilities))
            sorted_emotions = sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)

            primary_emotion = "neutral"
            primary_score = 0.0
            secondary_emotions_to_display = OrderedDict()

            if sorted_emotions:
                primary_emotion, primary_score = sorted_emotions[0]
                secondary_counter = 0
                for emotion, score in sorted_emotions:
                    if emotion != primary_emotion:
                        secondary_emotions_to_display[emotion] = round(float(score), 4)
                        secondary_counter += 1
                        if secondary_counter >= 2:
                            break

            return {
                "emotion_primary": primary_emotion,
                "emotion_score": round(float(primary_score), 4),
                "secondary_emotions_json": dict(secondary_emotions_to_display)
            }
        elif hf_emotion_pipeline is not None:
            # Fallback/Primary Pseudo-labeling with Hugging Face model
            print(f"Analyzer: Using Hugging Face for pseudo-labeling: '{processed_text[:50]}...'")
            hf_results = hf_emotion_pipeline(processed_text)

            if hf_results:
                primary_emotion = hf_results[0]['label'].lower()
                primary_score = float(hf_results[0]['score'])

                secondary_emotions_to_display = OrderedDict()
                if len(hf_results) > 1: # Some HF models return top-k, others just best
                    secondary_counter = 0
                    for i in range(1, len(hf_results)):
                        if hf_results[i]['label'].lower() != primary_emotion:
                            secondary_emotions_to_display[hf_results[i]['label'].lower()] = round(float(hf_results[i]['score']), 4)
                            secondary_counter += 1
                            if secondary_counter >= 2:
                                break

                return {
                    "emotion_primary": primary_emotion,
                    "emotion_score": round(primary_score, 4),
                    "secondary_emotions_json": dict(secondary_emotions_to_display)
                }
            else:
                print("Analyzer: Hugging Face pipeline returned no results.")
                return {"emotion_primary": "Neutral", "emotion_score": 0.0, "secondary_emotions_json": {}}
        else:
            print("Analyzer: No emotion analysis model (TensorFlow or Hugging Face) is loaded or available.")
            return {"emotion_primary": "Error", "emotion_score": 0.0, "secondary_emotions_json": {}}

    except Exception as e:
        print(f"Analyzer: ERROR during emotion analysis in analyze_emotion function: {e}")
        return {"emotion_primary": "Error", "emotion_score": 0.0, "secondary_emotions_json": {}}