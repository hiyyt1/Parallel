import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
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
    'user_region_id': '4',
    '_ym_isad': '2',
    'domain_sid': 'SRZX6b2JaUuEhMEpE2lUr%3A1744153406978',
    '_gid': 'GA1.2.777417189.1744153409',
    'views_counter': '%7B%22folk_rating.response%22%3A%5B10433140%5D%7D',
    'PHPSESSID_NG_USER_RATING': 'vngki6fd508m0i98esmj5he2lt',
    'banki_prev_page': '/services/responses/bank/alfabank/',
    'BANKI_RU_MYBANKI_ID': 'ef770d6a-91cb-41a4-bd51-210888c9bcfb',
    '_banki_ru_mybanki_id_migration': '2024-08-14-updatedCookieDomain',
    '_ga_MEEKHDWY53': 'GS1.1.1744158454.7.1.1744162320.53.0.0',
    '_ga': 'GA1.2.65386599.1741549032',
    'tmr_detect': '0%7C1744162322548',
    'aff_sub3': '/services/responses/list/',
    '_ga_EFC0FSWXRL': 'GS1.1.1744165245.9.0.1744165245.0.0.0',
    '_dc_gtm_UA-38591118-1': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'BANKI_RU_USER_IDENTITY_UID=6176112222777918389; _flpt_sso_auth_user_in_segment=off; _flpt_news_todialog_inc020_page_core=news_todialog_inc020_page_core_a; _flpt_header_mobile_app_links=hide; _ym_uid=1741549031197909838; _ym_d=1741549031; tmr_lvid=dfddad8335f095533aae767b82969060; tmr_lvidTS=1741549031167; ym_client_id=1741549031197909838; _flpt_percent_zone=5; ga_client_id=65386599.1741549032; uxs_uid=e5e95dd0-fd1d-11ef-a334-3590fd8c01a3; _gcl_au=1.1.825610197.1741549033; user_region_id=4; _ym_isad=2; domain_sid=SRZX6b2JaUuEhMEpE2lUr%3A1744153406978; _gid=GA1.2.777417189.1744153409; views_counter=%7B%22folk_rating.response%22%3A%5B10433140%5D%7D; PHPSESSID_NG_USER_RATING=vngki6fd508m0i98esmj5he2lt; banki_prev_page=/services/responses/bank/alfabank/; BANKI_RU_MYBANKI_ID=ef770d6a-91cb-41a4-bd51-210888c9bcfb; _banki_ru_mybanki_id_migration=2024-08-14-updatedCookieDomain; _ga_MEEKHDWY53=GS1.1.1744158454.7.1.1744162320.53.0.0; _ga=GA1.2.65386599.1741549032; tmr_detect=0%7C1744162322548; aff_sub3=/services/responses/list/; _ga_EFC0FSWXRL=GS1.1.1744165245.9.0.1744165245.0.0.0; _dc_gtm_UA-38591118-1=1',
    'downlink': '0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.955", "YaBrowser";v="25.2.4.955", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36',
}


def extract_review_data(review_url):
    print(f"Получение данных со страницы: {review_url}")
    response = requests.get(review_url, headers=headers, cookies=cookies)
    
    if response.status_code != 200:
        print(f"Ошибка при получении отзыва: {response.status_code}")
        return None, None, None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Извлечение даты
    date_span = soup.find("span", class_="l10fac986")
    review_date = date_span.get_text(strip=True) if date_span else "Дата не найдена"
    
    
    review_div = soup.find("div", class_="lb1789875 markdown-inside markdown-inside--list-type_circle-fill")
    review_text = "\n".join([p.get_text(strip=True) for p in review_div.find_all("p")]) if review_div else "Отзыв не найден"
    
    return review_url, review_date, review_text

input_file = "Sber_review_links.txt"  
output_file = "Sber_reviews.xlsx"  
reviews_data = []  


with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Удаляем пустые строки и дубликаты
links = list(set([line.strip() for line in lines if line.strip().startswith("http")]))

print(f"Найдено {len(links)} уникальных ссылок.")

# Обработка каждой ссылки
for link in links:
    url, date, review = extract_review_data(link)
    reviews_data.append({"URL": url, "Date": date, "Review": review})
    #time.sleep(2) 

# Сохранение данных в Excel
if reviews_data:
    df = pd.DataFrame(reviews_data)
    df.to_excel(output_file, index=False)  # Сохраняем данные в Excel
    print(f"Все отзывы успешно сохранены в файл {output_file}.")
else:
    print("Нет данных для сохранения.")


