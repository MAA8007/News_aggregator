from django.views.generic import ListView, DetailView
from .models import NewsItem
import random


class HomePageView(ListView):
    template_name = 'home.html'
    model = NewsItem
    context_object_name = 'latest_articles'

    def get_queryset(self):
        selected_categories = ["Formula 1", "Liverpool FC", "Pakistan", "Football", "Science & Technology", "Global News", "Self Dev"]
        latest_articles = [NewsItem.objects.filter(category=category).latest('published') for category in selected_categories if NewsItem.objects.filter(category=category).exists()]
        return latest_articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = NewsItem.objects.values_list('category', flat=True).distinct()
        context['categories'] = categories
        return context

class CategoryPageView(ListView):
    template_name = 'category.html'
    model = NewsItem
    context_object_name = 'articles'
    paginate_by = 13

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # This is the current page number
        current_page = context['page_obj'].number

        # This is the total number of pages
        total_pages = context['paginator'].num_pages

        # We'll display up to 5 pages (for example) around the current page.
        pages_before = list(range(max(current_page - 2, 1), current_page))
        pages_after = list(range(current_page + 1, min(current_page + 3, total_pages + 1)))

        # Add these new context variables
        context['pages_before'] = pages_before
        context['pages_after'] = pages_after
        context['show_first_ellipsis'] = pages_before[0] > 2 if pages_before else current_page > 1
        context['show_last_ellipsis'] = pages_after[-1] < total_pages - 1 if pages_after else current_page < total_pages

        categories = NewsItem.objects.values_list('category', flat=True).distinct()
        context['categories'] = categories
        return context

    def get_queryset(self):
        return NewsItem.objects.filter(category=self.kwargs['category']).order_by('-published')
