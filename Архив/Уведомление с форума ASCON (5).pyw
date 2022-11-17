#-------------------------------------------------------------------------------
# Name:        Уведомления с форума ASCON
# version:     v0.4.0
#
# Author:      dimak222
#
# Created:     25.08.2022
# Copyright:   (c) dimak222 2022
# Licence:     No
#-------------------------------------------------------------------------------

title = "Уведомление с форума ASCON"

icon = r"C:\Users\Каширских Дмитрий\Desktop\Дмитрий\ГОСТ\Прочее\Макросы\Уведомление с форума ASCON\cat.ico" # иконка в уведомлении (полный путь к иконке)

from sys import exit # для выхода из приложения без ошибки

def DoubleExe():# проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

    import subprocess # модуль вывода запущеных процессов
    from sys import exit # для выхода из приложения без ошибки

    CREATE_NO_WINDOW = 0x08000000 # отключённое консольное окно
    processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW).communicate()[0] # список всех процессов
    processes = processes.decode('cp866') # декодировка списка

    if str(processes).count(title[0:25]) > 2: # если найдено название программы (два процесса) с ограничением в 25 символов
        message(0, "Приложение уже запущено!") # сообщение, поверх всех окон и с автоматическим закрытием
        exit() # выходим из програмы
    else:
        message(0, "Приложение запущено!") # сообщение, поверх всех окон и с автоматическим закрытием

def resource_path(relative_path): # Для сохранения картинки внутри exe файла

    import os # модуль файловой системы

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def message(counter, text = "Ошибка!"): # сообщение, поверх всех окон и с автоматическим закрытием

    import tkinter.messagebox as mb # окно с сообщением
    import tkinter as tk # модуль окон

    if counter == 0: # время до закрытия приложения (если 0)
        counter = 4 # закрытие через 4 сек
    window = tk.Tk() # создание окна
    window.iconbitmap(default = resource_path("cat.ico")) # значёк программы
    window.attributes("-topmost",True) # окно поверх всех окон
    window.withdraw() # скрываем окно "невидимое"
    time = counter * 1000 # время в милисекундах
    window.after(time, window.destroy) # закрытие окна через n милисек
    if mb.showinfo(title, text) == "": # окно закрыто по времени
        pass
    else:
        window.destroy() # окно закрыто по кнопке
    window.mainloop() # отображение окна

def Txt_file(): # считываем значения из txt файла

    import os

    name_txt_file = title + ".txt" # название текстового файла

    if os.path.exists(name_txt_file): # если есть txt файл использовать его

        txt_file = open(name_txt_file, encoding = "utf-8") # открываем файл записи (w+), для чтения (r), (невидимый режим)
        lines = txt_file.readlines()  # прочитать все строки
        txt_file.close() # закрываем файл

        text_processing(lines, name_txt_file) # обработка текста (строки текста, путь к файлу)

    else: # если нет файла
        to_create_txt_file(name_txt_file) # создать txt файл рядом с программой с записью в него значений (путь к txt файлу)

    print(parameters)

    return parameters # возврящаем словарь в виде {Номер ячейки : Значение ячейки}

def text_processing(lines, Path): # обработка текста (строки текста, путь к файлу)

    import re # модуль регулярных выражений
    import time # модуль времени
    from sys import exit # для выхода из приложения без ошибки

    if lines == []: # если в файле нет записи, вписываем в файл опции для редактирования и инструкцию по использованию
        to_create_txt_file(Path) # создать txt файл с записью в него значений

    else: # если есть текст обратобать его

        try: # попытаться обработать значения в txt файле

            lines_clean = clearing_the_list(lines) # очистка списка строк от "#"

            for line in lines_clean: # для каждой строки производим обработку
                parameter = line.split("=") # делим по "="
                parameter[0] = parameter[0].strip() # убираем пробелы по бокам
                parameter[1] = parameter[1].strip().strip('"') # убираем пробелы и "..." по бокам

                if parameter[1].find("True") != -1: # если есть параметр со словом True, обрабатываем его
                    parameter[1] = True # присвоем значение "True"

                elif parameter[1].find("False") != -1: # если есть параметр со словом False, обрабатываем его
                    parameter[1] = False # присвоем значение "False"

                elif parameter[1].find(";") != -1: # если есть параметр с ";", обрабатываем его
                    parameter[1] = parameter[1].split(";") # разделяем параметр по ";"

                parameters[parameter[0]] = parameter[1] # добавляем в словарь параметры

        except:
            message(8, "Проверте правильность записи файла: \n\"" + Path + "\"\nИли удалите его, новый будет создан автоматически.")
            exit()

