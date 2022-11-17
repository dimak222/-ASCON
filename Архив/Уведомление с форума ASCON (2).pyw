#-------------------------------------------------------------------------------
# Name:        Уведомления с форума ASCON
# Purpose:
#
# Author:      dimak222
#
# Created:     25.08.2022
# Copyright:   (c) dimak222 2022
# Licence:     No
#-------------------------------------------------------------------------------

title = "Уведомление с форума ASCON"

##from win32gui import *
##import pythoncom, win32con, sys, os

import urllib.request
import re
import time
from sys import exit # для выхода из приложения без ошибки

icon = r"C:\Users\Каширских Дмитрий\Desktop\Дмитрий\ГОСТ\Прочее\Макросы\Уведомление с форума ASCON\cat.ico" # иконка в уведомлении

def site_processing(site): # обработка сайта

    response = urllib.request.urlopen(site) # открываем сайт
    html = response.read().decode("utf-8") # считываем с него значения
    response.close() # закрываем модуль

    return html # возвращаем считаные строки сайта

def notification_message(mask, html): # поиск и вывод значений из html (маска поиска, текст где искать)

    z = 0 # номер поиска сообщения

    text = re.findall(mask, html)[z] # ищем название темы

    return text # возвращаем найденые значения

def dictionary_processing(text, dictionary): # обработка текста по словарю

    for key in dictionary: # обрабатываем каждую замену из словаря
        text = re.sub(key, dictionary[key], text) # меняем найденые значения

    return text

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
    message = notification_message("<div class=\"list_posts\">(.+)<\/div>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    launch = notification_message("\/ <a href=\"(.+)\" rel=\"nofollow\" title=\"Re:", html) # поиск и вывод пути к теме сообщения из html (маска поиска, текст где искать)

    topic = dictionary_processing(topic, dictionary) # обработка текста по словарю
    message = dictionary_processing(message, dictionary) # обработка текста по словарю

    try: # попытаться сравнить предыдущее сообщение

        if message != ASCON_message:

            print(topic + "От " + autor + ":" + message)
    ##            WindowsBalloonTip(topic + "От " + autor + ":" + message) # всплывающие сообщения в Windows (исчезает по истечении времени)

            Windows_msg(Name_app = title, title = topic, msg = "От " + autor + ": " + message, duration = "short", icon = icon, launch = launch) # сообщение Windows
            ASCON_message = message # прочитанное сообщение

        else:
            print("Новых сообщений нет!")

    except NameError: # если нет сообщения присвоить ему текст

        print("Первого сообщения нет!"),
        Windows_msg(Name_app = "Первое уведомление с форума ASCON", title = topic, msg = "От " + autor + ": " + message, duration = "short", icon = icon, launch = launch) # сообщение Windows
        ASCON_message = message # прочитанное сообщение

def mail(): # проверка почты

    html = site_processing("https://mailzone.macrooptica.ru/owa/?bO=1#path=/mail") # обработка сайта
    launch = notification_message("\"signinTxt\">(.+)<", html) # поиск и вывод пути к теме сообщения из html (маска поиска, текст где искать)

    if launch == "sign in":
        print("Требуеться войти!")
    print(launch)
    exit()

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

def Sleep(n, m): # остановка проверки на случайное от n до m секунд

    import random # импорт модуля

    randomN = random.randint(n, m) # случайное целое число от n до m

    time.sleep(randomN) # остановка проверки на n секунд

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

err = 0 # счётчик ошибок

while 1: # цыкл обработки сообщений

    try: # попытаться выполнить программу

        ##mail() # проверка почты

        ASCON() # уведомление от ASCONa

        err = 0 # сбрасываем счётчик ошибок

        Sleep(55, 100) # остановка проверки на случайное от n до m секунд

    except Exception as e: # ловим любые ошибки

        print("Ошибка" , err, ":", e)

        if err < 11: # если ошибок меньше задонного числа

            err += 1 # добавляем значение к счётчику ошибок

            time.sleep(5) # ждём n секунд

        else:
            Windows_msg(Name_app = "Уведомление с форума ASCON", title = "Отслеживание сообщений прекращено!", msg = "Последняя ошибка: " + "\"" + str(e) + "\"", duration = "short", icon = icon, launch = "") # сообщение Windows
            exit() # выходим из програамы