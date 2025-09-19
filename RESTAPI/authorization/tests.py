from django.test import TestCase

import unittest
import json
from dz_file import app
import sqlite3
import os

class TestRoleAccess(unittest.TestCase):
    
    def setUp(self):
        # Настройка тестового окружения
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Создаем тестовую БД
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
        
        # Тестовые пользователи
        users = [
            ('admin_test', '123', 'admin'),
            ('manager_test', '123', 'manager'),
            ('user_test', '123', 'user')
        ]
        
        for username, password, role in users:
            c.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)",
                      (username, password, role))
        
        conn.commit()
        conn.close()
    
    def login_user(self, username, password):
        """Вспомогательная функция для логина"""
        return self.app.post('/login',
                           data=json.dumps({'username': username, 'password': password}),
                           content_type='application/json')
    
    def test_admin_access(self):
        """Тест доступа администратора"""
        # Логин админа
        response = self.login_user('admin_test', '123')
        self.assertEqual(response.status_code, 200)
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['username'] = 'admin_test'
                sess['role'] = 'admin'
            
            # Админ должен иметь доступ ко всем ресурсам
            admin_routes = [
                '/admin/dashboard',
                '/admin/users',
                '/admin/system-settings',
                '/manager/projects',
                '/user/profile'
            ]
            
            for route in admin_routes:
                response = client.get(route)
                self.assertEqual(response.status_code, 200, f"Admin should access {route}")
    
    def test_manager_access(self):
        """Тест доступа менеджера"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 2
                sess['username'] = 'manager_test'
                sess['role'] = 'manager'
            
            # Менеджер может получить доступ к своим ресурсам
            allowed_routes = [
                '/manager/projects',
                '/manager/tasks',
                '/user/profile',
                '/dashboard'
            ]
            
            for route in allowed_routes:
                response = client.get(route)
                self.assertEqual(response.status_code, 200, f"Manager should access {route}")
            
            # Менеджер НЕ может получить доступ к админским ресурсам
            forbidden_routes = [
                '/admin/dashboard',
                '/admin/users',
                '/admin/system-settings'
            ]
            
            for route in forbidden_routes:
                response = client.get(route)
                self.assertEqual(response.status_code, 403, f"Manager should NOT access {route}")
    
    def test_user_access(self):
        """Тест доступа обычного пользователя"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 3
                sess['username'] = 'user_test'
                sess['role'] = 'user'
            
            # Пользователь может получить доступ только к своим ресурсам
            allowed_routes = [
                '/user/profile',
                '/user/my-tasks',
                '/user/notifications',
                '/dashboard'
            ]
            
            for route in allowed_routes:
                response = client.get(route)
                self.assertEqual(response.status_code, 200, f"User should access {route}")
            
            # Пользователь НЕ может получить доступ к админским и менеджерским ресурсам
            forbidden_routes = [
                '/admin/dashboard',
                '/admin/users',
                '/manager/projects',
                '/manager/tasks'
            ]
            
            for route in forbidden_routes:
                response = client.get(route)
                self.assertEqual(response.status_code, 403, f"User should NOT access {route}")
    
    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        protected_routes = [
            '/admin/dashboard',
            '/manager/projects',
            '/user/profile',
            '/dashboard'
        ]
        
        for route in protected_routes:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 401, f"Unauthorized should NOT access {route}")
    
    def test_login_logout(self):
        """Тест логина и логаута"""
        # Тест успешного логина
        response = self.login_user('admin_test', '123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['role'], 'admin')
        
        # Тест неправильного логина
        response = self.login_user('wrong_user', 'wrong_pass')
        self.assertEqual(response.status_code, 401)
        
        # Тест логаута
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['username'] = 'admin_test'
                sess['role'] = 'admin'
            
            response = client.post('/logout')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()