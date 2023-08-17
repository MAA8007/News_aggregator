from django.core.management.base import BaseCommand
from django.core import management
from news.models import NewsItem  

class Command(BaseCommand):
    help = 'Run the scrape_news command followed by the runserver command'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting scrape_news...'))
        management.call_command('scrape_news', *args, **options)
        
        self.stdout.write(self.style.SUCCESS('Starting runserver...'))
        management.call_command('runserver', *args, **options)
