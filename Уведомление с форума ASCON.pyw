#-------------------------------------------------------------------------------
# Author:      dimak222
#
# Created:     25.08.2022
# Copyright:   (c) dimak222 2022
# Licence:     No
#-------------------------------------------------------------------------------

title = "Уведомление с форума ASCON"
ver = "v0.7.1.3"

icon = r"C:\Users\Каширских Дмитрий\Desktop\Дмитрий\ГОСТ\Прочее\Макросы\Уведомление с форума ASCON\cat.ico" # иконка в уведомлении (полный путь к иконке)

from sys import exit # для выхода из приложения без ошибки

def DoubleExe():# проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

    import subprocess # модуль вывода запущеных процессов
    import os # модуль файловой системы
    from sys import exit # для выхода из приложения без ошибки

    CREATE_NO_WINDOW = 0x08000000 # отключённое консольное окно
    processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW).communicate()[0] # список всех процессов
    processes = processes.decode('cp866') # декодировка списка

    filename = os.path.basename(__file__) # имя запускаемого файла

    if str(processes).count(filename[0:25]) > 2: # если найдено название программы (два процесса) с ограничением в 25 символов
        Message("Приложение уже запущено!") # сообщение, поверх всех окон и с автоматическим закрытием
        exit() # выходим из програмы
    else:
        Message("Приложение запущено!") # сообщение, поверх всех окон и с автоматическим закрытием

def Message(text = "Ошибка!", counter = 4): # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)

    from threading import Thread # библиотека потоков
    import time # модуль времени

    def Resource_path(relative_path): # для сохранения картинки внутри exe файла

        import os # работа с файовой системой

        try: # попытаться определить путь к папке
            base_path = sys._MEIPASS # путь к временной папки PyInstaller

        except Exception: # если ошибка
            base_path = os.path.abspath(".") # абсолютный путь

        return os.path.join(base_path, relative_path) # объеденяем и возващаем полный путь

    def Message_Thread(text, counter): # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)

        import tkinter.messagebox as mb # окно с сообщением
        import tkinter as tk # модуль окон

        if counter == 0: # время до закрытия окна (если 0)
            counter = 1 # закрытие через 1 сек
        window_msg = tk.Tk() # создание окна
        try: # попытаться использовать значёк
            window_msg.iconbitmap(default = Resource_path("cat.ico")) # значёк программы
        except: # если ошибка
            pass # пропустить
        window_msg.attributes("-topmost",True) # окно поверх всех окон
        window_msg.withdraw() # скрываем окно "невидимое"
        time = counter * 1000 # время в милисекундах
        window_msg.after(time, window_msg.destroy) # закрытие окна через n милисекунд
        if mb.showinfo(title, text, parent = window_msg) == "": # информационное окно закрытое по времени
            pass # пропустить
        else: # если не закрыто по времени
            window_msg.destroy() # окно закрыто по кнопке
        window_msg.mainloop() # отображение окна

    msg_th = Thread(target = Message_Thread, args = (text, counter)) # запуск окна в отдельном потоке
    msg_th.start() # запуск потока

    msg_th.join() # ждать завершения процесса, иначе может закрыться следующие окно

def Txt_file(): # считываем значения из txt файла

    import os # работа с файовой системой

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

    global parameters # делаем глобальным список с параметрами

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

                elif parameter[1].find("False") != -1 or parameter[1].strip() == "": # если есть параметр со словом False, обрабатываем его
                    parameter[1] = False # присвоем значение "False"

                elif parameter[1].find(";") != -1: # если есть параметр с ";", обрабатываем его
                    parameter[1] = parameter[1].split(";") # разделяем параметр по ";", создаёться список

                try: # пытаемся добавить параметры в словарь
                    parameters[parameter[0]] = parameter[1] # добавляем в словарь параметры

                except NameError: # если нет словаря создаём его и добавляем параметры
                    parameters = {} # создаём словарь с параметрами
                    parameters[parameter[0]] = parameter[1] # добавляем в словарь параметры

        except:
            Message("Проверте правильность записи файла: \n\"" + Path + "\"\nИли удалите его, новый будет создан автоматически.", 8)
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

    txt_file = open(name_txt_file, "w+", encoding = "utf-8") # открываем файл записи (w+), для чтения (r), (невидимый режим)

    txt = """my_topics = "False" # перечисление интересующих тем через ";", пример: "Макрос "Уведомления о новых сообщениях на форуме"; Компас v21; Программа сохранения в PDF". "False" или "" - выводит новые сообщения со всех тем
blacklist_of_topics = "False" # перечисление не интересующих тем через ";", пример: "Трубопроводы, сваренные из гнутого листа. Накладки на стыки; Электрика: мощность резистора ПЭВР-50, как она изменяется при регулировании.". "False" или "" - выводит новые сообщения со всех тем
#-------------------------------------------------------------------------------
update_msg = "55; 100" # частота обновления сообщений, случайное значение от n до m секунд (нижняя граница не меньше 20 сек, верхняя граница не меньше 40 сек)
error_time = "10; 20" # время ожидания между ошибками (после 10 ошибок подряд выдаёт сообщение о прикращении работы), случайное значение от n до m секунд
first_msg = "False" # показывать первое прочитанное сообщение (непосредственно после запуска приложения, актуально при параметре my_topics = "False"), "True" - показывать
 """

    txt_file.write(txt) # записываем текст в файл
    txt_file.close() # закрываем файл

    os.startfile(name_txt_file) # открываем файл в системе
    Message("Введите необходимые значения! \nИ запустите приложение повторно.") # сообщение с названием файла
    exit() # выходим

