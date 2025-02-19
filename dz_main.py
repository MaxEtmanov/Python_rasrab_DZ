# 1 Создание и управление директориями 

import os
from datetime import datetime
import json 
import chardet
import re
import zipfile
from jsonschema import validate, ValidationError

def create_project_structure():
    # Определяем структуру директорий
    directories = [
        'data/raw',
        'data/processed',
        'logs',
        'backups',
        'output'
    ]
    
    # Создаем корневую директорию проекта
    root_dir = 'project_root'
    
    # Создаем каждую директорию
    for dir_path in directories:
        full_path = os.path.join(root_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
    
    print("Структура проекта успешно создана!")

if __name__ == "__main__":
    create_project_structure()

## Создание текстовых файлов

text_ru= """ Буря мглою небо кроет,
Вихри снежные крутя;
То, как зверь, она завоет,
То заплачет, как дитя,
То по кровле обветшалой
Вдруг соломой зашумит,
То, как путник запоздалый,
К нам в окошко застучит.
Наша ветхая лачужка
И печальна и темна.
Что же ты, моя старушка,
Приумолкла у окна?
Или бури завываньем
Ты, мой друг, утомлена,
Или дремлешь под жужжаньем
Своего веретена?
Выпьем, добрая подружка
Бедной юности моей,
Выпьем с горя; где же кружка?
Сердцу будет веселей.
Спой мне песню, как синица
Тихо за морем жила;
Спой мне песню, как девица
За водой поутру шла.
Буря мглою небо кроет,
Вихри снежные крутя;
То, как зверь, она завоет,
То заплачет, как дитя.
Выпьем, добрая подружка
Бедной юности моей,
Выпьем с горя: где же кружка?
Сердцу будет веселей."""

with open ('project_root/data/raw/text_ru.txt', 'w', encoding= 'UTF-8') as file:
    file.write(text_ru)

text_en = """ The storm covers the sky with fog,
Snow whirlwinds spinning;
She will howl like a beast,
He wll cry like a child,
It is on the dilapidated roof
Suddenly the straw will make a noise,
That, like a late traveller,
Your ie knocking on our window.
Our dilapidated slut
Both sad and dark.
What are you, my old lady,
Shut up by the window?
Or storms with a howl
You, my friend, are tired,
Or dozing under the buzz
Your spindle?
Let is have a drink, good friend
My poor youth,
Let is drink from grief; where is the mug?
It will be more cheerful for the heart.
Sing me a song like a tit
She lived quietly beyond the sea;
Sing me a song like a girl
I went for water in the morning.
The storm covers the sky with fog,
Snow whirlwinds spinning;
She will howl like a beast,
He will cry like a child.
Let is have a drink, good friend
My poor youth,
Let is drink from grief: where is the mug?
It will be more cheerful for the heart "é" """

with open ('project_root/data/raw/text_en.txt', 'w', encoding='ISO-8859-1') as file:
    file.write(text_en)

directories = [
        'data/raw',
        'data/processed',
        'logs',
        'backups',
        'output'
]
## Получаем информацию о созданных директориях и файлах
created_dirs = [os.path.join('project_root', d) for d in directories]
created_files = [
    'project_root/data/raw/text_ru.txt',
    'project_root/data/raw/text_en.txt'
]

## Записываем в лог информацию о выполненных операциях
with open('project_root/logs/operations.log', 'w', encoding='UTF-8') as log:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Логируем создание директорий
    log.write(f"{current_time} - Созданы следующие директории:\n")
    for dir_path in created_dirs:
        log.write(f"{current_time} - {dir_path}\n")
    
    # Логируем создание файлов
    log.write(f"{current_time} - Созданы и заполнены следующие файлы:\n")
    for file_path in created_files:
        file_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"{file_time} - {file_path}\n")

## Создание и запись в лог
def log_operation(operation_name, message):
    log_path = 'D:/Projects/Python_rasrab/DZ_12M/project_root/logs/operations.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, 'a', encoding='UTF-8') as log:
        log.write(f"{timestamp} {operation_name}: {message}\n")
        
    