def clearing_the_list(lines): # очистка списка строк от "#"

    lines_clean = [] # список строк с чистым текстом (без текста после "#")

    for line in lines: # для каждой строки производим обработку

        if line.isspace(): # если пустая строка пропустить
            continue

        line_clean = line.split("#", 1)[0] # если в строке есть "#" не записывать всё что после неё

        if line_clean == "": # если нет записи до #, пропустиь строку
            continue

        lines_clean.append(line_clean) # список строк с чистым текстом (без текста после "#")

    return lines_clean # возврящаем чистые строки

def to_create_txt_file(name_txt_file): # создать txt файл с записью в него значений

    import os
    from sys import exit

    txt_file = open(name_txt_file, "w+") # открываем файл записи (w+), для чтения (r), (невидимый режим)

    txt = """my_topics = "False" # перечесление интересующих тем через ";", пример: "Уведомление с форума ASCON; Компас v21; Программа сохранения в PDF". "False" - выводит новые сообщения со всех тем
#-------------------------------------------------------------------------------
update_msg = "55; 100" # частота обновления сообщений, случайное значение от n до m секунд (верхняя граница не меньше 40 сек)
error_time = "5; 10" # время ожидания между ошибками (после 10 ошибок подряд выдаёт сообщение о прикращении работы), случайное значение от n до m секунд
first_msg = "True" # показывать первое прочитанное сообщение, False - не показывать
ignor_msg_editing = "False" # игнорировать сообщение, если оно было отредактировано, True - не показывает отредактированое сообщение
 """

    txt_file.write(txt) # записываем текст в файл
    txt_file.close() # закрываем файл

    os.startfile(name_txt_file) # открываем файл в системе
    message(0, "Введите необходимые значения!") # сообщение с названием файла
    exit() # выходим

