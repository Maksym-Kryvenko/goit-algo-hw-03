# Завдання 1

# Напишіть програму на Python, яка рекурсивно копіює файли у вихідній директорії, переміщає їх до нової директорії та сортує в піддиректорії, назви яких базуються на розширенні файлів.

# Також візьміть до уваги наступні умови:

# 1. Парсинг аргументів. Скрипт має приймати два аргументи командного рядка: шлях до вихідної директорії та шлях до директорії призначення (за замовчуванням, якщо тека призначення не була передана, вона повинна бути з назвою dist).

# 2. Рекурсивне читання директорій:

# Має бути написана функція, яка приймає шлях до директорії як аргумент.
# Функція має перебирати всі елементи у директорії.
# Якщо елемент є директорією, функція повинна викликати саму себе рекурсивно для цієї директорії.
# Якщо елемент є файлом, він має бути доступним для копіювання.

# 3. Копіювання файлів:

# Для кожного типу файлів має бути створений новий шлях у вихідній директорії, використовуючи розширення файлу для назви піддиректорії.
# Файл з відповідним типом має бути скопійований у відповідну піддиректорію.

# 4. Обробка винятків. Код має правильно обробляти винятки, наприклад, помилки доступу до файлів або директорій.

# 5. Після виконання програми всі файли у вихідній директорії рекурсивно скопійовано в нову директорію та розсортовано в піддиректорії за їх розширенням.

import os
import shutil
import sys
from pathlib import Path


def copy_files_recursively(source_dir, dest_dir):
    """
    Рекурсивно копіює файли з вихідної директорії до директорії призначення,
    сортуючи їх у піддиректорії за розширенням файлів.
    
    Args:
        source_dir: Шлях до вихідної директорії
        dest_dir: Шлях до директорії призначення
    """
    try:
        # Перевіряємо, чи існує вихідна директорія
        if not os.path.exists(source_dir):
            print(f"Помилка: Вихідна директорія '{source_dir}' не існує.")
            return
        
        if not os.path.isdir(source_dir):
            print(f"Помилка: '{source_dir}' не є директорією.")
            return
        
        # Перебираємо всі елементи у вихідній директорії
        for item in os.listdir(source_dir):
            item_path = os.path.join(source_dir, item)
            
            try:
                # Якщо це директорія, викликаємо функцію рекурсивно
                if os.path.isdir(item_path):
                    copy_files_recursively(item_path, dest_dir)
                
                # Якщо це файл, копіюємо його
                elif os.path.isfile(item_path):
                    # Отримуємо розширення файлу
                    file_extension = Path(item_path).suffix[1:]
                    if not file_extension:
                        file_extension = "no_extension"
                    
                    # Створюємо шлях до піддиректорії з назвою розширення
                    target_subdir = os.path.join(dest_dir, file_extension)
                    
                    # Створюємо піддиректорію, якщо її не існує
                    os.makedirs(target_subdir, exist_ok=True)
                    
                    # Формуємо шлях до файлу призначення
                    target_file_path = os.path.join(target_subdir, item)
                    
                    # Копіюємо файл
                    shutil.copy2(item_path, target_file_path)
                    print(f"Скопійовано: {item_path} -> {target_file_path}")
            
            except PermissionError:
                print(f"Помилка доступу: Немає прав для '{item_path}'")
            except Exception as e:
                print(f"Помилка при обробці '{item_path}': {e}")
    
    except PermissionError:
        print(f"Помилка доступу: Немає прав для читання директорії '{source_dir}'")
    except Exception as e:
        print(f"Помилка при обробці директорії '{source_dir}': {e}")


if __name__ == "__main__":
    # Парсинг аргументів командного рядка
    if len(sys.argv) < 2:
        print("Використання: python task1.py <вихідна_директорія> [директорія_призначення]")
        print("Якщо директорія призначення не вказана, буде використано 'dist'")
        sys.exit(1)
    
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2] if len(sys.argv) > 2 else "dist"
    
    print(f"Копіювання файлів з '{source_directory}' до '{destination_directory}'...")
    copy_files_recursively(source_directory, destination_directory)
    print("Завершено!")