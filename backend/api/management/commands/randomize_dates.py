# backend/api/management/commands/randomize_dates.py

import random
from datetime import datetime, date, timedelta
from django.core.management.base import BaseCommand
from api.models import Post # Adjust this import if your Post model is in a different app/location

class Command(BaseCommand):
    help = 'Randomizes the date field for all existing Post objects within a specific range of months.'

    def handle(self, *args, **kwargs):
        # Define the target year and months
        target_year = 2025 # You can change this to the current year or any desired year
        
        # Define the start and end dates for the random period
        # We'll use the 1st of each month to define the range
        month_ranges = [
            (datetime(target_year, 1, 1), datetime(target_year, 1, 31)),   # Jan
            (datetime(target_year, 2, 1), datetime(target_year, 2, 28)),   # Feb (simplification, consider leap year if critical)
            (datetime(target_year, 3, 1), datetime(target_year, 3, 31)),   # Mar
            (datetime(target_year, 4, 1), datetime(target_year, 4, 30)),   # Apr
            (datetime(target_year, 5, 1), datetime(target_year, 5, 31)),   # May
            (datetime(target_year, 6, 1), datetime(target_year, 6, 30)),   # Jun
            (datetime(target_year, 7, 1), datetime(target_year, 7, 31)),   # Jul
        ]
        
        self.stdout.write(self.style.SUCCESS("Starting date randomization for posts..."))
        
        posts = Post.objects.all()
        updated_count = 0

        for post in posts:
            # Randomly choose a month range
            start_date_of_month, end_date_of_month = random.choice(month_ranges)
            
            # Calculate the number of days in the chosen month range
            delta = end_date_of_month - start_date_of_month
            random_days = random.randint(0, delta.days)
            
            # Generate a random date within that range
            random_date_in_month = start_date_of_month + timedelta(days=random_days)
            
            # Assign a random time of day (hours, minutes, seconds)
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            
            new_date = random_date_in_month.replace(
                hour=random_hour,
                minute=random_minute,
                second=random_second,
                microsecond=0 # Reset microseconds for consistency
            )

            # Only update if the date has significantly changed to avoid unnecessary saves
            # For simplicity, we'll always save, but in large datasets, you might add a check
            post.date = new_date
            post.save()
            updated_count += 1
            self.stdout.write(f"Updated Post ID {post.id}: Date changed to '{new_date.strftime('%Y-%m-%d %H:%M:%S')}'")

        self.stdout.write(self.style.SUCCESS(f"\nCompleted! {updated_count} posts had their date updated."))
        self.stdout.write(self.style.WARNING("Remember to run 'python manage.py makemigrations' and 'python manage.py migrate' if you changed the 'date' field properties in your model."))