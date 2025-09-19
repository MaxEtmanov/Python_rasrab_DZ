from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload

# Создаем базу данных 
engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()

# Определяем модели
class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # Определяем отношение один-ко-многим
    books = relationship("Book", back_populates="author")
    
    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    
    # Определяем обратное отношение
    author = relationship("Author", back_populates="books")
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}')"

# Создаем таблицы
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
author1 = Author(name="Лев Толстой")
author2 = Author(name="Федор Достоевский")

book1 = Book(title="Война и мир", author=author1)
book2 = Book(title="Анна Каренина", author=author1)
book3 = Book(title="Преступление и наказание", author=author2)
book4 = Book(title="Идиот", author=author2)

session.add_all([author1, author2, book1, book2, book3, book4])
session.commit()

print("\n" + "="*50)
print("ЛЕНИВАЯ ЗАГРУЗКА (LAZY LOADING)")
print("="*50)

# Отключаем вывод SQL запросов для чистоты вывода
engine.echo = False

# 1. Ленивая загрузка (Lazy Loading)
print("Получаем всех авторов:")
authors = session.query(Author).all()

print("\nВыводим авторов и их книги (ленивая загрузка):")
for author in authors:
    print(f"Автор: {author.name}")
    # При обращении к books будет выполнен дополнительный запрос
    print(f"Книги: {[book.title for book in author.books]}")
    print()

print("\n" + "="*50)
print("ЖАДНАЯ ЗАГРУЗКА (EAGER LOADING)")
print("="*50)

# 2. Жадная загрузка (Eager Loading)
print("Получаем всех авторов с их книгами одним запросом:")
authors_eager = session.query(Author).options(joinedload(Author.books)).all()

print("\nВыводим авторов и их книги (жадная загрузка):")
for author in authors_eager:
    print(f"Автор: {author.name}")
    # Книги уже загружены, дополнительных запросов не будет
    print(f"Книги: {[book.title for book in author.books]}")
    print()

print("\n" + "="*50)
print("СРАВНЕНИЕ")
print("="*50)
print("При ленивой загрузке:")
print("1. Сначала выполняется запрос для получения всех авторов")
print("2. Затем для каждого автора выполняется отдельный запрос для получения его книг")
print("Итого: 1 + N запросов, где N - количество авторов (в нашем случае 3 запроса)")
print("\nПри жадной загрузке:")
print("1. Выполняется один запрос с JOIN для получения авторов вместе с их книгами")
print("Итого: 1 запрос")
print("\nРазница: жадная загрузка эффективнее при работе с большим количеством данных,")
print("так как избегает проблемы N+1 запросов, характерной для ленивой загрузки.")