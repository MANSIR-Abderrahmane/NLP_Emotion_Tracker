# backend/api/management/commands/randomize_platforms.py

import random
from django.core.management.base import BaseCommand
from api.models import Post

class Command(BaseCommand):
    help = 'Randomizes the platform field for all existing Post objects.'

    def handle(self, *args, **kwargs):
        platforms = ["X", "Instagram", "Facebook", "YouTube", "Reddit"]
        
        self.stdout.write(self.style.SUCCESS("Starting platform randomization for posts..."))
        
        posts = Post.objects.all()
        updated_count = 0

        for post in posts:
            original_platform = post.platform
            new_platform = random.choice(platforms)
            
            if original_platform != new_platform:
                post.platform = new_platform
                post.save()
                updated_count += 1
                self.stdout.write(f"Updated Post ID {post.id}: Platform changed from '{original_platform}' to '{new_platform}'")
            else:
                self.stdout.write(f"Post ID {post.id}: Platform remains '{original_platform}' (random choice was the same)")


        self.stdout.write(self.style.SUCCESS(f"\nCompleted! {updated_count} posts had their platform updated."))
        if updated_count < len(posts):
            self.stdout.write(self.style.WARNING(f"{len(posts) - updated_count} posts already had the randomly chosen platform."))