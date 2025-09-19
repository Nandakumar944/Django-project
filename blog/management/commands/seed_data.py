from django.core.management.base import BaseCommand
from blog.models import Category, Tag
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed initial categories and tags"

    def handle(self, *args, **kwargs):
        categories = ["Technology", "Health", "Travel", "Education", "Food"]
        tags = ["Python", "Django", "AI", "Machine Learning", "Fitness", "Recipes"]

        for name in categories:
            Category.objects.update_or_create(
                name=name,
                defaults={"slug": slugify(name)},
            )

        for name in tags:
            Tag.objects.update_or_create(
                name=name,
                defaults={"slug": slugify(name)},
            )

        self.stdout.write(self.style.SUCCESS("Categories and Tags seeded successfully!"))