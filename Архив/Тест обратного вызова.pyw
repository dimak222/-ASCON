#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Каширских Дмитрий
#
# Created:     25.10.2022
# Copyright:   (c) Каширских Дмитрий 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

title = "Тест обратного вызова"

import os
print(os.path.basename(__file__))

"""
this is an example how to implement the callback feature in winotify
"""
import os.path
import random
import string
import time
import sys

import winotify

# instantiate Notifier and Registry class
app_id = "winotify test"
app_path = os.path.abspath(__file__)

r = winotify.Registry(app_id, winotify.PY_EXE, app_path, force_override=True)
notifier = winotify.Notifier(r)


@notifier.register_callback
def do_somethin():
    print('yo hey')
    for x in range(3, 0, -1):
        print(f"toast in {x} secs")
        time.sleep(1)

    toast = notifier.create_notification("a new notification", "this is called from another thread",
                                         launch=quit_)
    toast.add_actions("Clear all")
    toast.show()


@notifier.register_callback(run_in_main_thread=True)  # register quit func
def quit_():
    # this wont work if called from another thread
    print('YESSSSSS')

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

    if n == 10:
        Message("Закрылось через " + str(n) + " сек=(") # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)
    else:
        Message("Закрылось!!!") # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)
    sys.exit()


@notifier.register_callback
def spam():
    for i in range(3):
        rand = ''.join(random.choice(string.ascii_letters) for _ in range(10))  # random toast body
        t = notifier.create_notification(f"spam motification {i}", rand)
        t.add_actions("clear all", clear)
        # t.add_actions("sys.exit", notifier.callback_to_url(sys.exit))
        t.show()
        time.sleep(1)

def main():
    # no need to specify app_id every time
    toast = notifier.create_notification("a notification", 'a notification test with callback',
                                         launch=do_somethin)
    # generic url still works
    toast.add_actions("Open Github", "https://github.com/versa-syahptr/winotify")
    toast.add_actions("Quit app", quit_)
    toast.add_actions("spam", spam)
    toast.show()

    print(toast.script)


@notifier.register_callback
def clear(): notifier.clear()


if __name__ == '__main__':
    notifier.start()
    main()

    def DoubleExe():# проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

        import subprocess # модуль вывода запущеных процессов
        from sys import exit # для выхода из приложения без ошибки

        CREATE_NO_WINDOW = 0x08000000 # отключённое консольное окно
        processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW).communicate()[0] # список всех процессов
        processes = processes.decode('cp866') # декодировка списка

        if str(processes).count(title[0:25]) > 2: # если найдено название программы (два процесса) с ограничением в 25 символов
            Message("Приложение уже запущено!") # сообщение, поверх всех окон и с автоматическим закрытием
            exit() # выходим из програмы

    DoubleExe() # проверка на уже запущеное приложение, с отключённым консольным окном "CREATE_NO_WINDOW"

    n = 0

    while True:
        notifier.update()
        time.sleep(1)
        n += 1
        if n == 10:
            quit_()
            print("Запущен quit_()")
        print("i'm running", n)