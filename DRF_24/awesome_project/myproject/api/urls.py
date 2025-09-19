from django.urls import path
from .views import BookListCreateAPIView, BookDetailAPIView, CategoryListCreateAPIView, CategoryDetailAPIView


urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
]

