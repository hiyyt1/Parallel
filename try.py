import requests
from bs4 import BeautifulSoup
import time

# Базовый URL (без номера страницы)
base_url = "https://www.banki.ru/services/responses/bank/tcs/product/mobile_app/?page={}&is_countable=on"

headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.banki.ru/',
}

# Добавляем куки
cookies = {
    'BANKI_RU_USER_IDENTITY_UID': '6176112222777918389',
    '_flpt_sso_auth_user_in_segment': 'off',
    '_flpt_news_todialog_inc020_page_core': 'news_todialog_inc020_page_core_a',
    '_flpt_header_mobile_app_links': 'hide',
    '_ym_uid': '1741549031197909838',
    '_ym_d': '1741549031',
    'tmr_lvid': 'dfddad8335f095533aae767b82969060',
    'tmr_lvidTS': '1741549031167',
    'ym_client_id': '1741549031197909838',
    '_flpt_percent_zone': '5',
    'ga_client_id': '65386599.1741549032',
    'uxs_uid': 'e5e95dd0-fd1d-11ef-a334-3590fd8c01a3',
    '_gcl_au': '1.1.825610197.1741549033',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'domain_sid': 'SRZX6b2JaUuEhMEpE2lUr%3A1744034781785',
    'gtm-session-start': '1744034780378',
    '_gid': 'GA1.2.1162776477.1744034785',
    'cid_time_cookie': '65386599.1741549032 | 7.04.2025 | 17:06:43 | +03:00',
    'banki_prev_page': '/services/responses/bank/tcs/product/mobile_app/',
    'counter_session': '13',
    'BANKI_RU_MYBANKI_ID': 'ef770d6a-91cb-41a4-bd51-210888c9bcfb',
    '_banki_ru_mybanki_id_migration': '2024-08-14-updatedCookieDomain',
    '_ga_MEEKHDWY53': 'GS1.1.1744034783.3.1.1744036141.18.0.0',
    '_ga': 'GA1.2.65386599.1741549032',
    '_ga_EFC0FSWXRL': 'GS1.1.1744034783.3.1.1744036143.0.0.0',
    'tmr_detect': '0%7C1744036144207',
    'aff_sub3': '/services/responses/bank/tcs/product/mobile_app/',
}


# Функция для получения HTML-кода страницы
def get_page_html(page_number):
    url = base_url.format(page_number)  # Формируем полный URL с номером страницы
    response = requests.get(url, headers=headers, cookies=cookies)
    
    # Проверяем статус ответа
    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка при получении страницы {page_number}: {response.status_code}")
        return None

# Функция для извлечения уникальных ссылок из HTML-кода
def extract_unique_links_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Используем set для хранения уникальных ссылок
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/services/responses/bank/response/" in href:
            # Убираем фрагменты вроде #comments
            clean_href = href.split("#")[0]
            full_url = f"https://www.banki.ru{clean_href}"  # Делаем ссылку полной
            links.add(full_url)  # Добавляем в set для автоматического удаления дубликатов
    
    return list(links)  # Преобразуем set обратно в список

# Основной код для обработки страниц и записи ссылок в файл
output_file = "Tbank_review_links.txt"  # Новый файл для записи уникальных ссылок

with open(output_file, "w", encoding="utf-8") as output:
    for page in range(1, 701):  # Обрабатываем страницы с 1 по 5
        print(f"Получение данных со страницы {page}...")
        html_content = get_page_html(page)
        
        if html_content:
            links = extract_unique_links_from_html(html_content)
            if links:
                output.write(f"page_{page}\n")  # Записываем номер страницы
                for link in links:
                    output.write(f"{link}\n")  # Записываем каждую уникальную ссылку
                output.write("\n")  # Разделитель между страницами
            else:
                print(f"Не удалось найти ссылки на странице {page}.")
        else:
            print(f"Не удалось получить данные со страницы {page}.")
        
        # Добавляем задержку между запросами
        time.sleep(1)

print(f"Все уникальные ссылки успешно сохранены в файл {output_file}.")
