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
    rating = pd.read_csv('ratings.csv',usecols=[1,2])

    df = pd.merge(films,rating,on = 'movieId',how = 'outer')
    df['rating'] = df['rating'].fillna(df['rating'].mean())
    df = pd.DataFrame(df.groupby('movieId')['rating'].mean().reset_index().round(1))#получаем средний рейтинг по фильму и группируем его по названию фильма
    df['title'] = films['title']
    df['genres'] = films['genres']

    progress_bar.next()
progress_bar.finish()

def searching_and_sorting():# Эта функция вызывает главное меню графического интерфейса пользователя и предлагает сделать выбор
    message = 'Выберите, что хотите сделать: '
    title = 'Главное меню'
    choises = ['Искать фильм по жанру','Искать фильм по тэгу']
    fill_vallues = choicebox(message,title,choises)
    # if fill_vallues == 'Искать фильм по жанру':
    #     genre_entry()
    # elif fill_vallues == 'Искать фильм по тэгу':
    #     tags_entry()