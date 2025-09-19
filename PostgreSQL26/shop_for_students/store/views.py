from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, CartItem
from django.db.models import F, Sum
from .models import Product, Category
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Проверяем параметр next в URL
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Проверяем параметр next в URL
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('product_list')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('product_list')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = cart_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    # Проверяем, авторизован ли пользователь
    if not request.user.is_authenticated:
        # Сохраняем URL, на который нужно вернуться после авторизации
        request.session['next_url'] = request.path
        return redirect('register')
        
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')  # Перенаправляем пользователя на страницу корзины
    return HttpResponse("Invalid request", status=400)

def clear_cart(request):
    if request.user.is_authenticated:
        # Удаляем только элементы корзины текущего пользователя
        CartItem.objects.filter(user=request.user).delete()
    # Перенаправляем обратно на страницу корзины
    return redirect('cart')

def add_product(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        
        # Создаем новый товар
        product = Product(
            name=name,
            description=description,
            price=price,
        )
        
        # Добавляем категорию, только если она выбрана
        if category_id:
            category = Category.objects.get(id=category_id)
            product.category = category
        
        # Обрабатываем изображение, если оно есть
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            product.image = filename
        
        # Сохраняем товар
        product.save()
        
        # Перенаправляем на главную страницу
        return redirect('product_list')
    
    return render(request, 'store/add_product.html', {'categories': categories})


