from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductFilterForm
from django.db.models import Sum, Count, Avg, Min, Max

#Category views
def category_stats(request):
    categories = Category.objects.annotate(
        total_products=Count('products'),  
        total_value=Sum('products__price'),  
        avg_price=Avg('products__price'), 
        min_price=Min('products__price'),  
        max_price=Max('products__price')  
    )
    
    # Общая статистика
    total_products = Product.objects.count()
    total_stats = Product.objects.aggregate(
        total_value=Sum('price'),
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    return render(request, 'shop/category_stats.html', {
        'categories': categories,
        'total_products': total_products,
        'total_value': total_stats['total_value'] or 0,
        'min_price': total_stats['min_price'],
        'max_price': total_stats['max_price']
    })

# List of all products
def product_list(request):
    products = Product.objects.all()
    filter_form = ProductFilterForm(request.GET or None)
    
    if filter_form.is_valid():
        # Фильтр по категории
        if filter_form.cleaned_data['category']:
            products = products.filter(category=filter_form.cleaned_data['category'])
        
        # Фильтр по минимальной цене
        if filter_form.cleaned_data['min_price']:
            products = products.filter(price__gte=filter_form.cleaned_data['min_price'])
        
        # Фильтр по максимальной цене
        if filter_form.cleaned_data['max_price']:
            products = products.filter(price__lte=filter_form.cleaned_data['max_price'])
        
        # Сортировка
        if filter_form.cleaned_data['sort_by']:
            products = products.order_by(filter_form.cleaned_data['sort_by'])
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'filter_form': filter_form
    })

# Creating a new product
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        # Проверяем, нужно ли создать новую категорию
        new_category_name = form.cleaned_data.get('new_category_name')
        if new_category_name:
            # Создаем новую категорию
            category, created = Category.objects.get_or_create(name=new_category_name)
            # Привязываем к товару
            product = form.save(commit=False)
            product.category = category
            product.save()
        else:
            form.save()
        return redirect('product_list')
    return render(request, 'shop/create_product.html', {'form': form})

# Reading a single product's details
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# Updating an existing product
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'shop/update_product.html', {'form': form})

# Deleting a product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/delete_product.html', {'product': product})
