import sqlite3 as sq
from E3S_class import Parser

url = r'https://www.e3s-conferences.org/articles/e3sconf/abs/2022/17/contents/contents.html'
a = Parser(url)

# Список выходных данных статей сборника
lst = a.get_articles()

# Сохранение в базе данных
with sq.connect("articles.db") as con:
    cur = con.cursor()
    #Если нет такой таблицы, то создаем ее
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