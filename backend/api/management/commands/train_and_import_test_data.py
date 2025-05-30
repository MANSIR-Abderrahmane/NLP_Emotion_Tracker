# backend/api/management/commands/train_and_import_test_data.py

import os
import joblib
import pandas as pd
from datetime import datetime
import re # For content cleaning
import numpy as np # Ensure this is imported for np usage

# Import NLTK for tokenization if not already imported
from nltk.tokenize import word_tokenize
import nltk

# Import scikit-learn components for model evaluation
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# Import Django specific components
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models import Post # Your Post model
# Make sure analyzer is imported from the correct path after the fix
from emotion_analyzer.analyzer import analyze_emotion, load_hybrid_models # Import load_hybrid_models too

# Import TensorFlow/Keras specific components
import tf_keras as keras # Use tf_keras if you installed it as such, otherwise import tensorflow.keras
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Dropout
from tf_keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from sentence_transformers import SentenceTransformer


# Ensure NLTK punkt data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

# Define the path where your trained model and vectorizer will be saved
MODEL_SAVE_DIR = os.path.join(settings.BASE_DIR, 'emotion_analyzer', 'models')
KERAS_MODEL_PATH = os.path.join(MODEL_SAVE_DIR, 'tensorflow_emotion_classifier.h5')
LABEL_ENCODER_PATH = os.path.join(MODEL_SAVE_DIR, 'label_encoder.joblib')
SENTENCE_TRANSFORMER_NAME_PATH = os.path.join(MODEL_SAVE_DIR, 'sentence_transformer_name.txt') # New path for SBERT model name

