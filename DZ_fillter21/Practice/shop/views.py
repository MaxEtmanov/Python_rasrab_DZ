from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import User, Order, Product, OrderItem


def recent_orders_view(request):
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    
    # Аннотируем количество заказов за последние 30 дней для каждого пользователя
    users_with_recent_orders = User.objects.annotate(
        recent_order_count=Count('order', filter=Q(order__created_at__gte=thirty_days_ago))
    ).filter(recent_order_count__gt=0)

    return render(request, 'shop/recent_orders.html', {'users': users_with_recent_orders})


def product_filter_view(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    period = request.GET.get('period')
    sort =  request.GET.get('sort')
    
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if period and period in ['7', '30','180', '365']:
        if period == '7':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7))
        elif period == '30':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30))
        elif period == '180':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=180))
        elif period == '365':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=365))
    
    # Исправленная сортировка - добавлена проверка на пустое значение
    if sort and sort.strip():  # Проверяем что sort не пустой и не None
        products = products.order_by(sort)
        
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'shop/product_list.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'paginator': paginator
    })
    
def ajax_product_list_view(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    period = request.GET.get('period')
    sort = request.GET.get('sort')
    
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if period and period in ['week', 'month', 'year']:
        if period == 'week':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7))
        elif period == 'month':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30))
        elif period == 'year':
            products = products.filter(created_at__gte=timezone.now() - timezone.timedelta(days=365))
    
    valid_sorts = ['id', '-id', 'price', '-price', 'name', '-name']
    if sort in valid_sorts:
        products = products.order_by(sort)
    
    # Пагинация для AJAX
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Формируем JSON ответ
    products_data = []
    for product in page_obj:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'category': product.category,
        })
    
    return JsonResponse({
        'products': products_data,
        'total_count': paginator.count,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })


def popular_products_view(request):
    products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')  # сортировка по количеству заказов в убывающем порядке

    return render(request, 'shop/popular_products.html', {'products': products})

def combined_filter_view(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    period = request.GET.get('period')
    sort = request.GET.get('sort', '-order_count')
    
    products = Product.objects.annotate(
        order_count=Count('orderitem')
    )
    
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if period:
        days = int(period)
        date_from = timezone.now() - timezone.timedelta(days=days)
        products = products.filter(created_at__gte=date_from)
    
    products = products.order_by(sort)
    
    return render(request, 'shop/combined_filter.html', {'products': products})