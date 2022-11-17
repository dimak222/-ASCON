#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Каширских Дмитрий
#
# Created:     22.09.2022
# Copyright:   (c) Каширских Дмитрий 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------


icon = r"C:\Users\Каширских Дмитрий\Desktop\Дмитрий\ГОСТ\Прочее\Макросы\Уведомление с форума ASCON\cat.ico" # иконка в уведомлении (полный путь к иконке)

def Windows_msg(Name_app = "Уведомление", title = "Заголовок", msg = "Сообщение", duration = "short", icon = "", launch = ""): # сообщение Windows

    from winotify import Notification, audio

    toast = Notification(app_id = Name_app, # название программы
                         title = title, # заголовок
                         msg = msg, # сообщение
                         duration = duration, # время отображения ("short" или "long")
                         icon = icon, # полный путь к иконке
                         launch = launch) # что открывать при нажатии на уведомление

    toast.set_audio(audio.Default, loop = False) # звук сообщения

    toast.add_actions(label = "Ссылка", launch = "https://github.com/versa-syahptr/winotify/") # кнопка в сообщении

    toast.add_actions(label = "Завершить работу", launch = print("Должен был завершить!")) # кнопка в сообщении

    toast.show() # запустить

Windows_msg(Name_app = "Уведомление с форума ASCON", title = "🆕 Макрос ''Уведомления о новых сообщениях на форуме''", msg = "Вышла новая версия программы: Уведомление с форума ASCON!", duration = "short", icon = icon, launch = "")