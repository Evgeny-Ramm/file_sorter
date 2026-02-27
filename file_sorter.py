#!/usr/bin/env python3
# Ветка для ревью кода
import os
import shutil
import argparse
import sys
import logging

# Словарь категорий и соответствующих расширений
EXTENSION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.odt', '.xlsx', '.pptx'],
    'Archives': ['.zip', '.tar', '.gz', '.7z', '.rar'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac'],
    'Video': ['.mp4', '.mkv', '.avi', '.mov'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.h', '.sh'],
    'Others': []  # для всего остального
}

def get_files(directory):
    """Возвращает список полных путей всех файлов в директории (без подпапок)."""
    files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            files.append(full_path)
    return files

def get_category(file_path):
    """Определяет категорию файла по его расширению."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return 'Others'

def ensure_dir(directory):
    """Создаёт директорию, если она не существует."""
    os.makedirs(directory, exist_ok=True)

def move_file(file_path, dest_dir, dry_run=False):
    """Перемещает файл в целевую папку, обрабатывая конфликты имён."""
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_dir, filename)

    if dry_run:
        print(f"[DRY RUN] {file_path} -> {dest_path}")
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
                dest_path = new_dest_path
                break
            counter += 1

    # Перемещаем файл
    shutil.move(file_path, dest_path)
    print(f"Перемещён: {file_path} -> {dest_path}")

def main():
    parser = argparse.ArgumentParser(description="Сортировщик файлов по расширениям.")
    parser.add_argument("directory", help="Путь к директории для сортировки")
    parser.add_argument("--dry-run", action="store_true", help="Показать, что будет сделано, без реального перемещения")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Ошибка: {args.directory} не является директорией или не существует.")
        sys.exit(1)

    files = get_files(args.directory)
    print(f"Найдено файлов: {len(files)}")

    for f in files:
        cat = get_category(f)
        dest_dir = os.path.join(args.directory, cat)
        move_file(f, dest_dir, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
