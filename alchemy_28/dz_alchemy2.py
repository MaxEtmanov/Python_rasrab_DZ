from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базу данных в памяти
engine = create_engine('sqlite:///database2.db', echo=True)
Base = declarative_base()

# Определяем модель User
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"

# Создаем таблицы
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Функция для вывода всех пользователей
def show_all_users():
    users = session.query(User).all()
    if users:
        print("\nСписок пользователей в базе данных:")
        for user in users:
            print(f"  - {user}")
    else:
        print("\nБаза данных пуста. Пользователей нет.")

# Проверяем начальное состояние
print("\n=== НАЧАЛЬНОЕ СОСТОЯНИЕ ===")
show_all_users()

# Пример 1: Успешная транзакция
print("\n=== ПРИМЕР 1: УСПЕШНАЯ ТРАНЗАКЦИЯ ===")
try:
    # Начинаем транзакцию
    user1 = User(username="user1", email="user1@example.com")
    user2 = User(username="user2", email="user2@example.com")
    
    session.add(user1)
    session.add(user2)
    
    # Фиксируем изменения
    session.commit()
    print("Транзакция успешно выполнена!")
except Exception as e:
    # Откатываем изменения в случае ошибки
    session.rollback()
    print(f"Ошибка: {e}")
    print("Изменения откачены!")

# Проверяем состояние после первой транзакции
show_all_users()

# Пример 2: Транзакция с ошибкой
print("\n=== ПРИМЕР 2: ТРАНЗАКЦИЯ С ОШИБКОЙ ===")
try:
    # Начинаем транзакцию
    user3 = User(username="user3", email="user3@example.com")
    user4 = User(username="user4", email="user4@example.com")
    
    session.add(user3)
    session.add(user4)
    
    # Имитируем ошибку - добавляем пользователя с существующим именем
    user_duplicate = User(username="user1", email="duplicate@example.com")
    session.add(user_duplicate)
    
    # Пытаемся зафиксировать изменения
    session.commit()
    print("Транзакция успешно выполнена!")
except Exception as e:
    # Откатываем изменения в случае ошибки
    session.rollback()
    print(f"Ошибка: {e}")
    print("Изменения откачены!")

# Проверяем состояние после второй транзакции
show_all_users()

# Пример 3: Использование контекстного менеджера для транзакций
print("\n=== ПРИМЕР 3: ИСПОЛЬЗОВАНИЕ КОНТЕКСТНОГО МЕНЕДЖЕРА ===")
try:
    # Начинаем транзакцию с помощью контекстного менеджера
    with session.begin():
        user5 = User(username="user5", email="user5@example.com")
        user6 = User(username="user6", email="user6@example.com")
        
        session.add(user5)
        session.add(user6)
        
        # Имитируем ошибку
        print("Имитируем ошибку...")
        raise ValueError("Искусственная ошибка для демонстрации отката")
        
    # Этот код не выполнится, если будет ошибка
    print("Транзакция успешно выполнена!")
except Exception as e:
    print(f"Ошибка: {e}")
    print("Изменения автоматически откачены!")

# Проверяем финальное состояние
print("\n=== ФИНАЛЬНОЕ СОСТОЯНИЕ ===")
show_all_users()

print("\n=== ВЫВОДЫ ===")
print("1. Первая транзакция успешно добавила пользователей user1 и user2")
print("2. Вторая транзакция не выполнилась из-за ошибки дублирования username")
print("   Пользователи user3 и user4 не были добавлены (откат)")
print("3. Третья транзакция не выполнилась из-за искусственной ошибки")
print("   Пользователи user5 и user6 не были добавлены (автоматический откат)")
print("4. В базе данных остались только пользователи из успешной транзакции")