#-------------------------------------------------------------------------------
# Name:        module4
# Purpose:
#
# Author:      Каширских Дмитрий
#
# Created:     24.08.2022
# Copyright:   (c) Каширских Дмитрий 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__all__ = ['ToastNotifier']

# #############################################################################
# ########## Libraries #############
# ##################################
# standard library

import logging
import threading
from os import path
from time import sleep
from pkg_resources import Requirement
from pkg_resources import resource_filename
# 3rd party modules
from win32api import GetModuleHandle
from win32api import PostQuitMessage
from win32con import CW_USEDEFAULT
from win32con import IDI_APPLICATION
from win32con import IMAGE_ICON
from win32con import LR_DEFAULTSIZE
from win32con import LR_LOADFROMFILE
from win32con import WM_DESTROY
from win32con import WM_USER
from win32con import WS_OVERLAPPED
from win32con import WS_SYSMENU
from win32gui import CreateWindow
from win32gui import DestroyWindow
from win32gui import LoadIcon
from win32gui import LoadImage
from win32gui import NIF_ICON
from win32gui import NIF_INFO
from win32gui import NIF_MESSAGE
from win32gui import NIF_TIP
from win32gui import NIM_ADD
from win32gui import NIM_DELETE
from win32gui import NIM_MODIFY
from win32gui import RegisterClass
from win32gui import UnregisterClass
from win32gui import Shell_NotifyIcon
from win32gui import UpdateWindow
from win32gui import WNDCLASS
from win32gui import PumpMessages

# Magic constants
PARAM_DESTROY = 1028
PARAM_CLICKED = 1029

#-------------------------------------------------------------------------------

class ToastNotifier(object):

    """Create a Windows 10  toast notification.
    from: https://github.com/jithurjacob/Windows-10-Toast-Notifications
    """

    def __init__(self, application_name = None):

        """Initialize."""

        self.hwnd = None
        self.nid = None
        self._thread = None
        self.wc = None
        self.hicon = None
        self.application_name = application_name or "Уведомление Windows"

    @staticmethod
    def _decorator(func, callback = None, **kwargs):
        """
        :param func: callable to decorate
        :param callback: callable to run on mouse click within notification window
        :return: callable
        """
        main_kwargs = kwargs

        def inner(*args, **kwargs):

            kwargs.update({'callback': callback})

            for key, value in main_kwargs.items():
                kwargs.update({key: value})

            func(*args, **kwargs)

        return inner

    def _show_toast(self, title, msg, icon_path, duration, callback_on_click, **kwargs):

        """Notification settings.
        :title: notification title
        :msg: notification message
        :icon_path: path to the .ico file to custom notification
        :duration: delay in seconds before notification self-destruction
        """
##        message_map = {WM_DESTROY: self.on_destroy, }
        # Register the window class.
        if self.wc is None:
            self.wc = WNDCLASS()
            self.hinst = self.wc.hInstance = GetModuleHandle(None)
            self.wc.lpszClassName = str("PythonTaskbar")  # must be a string
##            self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
            self.wc.lpfnWndProc = self._decorator(self.wnd_proc, callback_on_click, **kwargs)  # could instead specify simple mapping

            try:
                self.classAtom = RegisterClass(self.wc)

            except Exception as e: # вывод ошибки
                logging.error("Какие-то проблемы с классом Atom ({})".format(e))

            style = WS_OVERLAPPED | WS_SYSMENU
            if self.hwnd is None:
                self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                                         0, 0, CW_USEDEFAULT,
                                         CW_USEDEFAULT,
                                         0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)

        # icon
        if self.hicon is None:

            if icon_path is not None:
                icon_path = path.realpath(icon_path)

            else:
                icon_path = resource_filename(Requirement.parse("win10toast"), "win10toast/data/python.ico")
            icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE

            try:
                self.hicon = LoadImage(self.hinst, icon_path,
                                       IMAGE_ICON, 0, 0, icon_flags)

            except Exception as e:
                logging.error("Какие-то проблемы с иконкой ({}): {}".format(icon_path, e))
                self.hicon = LoadIcon(0, IDI_APPLICATION)

        # Taskbar icon
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP

        if self.nid is None:
            self.nid = (self.hwnd, 0, flags, WM_USER + 20, self.hicon, self.application_name)
            Shell_NotifyIcon(NIM_ADD, self.nid)

        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                      WM_USER + 20,
                                      self.hicon, "Balloon Tooltip", msg, 200,
                                      title))

        PumpMessages()

        # take a rest then destroy
        if duration is not None:
            sleep(duration)
            DestroyWindow(self.hwnd)
            UnregisterClass(self.wc.lpszClassName, None)

        return None

    def show_toast(self, title = "Заголовок", msg = "Какое-то сообщение",
                   icon_path = None, duration = 5, threaded = False, callback_on_click = None, **kwargs):
        """Notification settings.
        :title: notification title
        :msg: notification message
        :icon_path: path to the .ico file to custom notification
        :duration: delay in seconds before notification self-destruction, None for no-self-destruction
        """
        if not threaded:
            self._show_toast(title, msg, icon_path, duration, callback_on_click, **kwargs)

        else:
            if self.notification_active():
                # We have an active notification, let is finish so we don't spam them
                return False

            self._thread = threading.Thread(target = self._show_toast, args = (title, msg, icon_path, duration, callback_on_click), **kwargs)
            self._thread.start()

        return True

    def notification_active(self):
        """See if we have an active notification showing"""
        if self._thread != None and self._thread.is_alive():
            # We have an active notification, let is finish we don't spam them
            return True
        return False

    def wnd_proc(self, hwnd, msg, wparam, lparam, **kwargs):
        """Messages handler method"""

        if lparam == PARAM_CLICKED:
            # callback goes here
            if kwargs.get('callback'):
                kwargs.pop('callback')(**kwargs)
            self.on_destroy(hwnd, msg, wparam, lparam)
        elif lparam == PARAM_DESTROY:
            self.on_destroy(hwnd, msg, wparam, lparam)

##    def __enter__(self):
##        return self
##
##    def __exit__(self, exc_type, exc_val, exc_tb):
##        self.destroy()
##
##    def destroy(self):
##        DestroyWindow(self.hwnd)
##        UnregisterClass(self.wc.lpszClassName, None)
##        self.hwnd = None
##        self.nid = None
##        self._thread = None
##        self.wc = None
##        self.hicon = None

    def on_destroy(self, hwnd, msg, wparam, lparam):
        """Clean after notification ended."""
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

        return None