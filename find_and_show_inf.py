import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import easygui as gui
from easygui import *
from progress.bar import IncrementalBar
import sys
import user_interface as us

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
    

    us.searching_and_sorting()

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

    us.searching_and_sorting()

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
        us.tags_entry()
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
        us.genre_entry()
    else:
        genre()