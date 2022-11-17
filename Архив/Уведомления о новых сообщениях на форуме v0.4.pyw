#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://vk.com/topic-152266438_36613341
# http://forum.ascon.ru/index.php/topic,31043.msg247082.html


import pythoncom, urllib.request, re, time, traceback
from win32com.client import Dispatch, gencache
import tkinter as tk
import tkinter.messagebox as mb


# Словарь замен
dictionary = {r"&nbsp;":" ",
            r"&quot;":'"',
			r"&amp;":"&",
			r'\<blockquote class=[^\>]+\>':'\n"',
			r'\<br\>\</blockquote\>':'"\n',
            r"</a></cite>" : " ",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/smiley.gif\" alt=\"&#58;&#41;\" title=\"Smiley\" class=\"smiley\">":":-)",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/wink.gif\" alt=\";&#41;\" title=\"Wink\" class=\"smiley\">":";-)",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/shocked.gif\" alt=\"&#58;o\" title=\"Shocked\" class=\"smiley\">":"8-0",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/sad.gif\" alt=\"&#58;&#40;\" title=\"Sad\" class=\"smiley\">":":-(",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/blink.gif\" alt=\"8-&#41;\" title=\"\" class=\"smiley\">":"o_O",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/cry.gif\" alt=\"&#58;`&#40;\" title=\"Cry\" class=\"smiley\">":";-(",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/mad.gif\" alt=\"&gt;&#58;&#40;\" title=\"Mad\" class=\"smiley\">":":-X",
			r"<img src=\"https://forum.ascon.ru/Smileys/fugue/shuffle.gif\" alt=\"&#58;shu&#58;\" title=\"Shuffle\" class=\"smiley\">":":-1|",

            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/angel.gif\" alt=\"&#58;angel&#58;\" title=\"angel\" class=\"smiley\">":"😇",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/rolleyes.gif\" alt=\"&#58;&#58;&#41;\" title=\"Roll Eyes\" class=\"smiley\">":"🙄",

			r'(<[^>]+?>)':"",
            r"&gt;":">",
            r"&#39;": "'"}

# Подключим описание интерфейсов API7
kompas_api7_module = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
application = kompas_api7_module.IApplication(Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(kompas_api7_module.IApplication.CLSID, pythoncom.IID_IDispatch))

mess_0, n = "", 1
z,err = 0,0

while 1:
    try:

        response = urllib.request.urlopen('http://forum.ascon.ru/index.php?action=recent')
        html = response.read().decode("utf-8")
        response.close()

        autor = "От: " + re.findall("Последний ответ от <.+>\<a.+\"\>(.+)\<\/a\>", html)[z]
        topic = re.findall("rel=\"nofollow\" title=\"Re: (.+)\"", html)[z]
        message = re.findall("<div class=\"list_posts\">(.+)<\/div>", html)[z]

        for key in dictionary:
           message = re.sub(key, dictionary[key], message)
           topic = re.sub(key, dictionary[key], topic)

        if message != mess_0:
           application.MessageBoxEx(autor + "\n" + message, topic, 64)
           mess_0 = message
           n = 1

        else:
             if n < 6:
                n += 1
        time.sleep(10*n)

    except Exception as e:
        if err < 10:
            err+=1
            time.sleep(5)
        else:
            root = tk.Tk()															# создаём окно
            root.withdraw()															# скрываем его
            mb.showwarning("Отслеживание сообщений прекращено", traceback.format_exc())	# показываем окно с выводом ошибки
            root.destroy()
            break

