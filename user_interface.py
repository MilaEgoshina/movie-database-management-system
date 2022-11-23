import easygui as gui
from easygui import *
import find_and_show_inf as find
import add_and_save_inf as add

def searching_and_sorting():# Эта функция вызывает главное меню графического интерфейса пользователя и предлагает сделать выбор
    message = 'Выберите, что хотите сделать: '
    title = 'Главное меню'
    choises = ['Искать фильм по жанру','Искать фильм по тэгу','Добавить фильм в базу данных',"Удаление фильма из БД"]
    fill_vallues = choicebox(message,title,choises)
    if fill_vallues == 'Искать фильм по жанру':
        genre_entry()
    elif fill_vallues == 'Искать фильм по тэгу':
        tags_entry()
    elif fill_vallues == 'Добавить фильм в базу данных':
        add.add_info()
    elif fill_vallues == 'Удаление фильма из БД':
        add.delete_info()

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
        find.similarity_tags(user_input)#функция, которая проверяет ввод пользователя на сходство с данными в файле, если пользователь нажимает отмену, то его возвращает обратно на главное меню

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
        find.similarity_genre(user_input2)
    else:
        searching_and_sorting()