class Command(BaseCommand):
    help = 'Trains the Hybrid NLP Emotion Classifier and imports a test set into the database.'

    def _clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower() # Convert to lowercase
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # Remove URLs
        text = re.sub(r'@\w+|#\w+', '', text) # Remove mentions and hashtags
        text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
        text = text.strip() # Remove leading/trailing whitespace
        return text

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Hybrid NLP Model Training and Test Data Import..."))

        # Ensure the model save directory exists
        os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

        # --- NEW ADDITION: Remove existing model files to force pseudo-labeling with HF model ---
        self.stdout.write(self.style.WARNING("Clearing old emotion classifier models to ensure fresh pseudo-labeling..."))
        for model_file in [KERAS_MODEL_PATH, LABEL_ENCODER_PATH, SENTENCE_TRANSFORMER_NAME_PATH]:
            if os.path.exists(model_file):
                try:
                    os.remove(model_file)
                    self.stdout.write(self.style.WARNING(f"  Removed: {os.path.basename(model_file)}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Failed to remove {os.path.basename(model_file)}: {e}"))
        # --- END NEW ADDITION ---

        # 1. Load data from the database
        self.stdout.write("Loading data from the database...")
        all_posts = Post.objects.all()

        # Filter out posts with empty content
        valid_posts = [p for p in all_posts if p.content and self._clean_text(p.content)]

        if not valid_posts:
            raise CommandError("No valid posts found in the database to train or import.")

        texts = []
        true_labels = [] # This will store labels from the DB (either true or pseudo-generated)

        # Ensure analyzer models are loaded before starting pseudo-labeling loop
        # With the above file removal, this should now load the HF model as fallback if no custom model exists.
        load_hybrid_models()

        self.stdout.write("Processing posts and generating pseudo-labels for unlabeled data...")
        for post in valid_posts:
            cleaned_content = self._clean_text(post.content)

            # Check if the post is already labeled (either via emotion_primary or true_emotion_label)
            # Prioritize true_emotion_label if available, otherwise use emotion_primary
            label_from_db = post.true_emotion_label if post.true_emotion_label else post.emotion_primary

            if not label_from_db or label_from_db.strip() == "" or label_from_db.lower() == "error":
                # If unlabelled, pseudo-label using the analyzer
                self.stdout.write(self.style.WARNING(f"Post '{cleaned_content[:50]}...' is unlabelled or has 'Error'. Pseudo-labeling..."))
                analyzed_result = analyze_emotion(cleaned_content)
                pseudo_label = analyzed_result.get("emotion_primary", "Neutral") # Default to Neutral if analysis fails
                if pseudo_label == "Error": # If analyzer itself returned Error, it couldn't analyze
                    self.stdout.write(self.style.ERROR(f"Analyzer returned 'Error' for pseudo-labeling post '{cleaned_content[:50]}...'. Skipping for training."))
                    continue # Skip this post if pseudo-labeling failed
                true_labels.append(pseudo_label)
                self.stdout.write(self.style.SUCCESS(f"  -> Pseudo-labeled as: {pseudo_label}"))
            else:
                # Use the existing label
                true_labels.append(label_from_db)
                self.stdout.write(f"Post '{cleaned_content[:50]}...' has existing label: {label_from_db}")

            texts.append(cleaned_content)

        if not texts or not true_labels or len(texts) != len(true_labels):
            raise CommandError("No valid text-label pairs found after processing database posts. Ensure posts have content and can be labeled.")

        df = pd.DataFrame({'text': texts, 'label': true_labels})

        # Ensure all labels are strings
        df['label'] = df['label'].astype(str)

        # Check unique labels. If only one, warn the user.
        unique_labels = df['label'].unique()
        self.stdout.write(f"Emotion labels encoded: {unique_labels.tolist()}")
        if len(unique_labels) <= 1:
            self.stdout.write(self.style.WARNING(
                "WARNING: Only one or zero unique emotion labels found in the training data "
                f"('{unique_labels.tolist()}'). "
                "The model will not be able to classify different emotions effectively. "
                "Please ensure your database contains posts with diverse emotion labels, "
                "or re-run the pseudo-labeling process (e.g., via Colab notebook) to generate them."
            ))
            if len(unique_labels) == 0:
                 raise CommandError("No emotion labels found for training data.")


        # Split data into training and test sets (stratified if possible)
        # Using a small test size from the database for model evaluation.
        train_texts, test_texts, train_labels, test_labels = train_test_split(
            df['text'], df['label'], test_size=0.1, random_state=42,
            stratify=df['label'] if len(unique_labels) > 1 else None # Stratify only if multiple classes
        )

        self.stdout.write(f"Dataset split: {len(train_texts)} training samples, {len(test_texts)} test samples.")

        # 2. Generate embeddings for training and test data using SentenceTransformer
        self.stdout.write("Loading SentenceTransformer 'all-MiniLM-L6-v2'...")
        sbert_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        sentence_model = SentenceTransformer(sbert_model_name)
        # Save the model name for the analyzer to load
        with open(SENTENCE_TRANSFORMER_NAME_PATH, 'w') as f:
            f.write(sbert_model_name)
        self.stdout.write(f"SentenceTransformer '{sbert_model_name}' loaded successfully.")

        self.stdout.write("Preprocessing text and generating embeddings...")
        train_embeddings = sentence_model.encode(train_texts.tolist(), show_progress_bar=True)
        test_embeddings = sentence_model.encode(test_texts.tolist(), show_progress_bar=True)
        self.stdout.write("Text embeddings generated.")

        # 3. Encode labels
        label_encoder = LabelEncoder()
        train_labels_encoded = label_encoder.fit_transform(train_labels)
        test_labels_encoded = label_encoder.transform(test_labels)

        # 4. Build and train TensorFlow Keras classifier model
        self.stdout.write("Building TensorFlow Keras classifier model...")
        model = Sequential([
            Dense(256, activation='relu', input_shape=(train_embeddings.shape[1],)),
            Dropout(0.3),
            Dense(128, activation='relu'),
            Dropout(0.3),
            # Output layer: number of neurons = number of unique emotion labels
            # Use 'softmax' for multi-class classification, 'sigmoid' for binary.
            Dense(len(label_encoder.classes_), activation='softmax' if len(label_encoder.classes_) > 1 else 'sigmoid')
        ])

        # Compile the model
        # Use 'sparse_categorical_crossentropy' for integer labels when output is softmax.
        # Use 'binary_crossentropy' for sigmoid output (binary classification).
        if len(label_encoder.classes_) > 1:
            loss_function = 'sparse_categorical_crossentropy'
        else: # Single class will be mapped to 0 by LabelEncoder, use sparse_categorical_crossentropy
            loss_function = 'sparse_categorical_crossentropy'


        model.compile(optimizer=Adam(learning_rate=0.001),
                      loss=loss_function,
                      metrics=['accuracy'])

        self.stdout.write("TensorFlow Keras model built.")
        model.summary()

        # 5. Train the model
        self.stdout.write("Training TensorFlow Keras classifier...")
        epochs = 50
        model.fit(train_embeddings, train_labels_encoded,
                  epochs=epochs,
                  batch_size=32,
                  validation_split=0.1, # Use a validation split from the training data itself
                  verbose=1)
        self.stdout.write("TensorFlow Keras classifier trained.")

        # 6. Evaluate the model on the test set
        self.stdout.write("\n--- Model Evaluation Results (on 10% Test Set from DB) ---")
        loss, accuracy = model.evaluate(test_embeddings, test_labels_encoded, verbose=0)
        self.stdout.write(f"Test Loss: {loss:.4f}")
        self.stdout.write(f"Test Accuracy: {accuracy:.4f}")

        # Generate predictions for classification report
        y_pred_probs = model.predict(test_embeddings, verbose=0)
        if len(label_encoder.classes_) > 1:
            y_pred_encoded = np.argmax(y_pred_probs, axis=1)
        else: # Single output neuron
            # If len(label_encoder.classes_) is 1, then the target is always 0. The model will just predict 0.
            y_pred_encoded = np.array([0] * len(test_labels_encoded)) # Predict the only class that exists