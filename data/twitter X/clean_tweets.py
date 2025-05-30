
import pandas as pd
import csv
import re
from io import StringIO
import os

# Define file paths
INPUT_FILE = r'C:\Users\fujitus\Desktop\Me\NLP_Emotions_Tracker\data\x_tweets.csv'
OUTPUT_FILE = r'C:\Users\fujitus\Desktop\Me\NLP_Emotions_Tracker\data\x_tweets_fixed.csv'

# Verify input file exists
if not os.path.exists(INPUT_FILE):
    print(f"Input file not found at: {INPUT_FILE}")
    print("Please ensure x_tweets.csv exists in the data directory or provide the correct path.")
    raise FileNotFoundError(f"Input file not found at: {INPUT_FILE}. Please check the path and ensure the file exists.")

# Step 1: Read the CSV with robust parsing
try:
    data = pd.read_csv(INPUT_FILE, quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8', on_bad_lines='warn')
except Exception as e:
    print(f"Error reading CSV: {e}")
    # Fallback: Manual parsing
    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        raw_data = file.read()
    csv_buffer = StringIO(raw_data)
    data = pd.read_csv(csv_buffer, quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8', on_bad_lines='warn')

# Step 2: Text Preprocessing for Content column
def clean_text(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    # Encode to handle emojis and non-ASCII characters
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    # Replace newlines and carriage returns with spaces
    text = re.sub(r'[\n\r]+', ' ', text)
    # Escape double quotes for CSV compatibility
    text = text.replace('"', '""')
    # Normalize multiple spaces and tabs
    text = re.sub(r'\s+', ' ', text)
    # Simplify URLs, mentions, and hashtags
    text = re.sub(r'https?://\S+', '[URL]', text)
    text = re.sub(r'@\S+', '[USER]', text)
    text = re.sub(r'#\S+', '[HASHTAG]', text)
    # Trim leading/trailing spaces
    return text.strip()

# Apply cleaning to Content column
data['Content'] = data['Content'].apply(clean_text)

# Step 3: Validate and clean other columns
# Convert Date to datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Drop rows with missing Tweet ID or Content
data = data.dropna(subset=['Tweet ID', 'Content'])

# Check for duplicates
print("Duplicate Tweet IDs:", data['Tweet ID'].duplicated().sum())

# Step 4: Basic validation
print("\nDataset Info:")
print(data.info())
print("\nMissing Values:")
print(data.isnull().sum())
print("\nRow Count:", len(data))

# Step 5: Save the corrected CSV
data.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8')
print(f"\nFixed CSV saved to '{OUTPUT_FILE}'")