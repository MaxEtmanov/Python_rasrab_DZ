from django.db import models

# Create your models here.

class Product(models.Model):
    """
    Модель для представления товаров в магазине.
    
    Содержит основную информацию о товаре: название, описание,
    цену, изображение и дату создания записи.
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    image =models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
