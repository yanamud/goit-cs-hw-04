import threading
import os
import logging
import time
from colorama import init, Fore, Style

start_time = time.time()

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(keyword, file, result_dict):
    logging.info(f"Початок пошуку у файлі {file}")
    start_time = time.time()

    try:
        # Читання текстового файлу
        with open(file, 'r') as f:
            lines = f.readlines()
            found_lines = [line.strip() for line in lines if keyword in line]
            if found_lines:
                logging.info(Fore.GREEN + f"Знайдено в файлі {file}:" + Style.RESET_ALL)
                result_dict[keyword].append(file)
        end_time = time.time()
        logging.info(f"Завершення пошуку у файлі {file}")
        logging.info(f"Час виконання для файлу {file}: {end_time - start_time:.4f} сек")

    except FileNotFoundError:
        print("Файл не знайдено!")
    except IOError as e:
        print("Помилка вводу-виводу:", e)
    except Exception as e:
        print("Сталася невідома помилка:", e)

# Функція для обробки файлів у потоці
def process_files(files, keyword, result_dict):
    for file in files:
        search_keywords_in_file(keyword, file, result_dict)

# Головна функція
def main():
    # Шлях до папки з файлами
    folder_path = "files_txt"
    # Ключове слово, яке потрібно знайти
    keyword = " child"
    # Кількість потоків для обробки файлів
    num_threads = 3
    
    # Отримати список файлів у папці
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    # Створити словник для зберігання результатів пошуку
    result_dict = {keyword: []}
    
    # Розділити список файлів між потоками
    files_per_thread = [files[i:i + num_threads] for i in range(0, len(files), num_threads)]
    
    # Запустити потоки для обробки файлів
    threads = []
    for files_subset in files_per_thread:
        thread = threading.Thread(target=process_files, args=(files_subset, keyword, result_dict))
        thread.start()
        threads.append(thread)
    
    # Зачекати, поки всі потоки завершаться
    for thread in threads:
        thread.join()
    
    # Повернути словник з результатами
    return result_dict

if __name__ == "__main__":
    result = main()
    print(Fore.GREEN + "Результати пошуку:" + Style.RESET_ALL, result)

    end_time = time.time()
    execution_time = end_time - start_time
    print(Fore.BLUE + f"Загальний час виконання: {execution_time} секунд" + Style.RESET_ALL)   