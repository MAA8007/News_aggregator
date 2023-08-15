# news/services.py

from .models import NewsItem

def create_news_item(title, link, category, website, published, image):
    # Use get_or_create to either fetch the existing item or create a new one
    item, created = NewsItem.objects.get_or_create(
        link=link,
        defaults={
            'title': title,
            'category': category,
            'website': website,
            'published': published,
            'image':image
        }
    )

    # If not created, it means it's a duplicate.
    # You can log or handle as needed.
    if not created:
        print(f"Duplicate article found: {link}")
        return None  # Return None if a duplicate was found

    return item  # Return the created or found item
