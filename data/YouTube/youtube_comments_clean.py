import pandas as pd
import csv
import re
from io import StringIO
from html import unescape
import os

# Step 10.1: Define the file path (update this to the correct location)
INPUT_FILE = r"C:\Users\fujitus\Desktop\Me\NLP_Emotions_Tracker\data\youtube_comments.csv"  # Adjust this path
OUTPUT_FILE = r"C:\Users\fujitus\Desktop\Me\NLP_Emotions_Tracker\data\youtube_comments_fixed.csv"

# Verify file exists
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"Input file not found at: {INPUT_FILE}. Please check the path and ensure the file exists.")

# Step 10.2: Read the CSV with robust parsing
try:
    data = pd.read_csv(INPUT_FILE, quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8', on_bad_lines='warn')
except Exception as e:
    print(f"Error reading CSV: {e}")
    # Fallback: Manual parsing
    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        raw_data = file.read()
    csv_buffer = StringIO(raw_data)
    data = pd.read_csv(csv_buffer, quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8', on_bad_lines='warn')

# Step 10.3: Text Preprocessing for text column
def clean_text(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    # Decode HTML entities (e.g., ' to ', " to ")
    text = unescape(text)
    # Encode to handle emojis and non-ASCII characters
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    # Replace newlines and carriage returns with spaces
    text = re.sub(r'[\n\r]+', ' ', text)
    # Escape double quotes for CSV compatibility
    text = text.replace('"', '""')
    # Normalize multiple spaces and tabs
    text = re.sub(r'\s+', ' ', text)
    # Simplify URLs and user mentions
    text = re.sub(r'https?://\S+', '[URL]', text)
    text = re.sub(r'@\S+', '[USER]', text)
    # Trim leading/trailing spaces
    return text.strip()

# Apply cleaning to text column
data['text'] = data['text'].apply(clean_text)

# Step 10.4: Validate and clean other columns
# Convert published_at and updated_at to datetime
data['published_at'] = pd.to_datetime(data['published_at'], errors='coerce')
data['updated_at'] = pd.to_datetime(data['updated_at'], errors='coerce')

# Drop rows with missing author or published_at
data = data.dropna(subset=['author', 'published_at'])

# Check for duplicates (using author + published_at as a proxy for uniqueness)
data['duplicate_check'] = data['author'] + data['published_at'].astype(str)
print("Duplicate comments:", data['duplicate_check'].duplicated().sum())
data = data.drop(columns=['duplicate_check'])

# Step 10.5: Basic validation
print("\nDataset Info:")
print(data.info())
print("\nMissing Values:")
print(data.isnull().sum())
print("\nRow Count:", len(data))

# Step 10.6: Save the corrected CSV
data.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8')
print(f"\nFixed CSV saved to '{OUTPUT_FILE}'")