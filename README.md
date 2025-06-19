# TToSH.py - The Theory of Six Handshakes (для Wikipedia)

## 📖 О скрипте
*Скрипт разработан в рамках учебного задания по дисциплине **"Разработка ПО и скриптовые языки"**.*

TToSH.py проверяет теорию "шести рукопожатий" для статей Wikipedia. Он находит путь между двумя произвольными статьями через цепочку внутренних ссылок, демонстрируя, что любые две статьи связаны через небольшое количество переходов.

## ⚙️Как работает:
1. Использует алгоритм поиска в глубину (DFS) с ограничением до 5 переходов
2. Парсит только внутренние ссылки Wikipedia (исключая служебные страницы)
3. Автоматически соблюдает rate-limiting (10 запросов/сек)
4. Анализирует связи в обоих направлениях (A→B и B→A)

## 🚀 Запуск скрипта

1. **Требования**:
  - Python 3.6+
  - Установленные зависимости:
      > pip install requests beautifulsoup4

2. **Способ запуска**:
      > python TToSH.py

3. **Настройка параметров** (в файле скрипта):
      > ARTICLE_1 = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
      > 
      > ARTICLE_2 = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
      > 
      > RATE_LIMIT = 10  # Максимальное количество запросов в секунду

## 📊 Пример вывода
![Снимок](https://github.com/user-attachments/assets/9fcf8bab-427d-464c-9ddb-1f929fa08f58)

Проверка первого пути:
1) Six degrees of separation (New Yorkers) ->
2) New York City (Mayor Fernando Wood) ->
3) Fernando Wood (New York secede) ->
4) Partition and secession in New York (Vermont – succeeded) ->
5) Vermont (ABC) ->
6) American Broadcasting Company

Проверка второго пути:
1) American Broadcasting Company (by Edward J. Noble) ->
2) Edward J. Noble (broadcasting and) ->
3) Broadcasting (External links -> Telecommunications -> Nishizawa) ->
4) Jun-ichi Nishizawa (External links -> Telecommunications -> social media) ->
5) Social media (six degrees) ->
6) Six degrees of separation