def ASCON(): # уведомление от ASCONa

    import urllib.request # модуль открытия URL-адреса
    import re # регулярные выражения

    global ASCON_message

    dictionary = {r"&nbsp;":" ", # словарь замен
                r"&quot;":"\"",
    			r"&amp;":"&",
    			r"\<blockquote class=[^\>]+\>":'\n"',
                r"\<br\>\</blockquote\>":'"\n',
    			r"</blockquote\>":'"\n',
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

    topic = notification_message("rel=\"nofollow\" title=\"(.+)\"", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    autor = notification_message("Последний ответ от <.+>\<a.+\"\>(.+)\<\/a\>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    msg = notification_message("<div class=\"list_posts\">(.+)<\/div>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    launch = notification_message("\/ <a href=\"(.+)\" rel=\"nofollow\"", html) # поиск и вывод пути к теме сообщения из html (маска поиска, текст где искать)


    topic = topic.split("Re: ") # делим текст темы на "Re: "

    if len(topic) > 1: # если поделилось, используем 2-ю часть
        topic = topic[1] # 2-я часть списка

    else: # не делилось на "Re: "
        topic = "🆕 " + topic[0] # к начало темы добавляем значёк "🆕"

##    print(topic)
##    exit()

    if blacklist_of_topic(topic) == True: # проверка на не интересующие темы (название темы)

        if my_topic(topic) == True: # проверка на интересующие темы

            topic = dictionary_processing(topic, dictionary) # обработка текста по словарю
            topic = re.sub("\"", "''", topic) # меняем " => '' т.к. не выдаёт сообщение если в заголовке "

            msg = dictionary_processing(msg, dictionary) # обработка текста по словарю

##            print(topic)
##            exit()

            if ASCON_message != "": # попытаться сравнить предыдущее сообщение

                if msg != ASCON_message:

                    print(topic + "\nОт " + autor + ":\n" + msg)

                    Windows_msg(Name_app = title, title = topic, msg = "От " + autor + ": " + msg, duration = "short", icon = icon, launch = launch) # сообщение Windows
                    ASCON_message = msg # прочитанное сообщение

                else:
                    print("Новых сообщений нет!")

            else: # если нет сообщения присвоить ему текст

                if parameters["first_msg"]: # показывать первое прочитанное сообщение (непосредственно после запуска приложения, актуально при параметре my_topics = "False")
                    print("Первое сообщение!")
                    print(topic + "\nОт " + autor + ":\n" + msg)
                    Windows_msg(Name_app = "Первое уведомление с форума ASCON", title = topic, msg = "От " + autor + ": " + msg, duration = "short", icon = icon, launch = launch) # сообщение Windows

                ASCON_message = msg # прочитанное сообщение

        else: # нет интересующих тем

            ASCON_message = msg # прочитанное сообщение

            print("Нет интересующих тем!")

    else: # тема в чёрном списке

        ASCON_message = msg # прочитанное сообщение

        print("Тема в чёрном списке!")

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

        if type(parameters["my_topics"]) == list: # если значение параметра список, обработать каждое значение

            for my_topic in parameters["my_topics"]: # для каждой темы производим обработку

                my_topic = my_topic.strip() # убираем пробелы по бокам

                print("Интересующая тема:", my_topic)

                if my_topic == topic: # если интересующая тема и новая темы совпали

                    return True # выводим True (продолжаем обработку текста)

        else: # не список

            my_topic = parameters["my_topics"].strip() # убираем пробелы по бокам

            if my_topic == topic: # если интересующая тема и новая темы совпали

                print("Интересующая тема:", my_topic)

                return True # выводим True (продолжаем обработку текста)

    else: # не введены интересующие темы

        return True # выводим True (продолжаем обработку текста)

def blacklist_of_topic(topic): # проверка на не интересующие темы (название темы)

    if parameters["blacklist_of_topics"] != False: # если введены не интересующие темы и не пусто

        if type(parameters["blacklist_of_topics"]) == list: # если значение параметра список, обработать каждое значение

            for blacklist_of_topic in parameters["blacklist_of_topics"]: # для каждой темы производим обработку

                blacklist_of_topic = blacklist_of_topic.strip() # убираем пробелы по бокам

                print("Не интересующая тема:", blacklist_of_topic)

                if blacklist_of_topic == topic: # если не интересующая тема и новая темы совпали

                    return False # выводим False (не продолжаем обработку текста)

            return True # выводим True (продолжаем обработку текста)

        else: # не список

            blacklist_of_topic = parameters["blacklist_of_topics"].strip() # убираем пробелы по бокам

            if blacklist_of_topic == topic: # если не интересующая тема и новая темы совпали

                print("Не интересующая тема:", blacklist_of_topic)

                return False # выводим False (не продолжаем обработку текста)

            else: # темы не совпали

                return True # выводим True (продолжаем обработку текста)

    else: # не введены интересующие темы

        return True # выводим True (продолжаем обработку текста)

def dictionary_processing(text, dictionary): # обработка текста по словарю

    import re # модуль регулярных выражений

    for key in dictionary: # обрабатываем каждую замену из словаря
        text = re.sub(key, dictionary[key], text) # меняем найденые значения

    return text

def Windows_msg(Name_app = "Уведомление", title = "Заголовок", msg = "Сообщение", duration = "short", icon = "", launch = ""): # сообщение Windows

    from winotify import Notification, audio # библиотека уведомлений в Windows

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

    time.sleep(randomN) # остановка на n секунд

def error(e = "Ошибка!"): # в случае ошибки пытаеться 10 повторить выполнение программы (имя ошибки)

    global err # счётчик ошибок (для чтения вне функции)

    print("Ошибка" , err, ":", e)

    if err < 11: # если ошибок меньше задонного числа

        err += 1 # добавляем значение к счётчику ошибок

        try: # попытаться сделать паузу

            Sleep(int(parameters["error_time"][0]), int(parameters["error_time"][1])) # остановка на случайное от n до m секунд

        except:
            Message("Проверте правильность записи параметра: " + "error_time" + "\"\nИли удалите файл, новый будет создан автоматически.", 8) # сообщение, поверх всех окон и с автоматическим закрытием
            exit() # выходим из програмы

    else:
        Windows_msg(Name_app = "Уведомление с форума ASCON", title = "Отслеживание сообщений прекращено!", msg = "Последняя ошибка: " + "\"" + str(e) + "\"", duration = "short", icon = icon, launch = "") # сообщение Windows
        exit() # выходим из програмы

#-------------------------------------------------------------------------------

ASCON_message = "" # сообщение для сравнения
err = 0 # счётчик ошибок

DoubleExe() # проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

Txt_file() # считываем значения из txt файла

while 1: # цикл обработки сообщений

    try: # попытаться выполнить программу

        ASCON() # уведомление от ASCONa

        err = 0 # сбрасываем счётчик ошибок

        if int(parameters["update_msg"][0]) < 20: # если нижний порог меньше 20 сек присвоить ему 20 сек (что бы не DDosить)
            parameters["update_msg"][0] = 20 # 20 сек нижний порог

        if int(parameters["update_msg"][1]) < 40: # если верхний порог меньше 40 сек присвоить ему 40 сек (что бы не DDosить)
            parameters["update_msg"][1] = 40 # 40 сек верхний порог

        Sleep(int(parameters["update_msg"][0]), int(parameters["update_msg"][1])) # остановка на случайное от n до m секунд

    except Exception as e: # ловим любые ошибки

        error(e) # в случае ошибки пытаеться 10 повторить выполнение программы (имя ошибки)