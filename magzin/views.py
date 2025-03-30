from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def product_list(request):
    """
    Отображает список всех товаров.
    
    Получает все товары из базы данных и передает их в шаблон product_list.html
    для отображения в виде списка.
    """
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    """
    Отображает детальную информацию о конкретном товаре.
    
    Получает товар по его ID из базы данных или возвращает 404 ошибку,
    если товар не найден. Передает данные товара в шаблон product_detail.html.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

