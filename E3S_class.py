import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlwt


class Parser:
    def __init__(self, url):
        self.url = url

    def get_articles(self):
        """Загрузка данных статей из выбранного сборника"""
        resp = urlopen(self.url)
        html = resp.read().decode('utf8')  # считываем содержимое
        soup = BeautifulSoup(html, 'html.parser')
        res = soup.find_all('div', attrs={'class': 'export-article'})  # поиск по тегу <div>, который содержит class
        self.lst = []
        for div in res:
            dom = 'https://www.e3s-conferences.org'
            avt = [i.text for i in div.find('div', class_='article-authors').find_all('span')]  # авторы
            avt = list(
                map(lambda x: ' '.join(x.split('\xa0')), avt))  # удаление нечитаемых символов, стоящих между авторами
            article = div.find('a').text  # статьи
            referes = dom + div.find('a').get('href')  # ссылки на статью
            publ_data = div.find('div', class_='article_date_pub').text  # дата публикации
            publ_data = publ_data.split(': ')[1]
            doi = div.find('div', class_='article_doi').find('a').get('href')  # DOI ссылка
            pdf_ref = dom + div.find('div', class_='article_doc').find('a').get('href')  # pdf ссылка
            self.lst.append([avt, article, referes, publ_data, doi, pdf_ref])  # список с данными статей
        return self.lst

    def download_to_file(self):
        """Загрузка pdf файлов на диск"""
        pdf_ref = [i[-1] for i in self.lst]
        article = [i[1] for i in self.lst]
        for i in range(len(pdf_ref)):
            time.sleep(1)
            byte = requests.get(pdf_ref[i]).content
            try:
                with open(f'articles/{article[i]}.pdf', 'wb') as f:
                    f.write(byte)
                    print(f'Запись файла {article[i]}.pdf прошла успешно!')
            except FileNotFoundError:
                print(f'Скорее всего произошла ошибка в названии файла {article[i]}... .pdf')
        print('Загрузка pdf-файлов прошла успешно!')

    def write_to_txt(self):
        """Запись данных в текстовый файл"""
        with open('file_articles.txt', 'w', encoding='utf8') as f:
            for count, i in enumerate(self.lst):
                print(f'{count + 1}  ', *i[:2], i[-2:], '\n', file=f)
        print('Запись в файл txt прошла успешно!')

    def write_to_excel(self):
        """Запись данных в файл Excel"""
        # Настройка оформления и стилей
        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Статьи')
        for i in range(len(self.lst)):
            for j in range(len(self.lst[0])):
                if j == 0:
                    ws.write(i, j, ', '.join(self.lst[i][j]))
                else:
                    ws.write(i, j, self.lst[i][j])
        wb.save('Results2022.xls')
        print('Запись в файл Excel прошла успешно!')

def main():
    a = Parser(r'https://www.e3s-conferences.org/articles/e3sconf/abs/2022/20/contents/contents.html')
    lst = a.get_articles()
    print(lst)
    a.write_to_excel()
    a.write_to_txt()
    a.download_to_file()

if __name__ == '__main__':
    main()


