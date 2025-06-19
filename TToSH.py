import requests                 # - библиотека для выполнения HTTP-запросов к веб-страницам
from bs4 import BeautifulSoup   # - библиотека для парсинга HTML и извлечения данных из веб-страниц
import time                     # - библиотека Python для работы со временем



# Извлекает с заданной страницы все ссылки на другие статьи Википедии
def scrape_wiki_article_links(page_url, wiki_domain):
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article_links = set()
        for anchor_tag in soup.select('div.mw-parser-output a[href^="/wiki/"]'):
            relative_path = anchor_tag.get('href')
            if ":" not in relative_path:                    # Исключаем специальные страницы (например, "File:", "Help:")
                absolute_url = wiki_domain + relative_path
                article_links.add(absolute_url)
        return article_links
    
    except Exception as error:
        return set()



# Ищет путь между двумя статьями Wikipedia с использованием DFS
def find_path_between_wiki_pages(start_url, target_url, rate_limit):
    start_time = time.time()
    visited_urls  = set()                                   # Трекер посещенных страниц
    stack = [(start_url, [start_url])]                      # Стек с текущим URL и путем до него
    request_counter = 0                                     # Счетчик выполненных запросов
    search_time = 0

    while stack:
        # Получаем текущую страницу и путь до нее
        current_url, path = stack.pop()

        # Проверка достижения цели
        if current_url == target_url:
            search_time = time.time() - start_time
            return path, search_time

        # Проверка максимальной глубины
        if len(path) > 5:
            continue

        # Обработка непосещенных страниц
        if current_url not in visited_urls :
            visited_urls .add(current_url)

            # Получаем ссылки со страницы
            outgoing_links = scrape_wiki_article_links(
                current_url,
                "https://en.wikipedia.org"                  # wiki_domain
            )
            request_counter += 1

            # Учитываем rate-limit
            if request_counter >= rate_limit:
                time.sleep(1)                               # Защита от блокировки
                request_counter = 0

            # Добавляем новые ссылки в стек
            for link in outgoing_links:
                if link not in visited_urls :
                    stack.append((link, path + [link]))

    search_time = time.time() - start_time
    return None, search_time



# Анализирует связи между двумя статьями Wikipedia в обоих направлениях
def analyze_wikipedia_connections(url_1, url_2, rate_limit):

    print("\n=== Анализ связей между статьями ===")
    print(f"Статья A: {url_1}")
    print(f"Статья B: {url_2}\n")

    search_start = time.time()

    # Поиск первой цепи
    path_ab, duration_ab = find_path_between_wiki_pages(url_1, url_2, rate_limit)
    display_path_results(
            path=path_ab,
            duration=duration_ab,
            source="Статья A",
            target="Статья B",
            direction="A → B"
        )

    # Поиск второй цепи
    path_ba, duration_ba = find_path_between_wiki_pages(url_2, url_1, rate_limit)
    display_path_results(
        path=path_ba,
        duration=duration_ba,
        source="Статья B",
        target="Статья A",
        direction="B → A"
    )

    # Итоги
    total_duration = time.time() - search_start
    print(f"\n{' ИТОГИ '.center(50, '=')}")
    print(f"Общее время выполнения: {total_duration:.2f} секунд")
    print(f"Среднее время на поиск: {(duration_ab + duration_ba)/2:.2f} секунд")
    print("=" * 50)



# Выводит результаты поиска цепи в стандартизированном формате
def display_path_results(path, duration, source, target, direction):
    print(f"\nРезультаты поиска ({direction}):")
    
    if path:
        print(f"\nНайден путь из ({len(path)-1} переходов):")
        print("\n→ ".join(path))
        print(f"\nВремя поиска: {duration:.2f} сек")
    else:
        print(f"\nПуть между {source} и {target} не найден (максимальная глубина: 5)")
        print(f"Время поиска: {duration:.2f} сек")



if __name__ == "__main__":

    ARTICLE_1 = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
    ARTICLE_2 = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
    RATE_LIMIT = 10
    
    analyze_wikipedia_connections(
        url_1 = ARTICLE_1,
        url_2 = ARTICLE_2,
        rate_limit = RATE_LIMIT
    )