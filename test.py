import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from progress.bar import IncrementalBar
import easygui as gui
from easygui import *
import sys#Модуль sys обеспечивает доступ к некоторым переменным и функциям, взаимодействующим с интерпретатором python.

np.set_printoptions(threshold=sys.maxsize)# максимальное значение числа типа Py_ssize_t 

progress_bar = IncrementalBar('Загрузка фильмов', max = 1)
for i in range(1):
    tags = pd.read_csv('tags.csv',usecols=[1,2])
    films = pd.read_csv('movies.csv')
    ratings = pd.read_csv('ratings.csv',usecols=[1,2])

    df = pd.merge(films,ratings,on = 'movieId',how = 'outer')
    df['rating'] = df['rating'].fillna(df['rating'].mean())
    df = pd.DataFrame(df.groupby('movieId')['rating'].mean().reset_index().round(1))#получаем средний рейтинг по фильму и группируем его по названию фильма
    df['title'] = films['title']
    df['genres'] = films['genres']
    print(df)

    progress_bar.next()
progress_bar.finish()


def searching_and_sorting():# Эта функция вызывает главное меню графического интерфейса пользователя и предлагает сделать выбор
    message = 'Выберите, что хотите сделать: '
    title = 'Главное меню'
    choises = ['Искать фильм по жанру','Искать фильм по тэгу']
    fill_vallues = choicebox(message,title,choises)
    if fill_vallues == 'Искать фильм по жанру':
        genre_entry()
    elif fill_vallues == 'Искать фильм по тэгу':
        tags_entry()

def field_check(message,title,field_names):
    field_values = multenterbox(message,title,field_names)
    print(f'field_values {field_values}')
    while 1:
        if field_values is None: break
        errormsg = ''
        for i in range(len(field_values)):
            if field_values[i].strip() == '':
                errormsg += ('"%s" is a required field.\n\n' % field_names[i])
        if errormsg == '':
            break
        field_values = multenterbox(errormsg,message,title,field_names)#сохраняем ввод пользователя в переменной field_values в виде списка
    return field_values


def tags_entry():# Эта функция определяет параметры easygui multenterbox и вызывает field_check, если пользователь вводил значнеие, вызывает тест на подобие; если совпадение не найдено, пользователь возвращается окно ввода
    message = 'Введите, пожалуйста, тэг для поиска фильма, например: Brad Pitt | fantasy \nЕсли такого тэга нет, то Вы вернетесь обратно в главное меню'
    title = 'Поиск'
    field_names = ['Tag']

    field_values = field_check(message,title,field_names)#функция, которая проверяет : не оставил ли пользователь пустое окно для ввода
    if field_values != None:
        global user_input
        user_input = field_values[0]#если пользователь ввел значение, то сохраняем его в переменную user_input
        print(f'user_inpit tag {user_input}')
        similarity_tags(user_input)#функция, которая проверяет ввод пользователя на сходство с данными в файле, если пользователь нажимает отмену, то его возвращает обратно на главное меню

    else:
        searching_and_sorting()
    
def genre_entry():
    message = 'Введите,пожалуйста, интересующий Вас жанр для поиска фильма,например: comedy| mystery\nЕсли такого жанра нет, то Вы вернетесь обратно в главное меню'
    title = 'Поиск'
    field_names = ['Genre']

    field_values = field_check(message,title,field_names)
    if field_values != None:
        global user_input2
        user_input2 = field_values[0]
        print(f'user_input genre {user_input2}')
        similarity_genre(user_input2)
    else:
        searching_and_sorting()

