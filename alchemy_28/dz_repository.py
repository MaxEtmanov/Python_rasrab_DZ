from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from typing import List, Optional
from contextlib import contextmanager
import copy

# Создаем базу данных
engine = create_engine('sqlite:///repository_demo.db', echo=False)
Base = declarative_base()

# Определяем модели
class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    
    author = relationship("Author", back_populates="books")
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author_id={self.author_id})"

# Создаем таблицы
Base.metadata.create_all(engine)

# Фабрика сессий
class SessionFactory:
    def __init__(self, engine):
        self.engine = engine
        self._session_maker = sessionmaker(bind=engine)
    
    @contextmanager
    def create_session(self):
        """Создает сессию и управляет ее жизненным циклом"""
        session = self._session_maker()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Класс для хранения данных автора
class AuthorDTO:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

# Класс для хранения данных книги
class BookDTO:
    def __init__(self, id, title, author_id):
        self.id = id
        self.title = title
        self.author_id = author_id
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author_id={self.author_id})"

# Репозиторий для работы с книгами
class BookRepository:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory
    
    def add_book(self, title: str, author_id: int) -> BookDTO:
        """Добавляет новую книгу"""
        with self.session_factory.create_session() as session:
            book = Book(title=title, author_id=author_id)
            session.add(book)
            session.flush()  # Чтобы получить ID книги
            # Создаем DTO объект с данными из книги
            return BookDTO(book.id, book.title, book.author_id)
    
    def get_books_by_author_id(self, author_id: int) -> List[BookDTO]:
        """Получает все книги автора по его ID"""
        with self.session_factory.create_session() as session:
            books = session.query(Book).filter(Book.author_id == author_id).all()
            # Преобразуем объекты Book в BookDTO
            return [BookDTO(book.id, book.title, book.author_id) for book in books]
    
    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по её ID"""
        with self.session_factory.create_session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if book:
                session.delete(book)
                return True
            return False
    
    def get_book_by_id(self, book_id: int) -> Optional[BookDTO]:
        """Получает книгу по её ID"""
        with self.session_factory.create_session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if book:
                return BookDTO(book.id, book.title, book.author_id)
            return None

# Репозиторий для работы с авторами
class AuthorRepository:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory
    
    def add_author(self, name: str) -> AuthorDTO:
        """Добавляет нового автора"""
        with self.session_factory.create_session() as session:
            author = Author(name=name)
            session.add(author)
            session.flush()  # Чтобы получить ID автора
            # Создаем DTO объект с данными из автора
            return AuthorDTO(author.id, author.name)
    
    def get_author_by_id(self, author_id: int) -> Optional[AuthorDTO]:
        """Получает автора по его ID"""
        with self.session_factory.create_session() as session:
            author = session.query(Author).filter(Author.id == author_id).first()
            if author:
                return AuthorDTO(author.id, author.name)
            return None

# Тестовые сценарии
def run_tests():
    # Создаем фабрику сессий
    session_factory = SessionFactory(engine)
    
    # Создаем репозитории
    book_repo = BookRepository(session_factory)
    author_repo = AuthorRepository(session_factory)
    
    print("\n=== ТЕСТИРОВАНИЕ ПАТТЕРНА REPOSITORY ===")
    
    # Тест 1: Добавление автора и книг
    print("\nТест 1: Добавление автора и книг")
    author = author_repo.add_author("Александр Пушкин")
    print(f"Добавлен автор: {author}")
    
    book1 = book_repo.add_book("Евгений Онегин", author.id)
    book2 = book_repo.add_book("Капитанская дочка", author.id)
    print(f"Добавлены книги: {book1}, {book2}")
    
    # Тест 2: Получение книг автора
    print("\nТест 2: Получение книг автора")
    books = book_repo.get_books_by_author_id(author.id)
    print(f"Книги автора {author.name}:")
    for book in books:
        print(f"- {book.title}")
    
    # Тест 3: Удаление книги
    print("\nТест 3: Удаление книги")
    book_id_to_delete = book1.id
    print(f"Удаляем книгу с ID {book_id_to_delete}")
    success = book_repo.delete_book(book_id_to_delete)
    print(f"Книга удалена: {success}")
    
    # Проверяем, что книга удалена
    deleted_book = book_repo.get_book_by_id(book_id_to_delete)
    print(f"Книга с ID {book_id_to_delete} существует: {deleted_book is not None}")
    
    # Проверяем оставшиеся книги автора
    remaining_books = book_repo.get_books_by_author_id(author.id)
    print(f"Оставшиеся книги автора {author.name}:")
    for book in remaining_books:
        print(f"- {book.title}")
    
    # Тест 4: Добавление еще одного автора и книги
    print("\nТест 4: Добавление еще одного автора и книги")
    author2 = author_repo.add_author("Лев Толстой")
    print(f"Добавлен автор: {author2}")
    
    book3 = book_repo.add_book("Война и мир", author2.id)
    print(f"Добавлена книга: {book3}")
    
    # Проверяем книги обоих авторов
    print("\nКниги по авторам:")
    for author_id in [author.id, author2.id]:
        current_author = author_repo.get_author_by_id(author_id)
        books = book_repo.get_books_by_author_id(author_id)
        print(f"Автор {current_author.name}:")
        for book in books:
            print(f"- {book.title}")

if __name__ == "__main__":
    run_tests()
