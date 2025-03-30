
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post

class SimpleTests(TestCase):
    """Простые тесты для проверки работы блога"""
    
    def setUp(self):
        """Подготовка данных для тестов"""
        # Создаем тестовый пост
        self.post = Post.objects.create(
            title='Тестовый заголовок',
            content='Тестовое содержание поста'
        )
        
        # Создаем клиент для запросов
        self.client = Client()
    
    def test_post_list_exists(self):
        """Проверка доступности страницы со списком постов"""
        url = reverse('post_list')
        response = self.client.get(url)
        
        # Проверяем, что страница загружается успешно
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что наш тестовый пост отображается на странице
        self.assertContains(response, 'Тестовый заголовок')
    
    def test_post_detail_exists(self):
        """Проверка доступности страницы с деталями поста"""
        url = reverse('post_detail', args=[self.post.id])
        response = self.client.get(url)
        
        # Проверяем, что страница загружается успешно
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что содержимое поста отображается
        self.assertContains(response, 'Тестовый заголовок')
        self.assertContains(response, 'Тестовое содержание поста')
    
    def test_create_post(self):
        """Проверка создания нового поста"""
        url = reverse('post_create')
        
        # Отправляем данные для создания поста
        data = {
            'title': 'Новый пост',
            'content': 'Содержание нового поста'
        }
        response = self.client.post(url, data)
        
        # Проверяем, что после создания происходит перенаправление
        self.assertEqual(response.status_code, 302)
        
        # Проверяем, что пост был создан в базе данных
        self.assertTrue(Post.objects.filter(title='Новый пост').exists())