def ASCON(): # уведомление от ASCONa

    import urllib.request # модуль открытия URL-адреса
    import re # регулярные выражения

    global ASCON_message

    dictionary = {r"&nbsp;":" ", # словарь замен
                r"&quot;":'"',
    			r"&amp;":"&",
    			r"\<blockquote class=[^\>]+\>":'\n"',
    			r"\<br\>\</blockquote\>":'"\n',
                r"</a></cite>" : " ",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/smiley.gif\" alt=\"&#58;&#41;\" title=\"Smiley\" class=\"smiley\">":"😄",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/wink.gif\" alt=\";&#41;\" title=\"Wink\" class=\"smiley\">":"😉",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/shocked.gif\" alt=\"&#58;o\" title=\"Shocked\" class=\"smiley\">":"😱",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/sad.gif\" alt=\"&#58;&#40;\" title=\"Sad\" class=\"smiley\">":"😔",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/blink.gif\" alt=\"8-&#41;\" title=\"\" class=\"smiley\">":"😉",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/cry.gif\" alt=\"&#58;`&#40;\" title=\"Cry\" class=\"smiley\">":"😭",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/mad.gif\" alt=\"&gt;&#58;&#40;\" title=\"Mad\" class=\"smiley\">":"🤬",
    			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/shuffle.gif\" alt=\"&#58;shu&#58;\" title=\"Shuffle\" class=\"smiley\">":"=/",
                r"<img src=\"https://forum.ascon.ru/Smileys/fugue/angel.gif\" alt=\"&#58;angel&#58;\" title=\"angel\" class=\"smiley\">":"😇",
                r"<img src=\"https://forum.ascon.ru/Smileys/fugue/rolleyes.gif\" alt=\"&#58;&#58;&#41;\" title=\"Roll Eyes\" class=\"smiley\">":"🙄",
                r"<br>":"\n",
    			r"(<[^>]+?>)":"",
                r"&gt;":">",
                r"&#39;": "'"}

    html = site_processing("https://forum.ascon.ru/index.php?action=recent") # обработка сайта

    topic = notification_message("rel=\"nofollow\" title=\"Re: (.+)\"", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    autor = notification_message("Последний ответ от <.+>\<a.+\"\>(.+)\<\/a\>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    msg = notification_message("<div class=\"list_posts\">(.+)<\/div>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    launch = notification_message("\/ <a href=\"(.+)\" rel=\"nofollow\" title=\"Re:", html) # поиск и вывод пути к теме сообщения из html (маска поиска, текст где искать)

    if my_topic(topic) == True: # проверка на интересующие темы

        topic = dictionary_processing(topic, dictionary) # обработка текста по словарю
        msg = dictionary_processing(msg, dictionary) # обработка текста по словарю

        if ASCON_message != "": # попытаться сравнить предыдущее сообщение

            if msg != ASCON_message:

                print(topic + "От " + autor + ":" + msg)

                Windows_msg(Name_app = title, title = topic, msg = "От " + autor + ": " + msg, duration = "short", icon = icon, launch = launch) # сообщение Windows
                ASCON_message = msg # прочитанное сообщение

            else:
                print("Новых сообщений нет!")

        else: # если нет сообщения присвоить ему текст

            print("Перве сообщение!"),
            Windows_msg(Name_app = "Первое уведомление с форума ASCON", title = topic, msg = "От " + autor + ": " + msg, duration = "short", icon = icon, launch = launch) # сообщение Windows
            ASCON_message = msg # прочитанное сообщение

    else: # нет интересующих тем

        print("Нет интересующих тем!")

def site_processing(site): # обработка сайта

    import urllib.request # модуль открытия сайтов

    response = urllib.request.urlopen(site) # открываем сайт
    html = response.read().decode("utf-8") # считываем с него значения
    response.close() # закрываем модуль

    return html # возвращаем считаные строки сайта

def notification_message(mask, html): # поиск и вывод значений из html (маска поиска, текст где искать)

    import re # модуль регулярных выражений

    z = 0 # номер поиска сообщения

    text = re.findall(mask, html)[z] # ищем название темы

    return text # возвращаем найденые значения

def my_topic(topic): # проверка на интересующие темы (название темы)

    if parameters["my_topics"] != False: # если введены интересующие темы

        for my_topic in parameters["my_topics"]: # для каждой темы производим обработку

            my_topic = my_topic.strip() # убираем пробелы по бокам

            print("Интересующие тема:", my_topic)

            if my_topic == topic: # если интересующая тема и новая темы совпали

                return True # выводим True (продолжаем обработку текста)

    else: # не введены интересующие темы

        return True # выводим True (продолжаем обработку текста)

def dictionary_processing(text, dictionary): # обработка текста по словарю

    import re # модуль регулярных выражений

    for key in dictionary: # обрабатываем каждую замену из словаря
        text = re.sub(key, dictionary[key], text) # меняем найденые значения

    return text

def Windows_msg(Name_app = "Уведомление", title = "Заголовок", msg = "Сообщение", duration = "short", icon = "", launch = ""): # сообщение Windows

    from winotify import Notification, audio

    toast = Notification(app_id = Name_app, # название программы
                         title = title, # заголовок
                         msg = msg, # сообщение
                         duration = duration, # время отображения ("short" или "long")
                         icon = icon, # полный путь к иконке
                         launch = launch) # что открывать при нажатии на уведомление

    toast.set_audio(audio.Default, loop = False) # звук сообщения

##    toast.add_actions(label = "Ссылка", launch = "https://github.com/versa-syahptr/winotify/") # кнопка в сообщении

    toast.show() # запустить

def Sleep(n, m): # остановка на случайное от n до m секунд

    import random # импорт модуля случайных чисел
    import time # модуль для пауз

    if n > m: # если первое число больше второго сравнять их
        n = m

    randomN = random.randint(n, m) # случайное целое число от n до m

    print(randomN)
    time.sleep(randomN) # остановка на n секунд

def error(e = "Ошибка!"): # в случае ошибки пытаеться 10 повторить выполнение программы (имя ошибки)

    global err

    print("Ошибка" , err, ":", e)

    if err < 11: # если ошибок меньше задонного числа

        err += 1 # добавляем значение к счётчику ошибок

        try: # попытаться сделать паузу

            Sleep(int(parameters["error_time"][0]), int(parameters["error_time"][1])) # остановка на случайное от n до m секунд

        except:
            message(8, "Проверте правильность записи параметра: " + "error_time" + "\"\nИли удалите файл, новый будет создан автоматически.")
            exit()

    else:
        Windows_msg(Name_app = "Уведомление с форума ASCON", title = "Отслеживание сообщений прекращено!", msg = "Последняя ошибка: " + "\"" + str(e) + "\"", duration = "short", icon = icon, launch = "") # сообщение Windows
        exit() # выходим из програмы

#-------------------------------------------------------------------------------

parameters = {} # словарь с параметрами
ASCON_message = "" # сообщение для сравнения
err = 0 # счётчик ошибок

DoubleExe() # проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

Txt_file()

while 1: # цикл обработки сообщений

    try: # попытаться выполнить программу

        ASCON() # уведомление от ASCONa

        err = 0 # сбрасываем счётчик ошибок

        if int(parameters["update_msg"][1]) < 40: # если верхний порог меньще 40 сек присвоить ему 30 сек (что бы не DDosить)
            parameters["update_msg"][1] = 40 # 40 сек верхний порог

        Sleep(int(parameters["update_msg"][0]), int(parameters["update_msg"][1])) # остановка на случайное от n до m секунд

    except Exception as e: # ловим любые ошибки

        error(e) # в случае ошибки пытаеться 10 повторить выполнение программы (имя ошибки)