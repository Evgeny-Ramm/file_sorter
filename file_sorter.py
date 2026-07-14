#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# file_sorter.py
# Сортировка файлов по расширениям с цветным выводом и рекурсией.

import os
import shutil
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

EXTENSION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.odt', '.xlsx', '.pptx'],
    'Archives': ['.zip', '.tar', '.gz', '.7z', '.rar'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac'],
    'Video': ['.mp4', '.mkv', '.avi', '.mov'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.h', '.sh'],
}

def get_category(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return 'Others'

def move_file(file_path, dest_dir, dry_run=False):
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_dir, filename)

    if dry_run:
        print(f"{Fore.YELLOW}[DRY RUN] {file_path} -> {dest_path}{Style.RESET_ALL}")
        return

    os.makedirs(dest_dir, exist_ok=True)

    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_name = f"{base}_{counter}{ext}"
            new_path = os.path.join(dest_dir, new_name)
            if not os.path.exists(new_path):
                dest_path = new_path
                break
            counter += 1

    shutil.move(file_path, dest_path)
    print(f"{Fore.GREEN}Перемещён: {file_path} -> {dest_path}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="сортировка файлов")
    parser.add_argument("directory", help="папка для сортировки")
    parser.add_argument("-r", "--recursive", action="store_true", help="обход подпапок")
    parser.add_argument("--dry-run", action="store_true", help="сухой прогон")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Ошибка: папка не существует")
        return

    files = []
    if args.recursive:
        for root, _, filenames in os.walk(args.directory):
            for f in filenames:
                files.append(os.path.join(root, f))
    else:
        for entry in os.listdir(args.directory):
            full_path = os.path.join(args.directory, entry)
            if os.path.isfile(full_path):
                files.append(full_path)

    print(f"{Fore.CYAN}Найдено файлов: {len(files)}{Style.RESET_ALL}")

    stats = {}
    for f in files:
        cat = get_category(f)
        dest_dir = os.path.join(args.directory, cat)
        move_file(f, dest_dir, args.dry_run)
        stats[cat] = stats.get(cat, 0) + 1

    print(f"\n{Fore.CYAN}Статистика:{Style.RESET_ALL}")
    for cat, count in stats.items():
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    main()
