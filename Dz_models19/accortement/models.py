from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Название",
        help_text="Название категории"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Описание",
        help_text="Описание категории (необязательно)"
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='children',
        verbose_name="Родительская категория",
        help_text="Выберите родительскую категорию для создания подкategории"
    )
    
class Product(models.Model):
    name = models.CharField(
        max_length=200, 
        verbose_name="Название товара",
        help_text="Название товара (обязательное поле)"
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Подробное описание товара"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Цена",
        help_text="Цена товара в рублях"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество на складе",
        help_text="Доступное количество товара на складе"
    )
    #image = models.ImageField(
        #upload_to='products/%Y/%m/%d/', 
        #blank=True, 
        #null=True,
        #verbose_name="Изображение товара",
        #help_text="Основное изображение товара (необязательно)"
    #)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория",
        help_text="Категория, к которой относится товар"
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
        help_text="Дата и время добавления товара"
    )
    
    class Meta:
        db_table = 'shop_products'
        ordering = ['-date_added']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        unique_together = ['name', 'category']
        
    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('shipping', 'Доставляется'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing',
        verbose_name="Статус заказа"
    )
    
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Общая стоимость"
    )
    
    def total_price(self):  # ← ДОБАВЛЕНО: метод для вычисления общей стоимости
        """Вычисляет общую стоимость заказа"""
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    
class Review(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Товар"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Пользователь"
    )
    
    rating = models.IntegerField(
        verbose_name="Оценка"
    )
    
    text = models.TextField(
        verbose_name="Текст отзыва"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