# 2 Чтение, преобразование и сериализация данных
def read_raw():
    path = 'D:/Projects/Python_rasrab/DZ_12M/project_root/data/raw'
    processed_path = 'D:/Projects/Python_rasrab/DZ_12M/project_root/data/processed'
    
    #Полуаем список файлов в директории
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        
        # Определяем кодировку
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            print(f"\nКодировка файла {file}: {encoding}")
            
        try:
            # Читаем файл с определенной кодировкой
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"\nСодержимое файла {file}:\n")
                print(content)
                # Меняем регистр букв
                processed_content = content.swapcase()
                
                # Создаем новое имя файла
                processed_file = file.replace('.txt', '_processed.txt')
                processed_file_path = os.path.join(processed_path, processed_file)
                
                # Сохраняем обработанный текст
                with open(processed_file_path, 'w', encoding=encoding) as pf:
                    pf.write(processed_content)
                    
                print(f"Файл {file} обработан и сохранен как {processed_file}")
                
        except UnicodeDecodeError:
            print(f"Не удалось прочитать файл {file} с кодировкой {encoding}")
    log_operation("read_raw", f"Обработан файл {file}")
if __name__ == "__main__":
    read_raw()
    
## Сериализация данных
def serialize():
    # Пути к директориям
    processed_path = 'project_root/data/processed'
    raw_path = 'project_root/data/raw'
    output_path = 'project_root/output/processed_data.json'
    
    result_data = []
    
    # Получаем список обработанных файлов
    processed_files = [f for f in os.listdir(processed_path) if os.path.isfile(os.path.join(processed_path, f))]
    
    for proc_file in processed_files:
        # Получаем имя исходного файла
        original_file = proc_file.replace('_processed.txt', '.txt')
        
        # Определяем кодировку исходного файла
        with open(os.path.join(raw_path, original_file), 'rb') as f:
            raw_encoding = chardet.detect(f.read())['encoding']
            
        # Определяем кодировку обработанного файла    
        with open(os.path.join(processed_path, proc_file), 'rb') as f:
            proc_encoding = chardet.detect(f.read())['encoding']
            
        # Читаем файлы с определенными кодировками
        with open(os.path.join(raw_path, original_file), 'r', encoding=raw_encoding) as f:
            original_text = f.read()
            
        with open(os.path.join(processed_path, proc_file), 'r', encoding=proc_encoding) as f:
            processed_text = f.read()
        
        file_path = os.path.join(processed_path, proc_file)
        file_stats = os.stat(file_path)
        
        data = {
            'filename': proc_file,
            'original_text': original_text,
            'processed_text': processed_text,
            'size_bytes': file_stats.st_size,
            'last_modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        result_data.append(data)
    
    # Сохраняем данные в JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"Данные успешно сериализованы в {output_path}")

log_operation("serialize", "Данные успешно сериализованы")
if __name__ == "__main__":
    serialize()
    
# 3. Создание резервной копии
def backup():
    # Получаем текущую дату для имени файла
    now_date = datetime.now().strftime('%Y%m%d')
    backup_file = f'backup_{now_date}.zip'
    # Определяем пути 
    data_path = 'project_root/data' 
    backup_path = os.path.join('project_root/backups', backup_file)
    
    # Создаем архив
    with zipfile.ZipFile(backup_path, 'w') as f:
        # Проходим по всем файлам из директории data
        for root, dirs, files in os.walk(data_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Добавляем файл в архив с относительным путём
                arcname = os.path.relpath(file_path, 'project_root')
                f.write(file_path, arcname)
    print(f"Архив успешно создан: {backup_path}")
    
log_operation("backup", "Архив успешно создан")
if __name__ == "__main__":
    backup()

#Восстановление данных
def in_backup():
    # Пути к директориям
    current_date = datetime.now().strftime('%Y%m%d')
    backup_file = f'backup_{current_date}.zip'
    backup_path = os.path.join('project_root/backups', backup_file)
    in_backup_path = 'project_root'
    
    # Проверяем наличие архива
    if not os.path.exists(backup_path):
        print(f"Файл архива не найден: {backup_path}")
        return
    # Распаковываем архив
    with zipfile.ZipFile(backup_path, 'r') as f:
        # Проверяем целостность архива
        if f.testzip() is None:
            print(f"Начинаем восстановление из архива")
            f.extractall(in_backup_path)
            print(f"Данные успешно восстановлены в директорию: {in_backup_path}")
        else:
            print("Архив поврежден!")    
        
log_operation("in_backup", "Данные успешно восстановлены")
if __name__ == "__main__":
    in_backup()
    
# 4. Дополнительные задачи с сериализацией и JSON Schema
##Работа с пользовательскими классами и JSON
class FileInfo:
    def __init__(self, file_path):
        """Инициализация объекта FileInfo"""
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self._update_file_info()
    
    def _update_file_info(self):
        """Обновление информации о файле"""
        stats = os.stat(self.file_path)
        self.size = stats.st_size
        self.created = datetime.fromtimestamp(stats.st_ctime)
        self.modified = datetime.fromtimestamp(stats.st_mtime)
    
    def get_size_formatted(self):
        """Получение размера файла в читаемом формате"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.size < 1024:
                return f"{self.size:.2f} {unit}"
            self.size /= 1024
    
    def __str__(self):
        """Строковое представление информации о файле"""
        return (f"Файл: {self.file_name}\n"
                f"Путь: {self.file_path}\n"
                f"Размер: {self.get_size_formatted()}\n"
                f"Создан: {self.created.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Изменён: {self.modified.strftime('%Y-%m-%d %H:%M:%S')}")
        
### Сериализация в JSON
def serialize():
    path = 'project_root/data/processed'
    output_file = 'project_root/output/processed_files_info.json'
    data = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            file_info = FileInfo(file_path)
            data.append({
                'file_name': file_info.file_name,
                'file_path': file_info.file_path,
                'size': file_info.get_size_formatted(),
                'created': file_info.created.strftime('%Y-%m-%d %H:%M:%S'),
                'modified': file_info.modified.strftime('%Y-%m-%d %H:%M:%S')
            })
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii= False,  indent=4)

    print(f"Данные успешно сериализованы в {output_file}")
    with open('D:/Projects/Python_rasrab/DZ_12M/project_root/output/processed_files_info.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'Данные десериализованы: {data}')
    
log_operation("serialize", "Данные успешно сериализованы в JSON")
if __name__ == "__main__":
    serialize()
    
### JSON Schema
# Определяем схему для нашего JSON с информацией о файлах
schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_path": {"type": "string"},
            "size": {"type": "string", "pattern": "^[0-9]+\.[0-9]+ [KMGT]?B$"},
            "created": {
                "type": "string",
                "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
            },
            "modified": {
                "type": "string",
                "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
            }
        },
        "required": ["file_name", "file_path", "size", "created", "modified"]
    }
}

def validate_json_schema():
    # Читаем JSON файл
    json_path = 'project_root/output/processed_files_info.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        doc=json.load(f)
    
    try:
        validate(instance=doc, schema=schema)
        print("Структура JSON файла соответствует схеме")
                
    except ValidationError as e:
        print(f"Ошибка валидации JSON:")
        print(f"Сообщение: {e.message}")
        
log_operation("validate_json_schema", "Структура JSON файла соответствует схеме")
if __name__ == "__main__":
    validate_json_schema()

# 5. Отчет о проделанной работе

def create_work_report():
    log_file = 'D:/Projects/Python_rasrab/DZ_12M/project_root/logs/operations.log'
    report_file = 'D:/Projects/Python_rasrab/DZ_12M/work_report.json'
    
    work_report = {
        "дата_отчета": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "выполненные_работы": []
    }
    
    with open(log_file, 'r', encoding='UTF-8') as f:
        log_entries = f.readlines()
        
    for entry in log_entries:
        if entry.strip():
            # Парсим строку лога
            timestamp = entry[1:20]  # Извлекаем дату и время
            message = entry[22:].strip()  # Извлекаем сообщение
            
            work_item = {
                "время_выполнения": timestamp,
                "описание_операции": message
            }
            work_report["выполненные_работы"].append(work_item)
    
    # Сохраняем отчет в JSON
    with open(report_file, 'w', encoding='UTF-8') as f:
        json.dump(work_report, f, ensure_ascii=False, indent=2)
    
    print(f"Отчет успешно создан: {report_file}")

if __name__ == "__main__":
    create_work_report()

