from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название книги")
    author = models.CharField(max_length=255, verbose_name="Автор")
    published_date = models.DateField(verbose_name="Дата публикации")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    page_count = models.PositiveIntegerField(verbose_name="Количество страниц")
    cover = models.URLField(blank=True, verbose_name="Обложка книги (URL)")

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']  # Сортировка по названию
    
    def __str__(self):
        return self.name