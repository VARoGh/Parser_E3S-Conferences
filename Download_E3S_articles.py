from E3S_class import Parser

url = r'https://www.e3s-conferences.org/articles/e3sconf/abs/2022/21/contents/contents.html'
a = Parser(url)

# Список выходных данных статей сборника
lst = a.get_articles()

message = input('Если необходимо записать выходные данные статей в файл, '
                'то нажмите \n1 - для записи в excel,\n2 - в текстовый файл,\n'
                'любую другую клавишу - не записывать данные статей  ')
if message == '1':
    # Сохранение полученных данных в файл Excel
    a.write_to_excel()
if message == '2':
    # Сохранение полученных данных в текстовый файл
    a.write_to_txt()

message = input('Скачать файлы статей? Если да - нажмите y, если нет - любую другую клавишу ')
if message == 'y':
    # Сохранение полученных данных в файл Excel
    # Загрузка статей в формате pdf
    a.download_to_file()


