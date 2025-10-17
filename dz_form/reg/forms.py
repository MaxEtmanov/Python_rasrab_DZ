from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Message

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    """
    ModelForm для регистрации: поля username, email + password1/password2 (не в модели).
    При save() устанавливает хеш пароля через set_password.
    """
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        # показываем username и email (phone/bio можно добавить если хотим)
        fields = ('username', 'email', 'phone_number', 'bio')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email__iexact=email)
            if qs.exists():
                raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError({'password2': 'Пароли не совпадают.'})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def authenticate_user(self, request):
        from django.contrib.auth import authenticate
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        return user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'text')

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if not text:
            raise ValidationError('Поле сообщения не должно быть пустым.')
        if len(text) > 500:
            raise ValidationError('Сообщение не должно превышать 500 символов.')
        return text