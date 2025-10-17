Этот проект реализует простое веб-приложение на Django, включающее три основных функции:

Регистрация пользователей с дополнительными полями phone_number и bio.

Авторизация пользователей с проверкой имени пользователя и пароля.

Отправка сообщений зарегистрированными пользователями с проверкой валидности данных.

Приложение демонстрирует работу с формами (ModelForm, Form), валидацией, маршрутами (urls.py), шаблонами и системой сообщений Django.

⚙️ Установка и запуск
1. Клонировать репозиторий
git clone https://github.com/yourusername/dz_form.git
cd dz_form

2. Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

3. Установить зависимости
pip install django

4. Применить миграции
python manage.py makemigrations
python manage.py migrate

5. Создать суперпользователя (по желанию)
python manage.py createsuperuser

6. Запустить сервер
python manage.py runserver