def tag():#функция, которая добавляет все совпадающие по тегам фильмы в датафрейм
    similarity1 = []
    for i in similarity:
        similarity1.append(tags.loc[tags['tag'].isin(i)])#записываем в отдельный список строки из датафрейма с тэгами, если тэг пользователя и имеющийся тег совпал
    print('similarity',similarity1)
    #во временном листе сбрасываем индекс,удаляем столбец с индексами и повторяющиеся записи
    temp_list = similarity1[0]
    print('temp:',temp_list)
    temp_list = temp_list.reset_index()
    temp_list.drop('index',axis = 1, inplace = True)
    temp_list = temp_list.drop_duplicates(subset = 'movieId')
    #нам необходимо объединить временный лист с основным датафреймом по общему столбцу MovieID, для того чтобы определить названия и жанры найденных фильмов по тэгам
    df1 = pd.merge(temp_list,df,on = 'movieId',how='left')
    df1.drop('tag',axis=1,inplace=True)
    df1.drop('movieId',axis=1,inplace=True)
    #далее сортируем фильмы по рейтингу и показываем пользователю фильмы с рейтингов более 2.5
    df_sort = df1.sort_values(by = 'rating',ascending=False)
    df_sort = df_sort[df_sort['rating'] > 2.5]
    headings = []#сюда будем записывать названия столбцов для корректного отображения с помощью дальнейшего использования библиотеки 
    headings.insert(0,{'rating': 'Рейтинг','title': '--------Название фильма','genres':'--------Жанр'})
    df_sort = pd.concat([pd.DataFrame(headings),df_sort],ignore_index=True,sort=True)

    rating = df_sort['rating'].to_list()
    genres = df_sort['genres'].to_list()
    titles = df_sort['title'].to_list()

    #преобразуем один список numpy из получившихся списков для дальнейшего его использования в eaygui

    df_sort = np.concatenate([np.array(i)[:,None] for i in [rating,genres,titles]],axis = 1)
    df_sort.nbytes
    df_sort= str(df_sort).replace('[','').replace(']','')
    gui.codebox(msg="Вот фильмы, которые мы подобрали по выбранным тэгам:",text=(df_sort),title='Фильмы')
    

    searching_and_sorting()

def genre():
    similarity_genres = []
    for i in similarity2:
        similarity_genres.append(films.loc[films['genres'].isin(i)])
    
    temp_list = similarity_genres[0]
    temp_list = temp_list.reset_index()
    temp_list.drop('index',axis = 1,inplace = True)
    temp_list.drop('title',axis = 1,inplace = True)
    temp_list.drop('genres',axis = 1,inplace = True)
    temp_list = temp_list.drop_duplicates(subset = 'movieId')

    df1 = pd.merge(temp_list,df,on='movieId',how= 'left')
    df_sort = df1.sort_values(by = 'rating',ascending=False)
    df_sort = df_sort[df_sort['rating'] > 2.5]
    heading = []
    heading.insert(0,{'rating':'Рейтинг','title':'-------Название фильма:','genres': '-----------Жанр'})
    df_sort = pd.concat([pd.DataFrame(heading),df_sort],ignore_index=True,sort= True)

    rating = df_sort['rating'].to_list()
    titles = df_sort['title'].to_list()
    genres = df_sort['genres'].to_list()

    df_sort = np.concatenate([np.array(i)[:,None] for i in[rating,titles,genres]],axis = 1)
    df_sort.nbytes
    df_sort = str(df_sort).replace('[','').replace(']','')
    gui.codebox(msg='Вот названия фильмов по выбранным Вами жанрам',text=(df_sort),title='Фильмы')

    searching_and_sorting()

def similarity_tags(user_input):#функция, которая сравнивает ввод пользователя с данными в файлах на предмет совпадения более 90%
    tag_list = tags['tag'].unique()
    query = user_input
    choises = tag_list
    res = process.extract(query,choises)
    print(res)
    global similarity
    similarity = [i for i in res if i[1] > 90]
    print(similarity)
    if similarity == []:#если совпадений не найдено, то возвращаемся обратно в окно ввода
        tags_entry()
    else:
        tag()
def similarity_genre(user_input2):
    genre_list = films['genres'].unique()
    query = user_input2
    choises = genre_list
    res = process.extract(query,choises)
    global similarity2
    similarity2 = [i for i in res if i[1] > 90]
    if similarity2 == []:
        genre_entry()
    else:
        genre()

if __name__ == '__main__':
    searching_and_sorting()