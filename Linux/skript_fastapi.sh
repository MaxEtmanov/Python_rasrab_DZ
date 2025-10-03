#!/bin/bash

# --- Проверка Python 3 ---
if ! command -v python3 > /dev/null
then
    echo "Python 3 не найден. Пожалуйста, установите его."
    exit 1
fi
echo "Python 3 найден."

# --- Проверка pip ---
if ! command -v pip > /dev/null
then
    echo "pip не найден. Пожалуйста, установите его."
    exit 1
fi
echo "pip найден."

# --- Создание директории проекта ---
if [ -d "fastapi_project" ]; then
    echo "Директория fastapi_project уже существует."
    echo "Удаляем все файлы внутри..."
    rm -rf fastapi_project/*
else
    echo "Создаём директорию fastapi_project..."
    mkdir fastapi_project
fi

cd fastapi_project
echo "Перешли в директорию fastapi_project"

# --- Создание виртуального окружения ---
echo "Создаём виртуальное окружение..."
python3 -m venv venv
echo "Виртуальное окружение создано."

# --- Активация виртуального окружения ---
echo "Активируем виртуальное окружение..."
source venv/bin/activate
echo "Виртуальное окружение активировано."

# --- Создание requirements.txt ---
echo "Создаём файл requirements.txt..."
echo "fastapi" > requirements.txt
echo "uvicorn" >> requirements.txt
echo "pydantic" >> requirements.txt
echo "Файл requirements.txt создан."

# --- Установка зависимостей ---
echo "Устанавливаем зависимости..."
pip install -r requirements.txt
echo "Зависимости установлены."

# --- Создание директорий для проекта ---
echo "Создаём папки static и logs..."
mkdir static
mkdir logs
echo "Папки созданы."

# --- Создание main.py ---
echo "Создаём файл main.py..."
echo "from fastapi import FastAPI" > main.py
echo "" >> main.py
echo "app = FastAPI()" >> main.py
echo "" >> main.py
echo "@app.get('/')" >> main.py
echo "def read_root():" >> main.py
echo "    return {'message': 'Hello, FastAPI!'}" >> main.py
echo "Файл main.py создан."

# --- Запуск FastAPI ---
echo "Запускаем сервер FastAPI..."
uvicorn main:app --reload
