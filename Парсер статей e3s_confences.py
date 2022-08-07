import time
import requests
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import xlwt


def get_articles(html):
    """Загрузка данных статей из выбранного сборника"""

    soup = BeautifulSoup(html, 'html.parser')  # делаем суп
    res = soup.find_all('div', attrs={'class': 'export-article'})  # поиск по тегу <div>, который содержит class
    lst = []
    for div in res:
        avt = [i.text for i in div.find('div', class_='article-authors').find_all('span')]  # авторы
        avt = list(
            map(lambda x: ' '.join(x.split('\xa0')), avt))  # удаление нечитаемых символов, стоящих между авторами
        article = div.find('a').text  # статьи
        referes = dom + div.find('a').get('href')  # ссылки на статью
        publ_data = div.find('div', class_='article_date_pub').text  # дата публикации
        doi = div.find('div', class_='article_doi').find('a').get('href')  # DOI ссылка
        pdf_ref = dom + div.find('div', class_='article_doc').find('a').get('href')  # pdf ссылка
        lst.append((avt, article, referes, publ_data, doi, pdf_ref))  # список с данным статей
    return lst


def download_to_file(pdf_ref, article):
    # Загрузка pdf файлов на диск
    byte = requests.get(pdf_ref).content
    time.sleep(1)
    try:
        with open(f'articles/{article}.pdf', 'wb') as f:
            f.write(byte)
            print(f'Запись файла {article}.pdf прошла успешно!')
    except FileNotFoundError:
        print(f'Скорее всего произошла ошибка в названии файла {article}... .pdf')


def write_to_txt(lst):
    """Запись данных в текстовый файл"""
    with open('file_articles.txt', 'w', encoding='utf8') as f:
        for count, i in enumerate(lst):
            print(f'{count + 1}  ', *i[:2], i[-2:], '\n', file=f)


def write_to_excel(lst):
    """Запись данных в файл Excel"""
    # Настройка оформления и стилей
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Статьи')
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if j == 0:
                ws.write(i, j, ', '.join(lst[i][j]))
            else:
                ws.write(i, j, lst[i][j])
    wb.save('Results2022.xls')


def main():
    global dom
    dom = 'https://www.e3s-conferences.org'
    # url = 'https://www.e3s-conferences.org/articles/e3sconf/abs/2021/61/contents/contents.html'
    url = 'https://www.e3s-conferences.org/articles/e3sconf/abs/2022/20/contents/contents.html'
    resp = urlopen(url)  # скачиваем файл - функция из библиотеки
    html = resp.read().decode('utf8')  # считываем содержимое

    lst = get_articles(html)
    pdf_ref = lst[-1]
    article = lst[1]

    change = input(
        """Нажимте клавишу 1 - если надо скачать файл статьи; 2 -  если надо записать в текстовый файл; 3 - если надо записать в excel; любую другую клавишу - если без записи в файл  """)
    if change == '1':
        download_to_file(pdf_ref, article)
    elif change == '2':
        write_to_txt(lst)
    elif change == '3':
        write_to_excel(lst)
    else:
        print('Был выбран режим без записи результатов.')
    print('Парсинг прошел успешно!!!')


if __name__ == '__main__':
    main()
