from django.urls import path
from .views import HomePageView, CategoryPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('category/<str:category>/', CategoryPageView.as_view(), name='category_page'),
]
