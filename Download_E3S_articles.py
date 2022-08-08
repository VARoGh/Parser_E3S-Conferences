from E3S_class import Parser

url = r'https://www.e3s-conferences.org/articles/e3sconf/abs/2022/21/contents/contents.html'
a = Parser(url)

# Список выходных данных статей сборника
lst = a.get_articles()

message = input('Нажмите 1 для записи выходных данных статей в файл excel,\n'
                '2 - в текстовый файл,\nдля продолжения без записи - любую другую клавишу ')

if message == '1':
    # Сохранение полученных данных в файл Excel
    a.write_to_excel()
if message == '2':
    # Сохранение полученных данных в текстовый файл
    a.write_to_txt()

message = input('Нажмите y для загрузки файлов статей ')
if message == 'y':
    a.download_to_file()
