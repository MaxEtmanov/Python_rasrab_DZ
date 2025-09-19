from flask import Flask, request, jsonify, session
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'z-restapi-23-secret-key'

# Базовые декораторы для проверки ролей
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Login required'}), 401
            
            user_role = session.get('role')
            if user_role not in allowed_roles:
                return jsonify({
                    'error': f'Access denied. Required roles: {allowed_roles}',
                    'your_role': user_role
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Специализированные декораторы
def admin_only(f):
    @wraps(f)
    @role_required('admin')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def manager_or_admin(f):
    @wraps(f)
    @role_required('admin', 'manager')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def authenticated_user(f):
    @wraps(f)
    @role_required('admin', 'manager', 'user')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

# Логин
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users WHERE username = ? AND password = ?", 
              (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['role'] = user[2]
        return jsonify({'message': 'Login successful', 'role': user[2]})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# АДМИНСКИЕ РЕСУРСЫ
@app.route('/admin/dashboard')
@admin_only
def admin_dashboard():
    return jsonify({
        'message': 'Admin Dashboard',
        'user': session['username'],
        'permissions': ['create', 'read', 'update', 'delete', 'manage_users']
    })

@app.route('/admin/users')
@admin_only
def manage_users():
    return jsonify({
        'message': 'User Management Panel',
        'users': ['admin', 'manager', 'user'],
        'actions': ['create', 'edit', 'delete', 'change_roles']
    })

@app.route('/admin/system-settings')
@admin_only
def system_settings():
    return jsonify({
        'message': 'System Settings',
        'settings': ['database', 'security', 'backup']
    })

# МЕНЕДЖЕРСКИЕ РЕСУРСЫ
@app.route('/manager/projects')
@manager_or_admin
def manager_projects():
    return jsonify({
        'message': 'Project Management',
        'user': session['username'],
        'role': session['role'],
        'permissions': ['view_projects', 'edit_tasks', 'assign_tasks']
    })

@app.route('/manager/tasks')
@manager_or_admin
def manage_tasks():
    return jsonify({
        'message': 'Task Management',
        'actions': ['create_task', 'edit_task', 'assign_task', 'view_reports']
    })

@app.route('/manager/reports')
@manager_or_admin
def view_reports():
    return jsonify({
        'message': 'Reports and Analytics',
        'reports': ['task_progress', 'user_activity', 'project_status']
    })

# ПОЛЬЗОВАТЕЛЬСКИЕ РЕСУРСЫ
@app.route('/user/profile')
@authenticated_user
def user_profile():
    return jsonify({
        'message': 'User Profile',
        'username': session['username'],
        'role': session['role'],
        'permissions': ['view_tasks', 'add_comments', 'mark_complete']
    })

@app.route('/user/my-tasks')
@authenticated_user
def my_tasks():
    return jsonify({
        'message': 'My Tasks',
        'user': session['username'],
        'tasks': ['Task 1', 'Task 2', 'Task 3']
    })

@app.route('/user/notifications')
@authenticated_user
def notifications():
    return jsonify({
        'message': 'Notifications',
        'notifications': ['New task assigned', 'Project updated']
    })

# ОБЩИЕ РЕСУРСЫ (для всех авторизованных)
@app.route('/dashboard')
@login_required
def general_dashboard():
    user_role = session.get('role')
    
    # Разные данные в зависимости от роли
    if user_role == 'admin':
        data = {
            'view': 'Admin Dashboard',
            'widgets': ['users', 'projects', 'system', 'reports']
        }
    elif user_role == 'manager':
        data = {
            'view': 'Manager Dashboard', 
            'widgets': ['projects', 'tasks', 'team']
        }
    else:
        data = {
            'view': 'User Dashboard',
            'widgets': ['my_tasks', 'notifications']
        }
    
    return jsonify({
        'message': f'Welcome {session["username"]}',
        'role': user_role,
        'dashboard': data
    })

# РЕСУРС С МНОЖЕСТВЕННЫМИ РОЛЯМИ
@app.route('/projects/view')
@role_required('admin', 'manager', 'user')
def view_projects():
    user_role = session.get('role')
    
    # Разные уровни доступа
    if user_role == 'admin':
        projects = ['All Projects', 'Hidden Projects', 'Archived Projects']
    elif user_role == 'manager':
        projects = ['Active Projects', 'My Projects']
    else:
        projects = ['Assigned Projects']
    
    return jsonify({
        'message': 'Projects View',
        'role': user_role,
        'projects': projects
    })

# Проверка доступа
@app.route('/check-access/<resource>')
@login_required
def check_access(resource):
    user_role = session.get('role')
    
    access_map = {
        'admin_panel': ['admin'],
        'user_management': ['admin'],
        'project_management': ['admin', 'manager'],
        'task_management': ['admin', 'manager'],
        'profile': ['admin', 'manager', 'user'],
        'reports': ['admin', 'manager']
    }
    
    has_access = user_role in access_map.get(resource, [])
    
    return jsonify({
        'resource': resource,
        'user_role': user_role,
        'has_access': has_access,
        'required_roles': access_map.get(resource, [])
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'})

if __name__ == '__main__':
    app.run(debug=True)
