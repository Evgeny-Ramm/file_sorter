#!/usr/bin/env python3
# Ветка для ревью кода
import json
import os
import shutil
import argparse
import sys
import logging

def load_config(config_file='config.json'):
    """Загружает конфигурацию из JSON-файла. Если файл не найден, возвращает словарь по умолчанию."""
    default_config = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'Documents': ['.pdf', '.docx', '.doc', '.txt', '.odt', '.xlsx', '.pptx'],
        'Archives': ['.zip', '.tar', '.gz', '.7z', '.rar'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac'],
        'Video': ['.mp4', '.mkv', '.avi', '.mov'],
        'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.h', '.sh'],
        'Others': []
    }
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # Проверим, что загруженный конфиг — это словарь (можно добавить больше проверок)
        if isinstance(config, dict):
            return config
        else:
            print(f"Ошибка: файл {config_file} должен содержать словарь. Используется конфигурация по умолчанию.")
            return default_config
    except FileNotFoundError:
        # Если файла нет, создадим его с конфигом по умолчанию (опционально)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print(f"Создан файл конфигурации {config_file} с настройками по умолчанию.")
        return default_config
    except json.JSONDecodeError:
        print(f"Ошибка: файл {config_file} повреждён (некорректный JSON). Используется конфигурация по умолчанию.")
        return default_config


def get_files(directory, recursive=False):
    """Возвращает список полных путей всех файлов в директории.
    Если recursive=True, обходит подпапки рекурсивно."""
    files = []
    if recursive:
        # os.walk рекурсивно обходит все подпапки
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                files.append(full_path)
    else:
        # старый вариант: только текущая папка
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
    return files


def get_category(file_path, config, default='Others'):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for category, extensions in config.items():
        if ext in extensions:
            return category
    return default

def ensure_dir(directory):
    """Создаёт директорию, если она не существует."""
    os.makedirs(directory, exist_ok=True)

def move_file(file_path, dest_dir, dry_run=False):
    """Перемещает файл в целевую папку, обрабатывая конфликты имён."""
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_dir, filename)

    if dry_run:
        logging.info(f"[DRY RUN] {file_path} -> {dest_path}")
        return

    # Создаём папку назначения
    ensure_dir(dest_dir)

    # Если файл уже существует, генерируем уникальное имя
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_filename = f"{base}_{counter}{ext}"
            new_dest_path = os.path.join(dest_dir, new_filename)
            if not os.path.exists(new_dest_path):
                logging.info(f"Конфликт имён: {filename} уже существует, переименован в {new_filename}")
                dest_path = new_dest_path
                break
            counter += 1

    # Перемещаем файл
    shutil.move(file_path, dest_path)
    logging.info(f"Перемещён: {file_path} -> {dest_path}")

def main():
    parser = argparse.ArgumentParser(description="Сортировщик файлов по расширениям.")
    parser.add_argument("directory", help="Путь к директории для сортировки")
    parser.add_argument("--dry-run", action="store_true", help="Показать, что будет сделано, без реального перемещения")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Обрабатывать файлы рекурсивно (включая подпапки)")
    args = parser.parse_args()
    
     # Настройка логирования
    logging.basicConfig(
        filename='file_sorter.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
     )

    config = load_config()

    if not os.path.isdir(args.directory):
        logging.error(f"Директория {args.directory} не существует.")
        sys.exit(1)

    files = get_files(args.directory, recursive=args.recursive)
    logging.info(f"Найдено файлов: {len(files)} в директории {args.directory}")

    for f in files:
        cat = get_category(f, config, default='Others')
        dest_dir = os.path.join(args.directory, cat)
        move_file(f, dest_dir, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
