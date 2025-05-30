import csv
import os
import re # For content cleaning
from datetime import datetime
from dateutil.parser import parse as date_parse # For robust date parsing
import uuid # Add this import for generating unique IDs
import hashlib # Add this import if you want to use it directly, though uuid.uuid5 handles hashing internally

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models import Post # Adjust this if your Post model is in a different app/location

from emotion_analyzer.analyzer import analyze_emotion, load_hybrid_models


class Command(BaseCommand):
    help = 'Imports social media post data from CSV files located in the "data" directory.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Specify a single CSV file to import (e.g., --file twitter_posts.csv)',
            nargs='?', # Makes the argument optional
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Loading emotion analysis models..."))
        load_hybrid_models()
        self.stdout.write(self.style.SUCCESS("Emotion analysis models loaded."))


        data_dir = os.path.join(settings.BASE_DIR.parent, 'data', 'clean data') # Path to the 'data' folder
        if not os.path.exists(data_dir):
            raise CommandError(f"Data directory not found at: {data_dir}")

        csv_files = []
        if options['file']:
            # If a specific file is provided, check if it exists
            specific_file_path = os.path.join(data_dir, options['file'])
            if not os.path.exists(specific_file_path):
                raise CommandError(f"Specified file not found: {specific_file_path}")
            csv_files.append(specific_file_path)
        else:
            # If no specific file, find all CSVs in the data directory
            for f in os.listdir(data_dir):
                if f.endswith('.csv'):
                    csv_files.append(os.path.join(data_dir, f))

        if not csv_files:
            raise CommandError("No CSV files found in the 'data' directory or specified file does not exist.")

        self.stdout.write(self.style.MIGRATE_HEADING(f"Found {len(csv_files)} CSV files to import."))

        for csv_file_path in csv_files:
            self.stdout.write(f"Importing data from {os.path.basename(csv_file_path)}...")
            num_imported = 0
            num_skipped = 0

            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    content = row.get('text') # Assuming 'text' column for content
                    if not content or not content.strip():
                        num_skipped += 1
                        continue # Skip empty content

                    # Clean content (basic example, extend as needed)
                    content = re.sub(r'\s+', ' ', content).strip() # Replace multiple spaces with single, strip whitespace

                    # Original post_id from CSV (this might be author for comments)
                    original_id_from_csv = row.get('id')
                    platform_base_name = os.path.basename(csv_file_path).replace('_fixed.csv', '').replace('_posts.csv', '').replace('_comments.csv', '')
                    platform = platform_base_name # Use this for database filtering if needed later

                    # Derive author from original_id_from_csv if it looks like a username
                    # Otherwise, use the 'author' column or default to 'anonymous'
                    author = row.get('author', 'anonymous')
                    if original_id_from_csv and original_id_from_csv.startswith('@'):
                        author = original_id_from_csv # Assume @username is the author
                    # If the CSV has an 'author' column and it's present, prioritize it
                    elif row.get('author') and row.get('author').strip():
                        author = row.get('author').strip()


                    likes = int(row.get('likes', 0)) # Default to 0 likes

                    # Robust date parsing
                    date_str = row.get('date') or row.get('created_at') or row.get('timestamp')
                    date_obj = None
                    if date_str:
                        try:
                            date_obj = date_parse(date_str)
                        except (ValueError, TypeError):
                            self.stdout.write(self.style.WARNING(f"Could not parse date '{date_str}' for row {reader.line_num} in {os.path.basename(csv_file_path)}. Using current date."))
                            date_obj = datetime.now()
                    else:
                        date_obj = datetime.now() # Fallback to current date if no date found

                    # Generate a truly unique external_id for each post/comment
                    # This ensures uniqueness even if the original 'id' from CSV is not unique (e.g., author names).
                    # We use uuid.uuid5 with a namespace and a unique string derived from platform,
                    # original CSV ID (author), content, and timestamp for stability.
                    unique_identifier_string = f"{platform}-{original_id_from_csv}-{content}-{date_obj.isoformat()}"
                    # Ensure the string is consistently encoded for hashing
                    post_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_identifier_string.encode('utf-8').decode('latin-1')))


                    # EMOTION ANALYSIS:
                    try:
                        analysis_results = analyze_emotion(content)
                        primary_emotion = analysis_results["emotion_primary"]
                        primary_score = analysis_results["emotion_score"]
                        secondary_emotions = analysis_results["secondary_emotions_json"]
                    except Exception as e:
                        primary_emotion = "neutral" # Default to neutral on analysis error
                        primary_score = 0.0
                        secondary_emotions = {}
                        self.stdout.write(self.style.ERROR(f"Error analyzing emotion for row {reader.line_num} (Generated ID: {post_id}): {e} - Content: {content[:50]}..."))


                    try:
                        # Check for existing post to avoid duplicates based on *generated* external_id and platform
                        if Post.objects.filter(external_id=post_id, platform=platform).exists():
                            num_skipped += 1
                            self.stdout.write(self.style.WARNING(f"Skipping duplicate post (Generated ID: {post_id}) from {platform}."))
                            continue

                        Post.objects.create(
                            external_id=post_id, # Use the generated unique ID
                            content=content,
                            platform=platform,
                            author=author,
                            date=date_obj,
                            likes=likes,
                            emotion_primary=primary_emotion,
                            emotion_score=primary_score,
                            secondary_emotions_json=secondary_emotions # If you have a JSONField
                        )
                        num_imported += 1
                        self.stdout.write(self.style.SUCCESS(f"Imported (Generated ID: {post_id} - Original CSV ID: {original_id_from_csv}): {content[:70]}... -> Emotion: {primary_emotion}"))

                    except Exception as e:
                        num_skipped += 1
                        self.stdout.write(self.style.ERROR(f"Error importing row {reader.line_num} (Generated ID: {post_id}) from {os.path.basename(csv_file_path)}: {e} - Row: {row}"))

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {num_imported} posts from {os.path.basename(csv_file_path)}."))
            self.stdout.write(self.style.WARNING(f"Skipped {num_skipped} rows from {os.path.basename(csv_file_path)} due to errors, duplicates, or empty content."))

        self.stdout.write(self.style.SUCCESS("\nData import process completed."))