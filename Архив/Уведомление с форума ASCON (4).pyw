#-------------------------------------------------------------------------------
# Name:        Уведомления с форума ASCON
# version:     v0.3.2
#
# Author:      dimak222
#
# Created:     25.08.2022
# Copyright:   (c) dimak222 2022
# Licence:     No
#-------------------------------------------------------------------------------

title = "Уведомление с форума ASCON"

icon = r"C:\Users\Каширских Дмитрий\Desktop\Дмитрий\ГОСТ\Прочее\Макросы\Уведомление с форума ASCON\cat.ico" # иконка в уведомлении

from sys import exit # для выхода из приложения без ошибки

def DoubleExe():# проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

    import subprocess # модуль вывода запущеных процессов
    from sys import exit # для выхода из приложения без ошибки

    CREATE_NO_WINDOW = 0x08000000 # отключённое консольное окно
    processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW).communicate()[0] # список всех процессов
    processes = processes.decode('cp866') # декодировка списка

    if str(processes).find(title[0:25]) != -1: # если найдено название программы с ограничением в 25 символов
        message(0, "Приложение уже запущено!") # сообщение, поверх всех окон и с автоматическим закрытием
        exit() # выходим из програмы

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

    topic = dictionary_processing(topic, dictionary) # обработка текста по словарю
    msg = dictionary_processing(msg, dictionary) # обработка текста по словарю

    if ASCON_message != "": # попытаться сравнить предыдущее сообщение

        if msg != ASCON_message:

            print(topic + "От " + autor + ":" + msg)
    ##            WindowsBalloonTip(topic + "От " + autor + ":" + msg) # всплывающие сообщения в Windows (исчезает по истечении времени)

            Windows_msg(Name_app = title, title = topic, msg = "От " + autor + ": " + msg, duration = "short", icon = icon, launch = launch) # сообщение Windows
            ASCON_message = msg # прочитанное сообщение

        else:
            print("Новых сообщений нет!")

    else: # если нет сообщения присвоить ему текст

        print("Первого сообщения нет!"),
        Windows_msg(Name_app = "Первое уведомление с форума ASCON", title = topic, msg = "От " + autor + ": " + msg, duration = "short", icon = icon, launch = launch) # сообщение Windows
        ASCON_message = msg # прочитанное сообщение

def Txt_file(): # считывание с txt файла

    import os # работа с файовой системой
    from sys import exit # для выхода из приложения без ошибки

    name_txt_file = title + ".txt" # название текстового файла

    if os.path.exists(name_txt_file): # если есть текстовый файл использовать его
        try:

            txt_file = open(name_txt_file, encoding = "utf-8") # открываем файл с кодировкой
            lines = txt_file.readlines() # считываем весь файл
            txt_file.close() # закрываем файл

            if lines == []: # если в файле нет записи, вписываем в файл опции для редактирования и инструкцию по использованию
                to_create_txt_file(name_txt_file) # создать txt файл с записью в него значений (путь к txt файлу)
            else:
                text_processing(lines, name_txt_file) # обработка текста (строки текста, путь к файлу)

        except SystemExit: # обрабатываем ошибку, если был использован "exit()"
            exit() # остановить программу

        except:
            message(8, "Проверте txt файл: \"" + name_txt_file + "\"\nИли удалите файл, новый будет создан автоматически.") # сообщение, поверх всех окон и с автоматическим закрытием
            exit() # остановить программу

    else: # использовать файл рядом с программой
        to_create_txt_file(name_txt_file) # создать txt файл с записью в него значений (путь к txt файлу)

