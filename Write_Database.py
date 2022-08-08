import requests
import time
import random
import sqlite3 as sq
from E3S_class import Parser


def save_database(lst: list) -> None:
    """Сохранение в базу данных"""
    with sq.connect("articles.db") as con:
        cur = con.cursor()
        # Если нет такой таблицы, то создаем ее
        cur.execute("""CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        author TEXT,
                        title TEXT,
                        url TEXT,
                        date TEXT,
                        doi TEXT,
                        url_pdf TEXT)
                        """)
        count = 0
        for article in lst:
            article[0] = ', '.join(article[0])
            cur.execute("""
                        SELECT doi FROM articles WHERE doi = (?)
                        """, (article[4],))
            result = cur.fetchone()
            # Проверка на присутствие записи в базе
            if result is None:
                cur.execute("""
                            INSERT INTO articles
                            VALUES (NULL, ?, ?, ?, ?, ?, ?)
                            """, article)
                count += 1
    print(f'В базу данных добавлено {count} записей')


def main():
    year = int(input('Выберите год публикации сборников статей:  '))
    count = 0
    while True:
        count += 1
        url = f'https://www.e3s-conferences.org/articles/e3sconf/abs/{year}/{count:02}/contents/contents.html'
        if requests.get(url).status_code == 404:
            print('Такой страницы не существует.')
            print('Программа остановлена.')
            break
        a = Parser(url)
        lst = a.get_articles() # Список выходных данных статей сборника
        save_database(lst)
        time.sleep(random.random() * 3)


if __name__ == '__main__':
    main()
