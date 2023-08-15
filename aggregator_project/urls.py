# aggregator_project/urls.py

from django.contrib import admin
from django.urls import path, include
from news.views import HomePageView, CategoryPageView


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', HomePageView.as_view(), name='home_page'),
    path('category/<str:category>/', CategoryPageView.as_view(), name='category_page'),
]


