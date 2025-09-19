from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    # Переносим поле создания новой категории в ProductForm
    new_category_name = forms.CharField(
        max_length=100,
        required=False,
        label='Или создать новую категорию',
        help_text='Если заполните это поле, будет создана новая категория'
    )
    
    price = forms.DecimalField(
        required=True,
        min_value=0.01,
        decimal_places=2,
        max_digits=10,
        error_messages={
            'required': 'Цена обязательна для заполнения',
            'min_value': 'Цена должна быть больше 0'
        }
    )
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле category необязательным
        self.fields['category'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category_name = cleaned_data.get('new_category_name')
        
        # Проверяем, что выбрана либо существующая категория, либо указано имя новой
        if not category and not new_category_name:
            raise forms.ValidationError('Выберите категорию или создайте новую')
        
        return cleaned_data
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price:
            raise forms.ValidationError('Поле цена не может быть пустым')
        if price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля')
        return price
    
class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории"
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        label="Цена от"
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        label="Цена до"
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Без сортировки'),
            ('price', 'Цена по возрастанию'),
            ('-price', 'Цена по убыванию'),
            ('created_at', 'Дата по возрастанию'),
            ('-created_at', 'Дата по убыванию'),
        ]
    )