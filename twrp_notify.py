from bs4 import BeautifulSoup
import requests
import json
from telegram_send import send as tg_send
import asyncio

def parse_html(url):
    """
    Парсит HTML-страницу и извлекает текст из тегов <a>.

    Args:
        url (str): URL страницы для парсинга.

    Returns:
        list: Список извлеченного текста.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP

        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('strong')
        text_list = [tag.text for tag in a_tags]
        return text_list

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []



def to_file(data):
    """
    Записывает данные в файл в формате JSON.

    Args:
        data (list): Список данных для записи.
    """
    try:
        with open('models.txt', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4) # indent для форматирования
        return "Файл models.txt успешно записан!"
    except Exception as e:
        return f"Ошибка при записи в файл: {e}"


def read_from_file(filename):
    """
    Читает данные из файла JSON и возвращает список.

    Args:
        filename (str): Имя файла для чтения.

    Returns:
        list: Список данных, прочитанных из файла.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            local_data = json.load(f)
        return local_data
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {filename}.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return []


def find_new_items(local_list, remote_list):
    """
    Находит элементы, которые есть в remote_list, но отсутствуют в local_list.

    Args:
        local_list (list): Локальный список.
        remote_list (list): Удаленный список.

    Returns:
        list: Список новых элементов.
    """
    new_items = [item for item in remote_list if item not in local_list]
    return new_items

url = 'https://twrp.me/Devices/Realme/' # Замените на URL вашей страницы


async def main(): # Делаем функцию, которая вызывает tg_send, асинхронной
    remote_list = parse_html(url)
    local_list = read_from_file('models.txt')
    # print(local_list)
    new_models = find_new_items(local_list, remote_list)
    if new_models:
        await tg_send(str(new_models)) # Добавляем await и преобразуем список в строку

if __name__ == '__main__':
    asyncio.run(main()) # Запускаем асинхронную функцию main()

