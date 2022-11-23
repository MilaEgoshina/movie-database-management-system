import csv
import easygui as gui
from easygui import *
import pandas as pd
import user_interface as user

def add_info():
    msg = 'Введите название нового фильма и его жанр'
    title = 'Добавление нового фильма в БД'
    values = ['Название фильма','Жанр']
    films = pd.read_csv('movies.csv')
    fill_value = user.field_check(msg,title,values)
    line = int(films['movieId'].iloc[-1])
    names = films['title'].to_list()
    if fill_value != None:
        if fill_value[0] in names:
            msgbox('Этот фильм уже есть в базе данных')
        else:
            new_film = []
            new_film.append(fill_value[0])
            new_film.append(fill_value[1])
            line +=1
            new_film.insert(0,str(line))
            with open('movies.csv','a',newline='') as file:
                new_info = csv.writer(file)
                new_info.writerow(new_film)
            msgbox('Новый фильм был успешно загружен в базу данных')

def delete_info():
    msg = 'Введите название фильма совместно с годом его выпуска, для того чтобы его удалить из БД'
    title = 'Удаление фильма из БД'
    choices = ['Название фильма',"Год выпуска"]
    fill_vallue = user.field_check(msg,title,choices)
    films = pd.read_csv('movies.csv')
    names = films['title'].to_list() 
    if fill_vallue != None:
        fill_vallue[1] = '(' + fill_vallue[1] + ')'
        del_film = str(fill_vallue[0] +' ' + fill_vallue[1])

        if del_film in names:
            delete_row('movies.csv','title',del_film)
            msgbox('Фильм был успешно удален')
        else:
            msgbox('Такого фильма нет')

def delete_row(file, column_name, *args):

    row_to_remove = []
    for row_name in args:
        row_to_remove.append(row_name)

    try:
        df = pd.read_csv(file)
        for row in row_to_remove:
            df = df[eval("df.{}".format(column_name)) != row]
        df.to_csv(file, index=False)
    except Exception  as e:
        raise Exception("Error message....")