def text_processing(lines, Path): # обработка текста (строки текста, путь к файлу)

    import os # работа с файовой системой
    from sys import exit # для выхода из приложения без ошибки

    global dictionary # словарь с путями перемещения (что перемещаем : куда перемещаем)

    try: # попытаться обработать значения в txt файле

        lines_clean = clearing_the_list(lines) # очистка списка строк от "#"

        if lines_clean == []: # если txt файл незаполнен выдать сообщение
            message(0, "Заполните txt файл!") # сообщение, поверх всех окон и с автоматическим закрытием
            exit() # остановить программу

        for line in lines_clean: # для каждой строки производим обработку
            Paths = line.split("=") # делим по "="
            try:
                Paths[0] = Paths[0].strip().strip('"') # убираем пробелы и "..." (кавычки) по бокам
                Paths[1] = Paths[1].strip().strip('"') # убираем пробелы и "..." (кавычки) по бокам

                dictionary[os.path.join(Paths[0])] = os.path.join(Paths[1], os.path.basename(Paths[0])) # добавляем в словарь пути перемещения (что перемещаем : куда перемещаем + название файла)

            except:
                pass

    except SystemExit: # обрабатываем ошибку, если был использован "exit()"
        exit() # остановить программу

    except:
        if askyesno("Проверте в txt файле правильность значения: \"" + parameter[0] + "\"\nИли удалите файл, новый будет создан автоматически." + "\nОткрыть файл для редактирования?"): # вопросительное сообщение, поверх всех окон
            os.startfile(Path) # открываем файл
        exit() # остановить программу

def to_create_txt_file(Path): # создать txt файл с записью в него значений (путь к txt файлу)

    import os # работа с файовой системой
    from sys import exit # для выхода из приложения без ошибки

    txt_file = open(Path, "w+") # открываем файл записи (w+), для чтения (r), (невидимый режим)

    txt = """# Полный путь копируемого файла (или имя файла с расширением) = Путь куда копировать
# "cat.ico" = "C:\\Users\\Cat\\Desktop"
# "C:\\cat.ico" = "C:\\Users\\Cat\\Desktop"
# C:\\cat.ico = C:\\Users\\Cat\\Desktop
#-------------------------------------------------------------------------------""" # текст записываемый в .txt файл

    txt_file.write(txt) # записываем текст в файл
    txt_file.close() # закрываем файл

    os.startfile(Path) # открываем файл в системе
    message(0, "Создан txt файл: \"" + Path + "\"\nВведите необходимые значения!") # сообщение с названием файла
    exit() # выходим

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

    randomN = random.randint(n, m) # случайное целое число от n до m

    time.sleep(randomN) # остановка на n секунд

#-------------------------------------------------------------------------------
# старая версия всплывающего сообщения

##from win32gui import *
##import pythoncom, win32con, sys, os

class WindowsBalloonTip: # всплывающие сообщения в Windows (исчезает по истечении времени)

    def __init__(self, title, msg):

        message_map = {win32con.WM_DESTROY: self.OnDestroy}
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map
        try:
            classAtom = RegisterClass(wc)
        except:
            pass
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join(sys.path[0], "cat.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
        	hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
        	hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "Уведомление о новых сообщениях")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20, hicon, "Balloon tooltip", msg, 200, title))
        time.sleep(10) # время до исчезновения сообщения)
        DestroyWindow(self.hwnd)
        UnregisterClass(classAtom, hinst)
    def OnDestroy(self, hwnd, title, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

#-------------------------------------------------------------------------------

ASCON_message = "" # сообщение для сравнения
err = 0 # счётчик ошибок

##DoubleExe() # проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

while 1: # цыкл обработки сообщений

    try: # попытаться выполнить программу

        ASCON() # уведомление от ASCONa

        err = 0 # сбрасываем счётчик ошибок

        Sleep(55, 100) # остановка на случайное от n до m секунд

    except Exception as e: # ловим любые ошибки

        print("Ошибка" , err, ":", e)

        if err < 11: # если ошибок меньше задонного числа

            err += 1 # добавляем значение к счётчику ошибок

            Sleep(5, 10) # остановка на случайное от n до m секунд

        else:
            Windows_msg(Name_app = "Уведомление с форума ASCON", title = "Отслеживание сообщений прекращено!", msg = "Последняя ошибка: " + "\"" + str(e) + "\"", duration = "short", icon = icon, launch = "") # сообщение Windows
            exit() # выходим из програмы