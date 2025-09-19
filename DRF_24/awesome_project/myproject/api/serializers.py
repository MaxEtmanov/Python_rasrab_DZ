from rest_framework import serializers
from .models import Book, Category

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'title': {'help_text': 'Название книги'},
            'author': {'help_text': 'Автор книги'},
            'published_date': {'help_text': 'Дата публикации (формат YYYY-MM-DD)'},
            'isbn': {'help_text': 'Уникальный ISBN номер книги'},
            'page_count': {'help_text': 'Количество страниц'},
            'cover': {'help_text': 'Ссылка на изображение обложки'},
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']