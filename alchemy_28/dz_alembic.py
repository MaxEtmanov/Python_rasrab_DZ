from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Создаем базу данных
engine = create_engine('sqlite:///alembic_demo.db')
Base = declarative_base()

# Определяем модель Order
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float)  # Добавлено новое поле
    # created_at удалено
    
    def __repr__(self):
        return f"Order(id={self.id}, product_name='{self.product_name}', quantity={self.quantity}, price={self.price})"

# Создаем таблицы (это нужно только для начальной настройки)
# Base.metadata.create_all(engine)

print("Модель Order определена. Теперь нужно настроить и применить миграции Alembic.")
