# This is all horrible... Like, the worst... but I need to understand
# winhooks and ctypes to clean it up and thats effort.

import os
import time
import threading
import win32gui
import win32process

from . import curser_position as cur


import sys
import time
import ctypes
import ctypes.wintypes


from ctypes import windll, create_string_buffer
import struct
import sys
import os


# Credit for stoppable thread...
# https://stackoverflow.com/questions/47912701/python-how-can-i-implement-a-stoppable-thread
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Resize_Listener(StoppableThread):


    def __init__(self, *args, **kwargs):


        self.win32 = ctypes.WinDLL('kernel32', use_last_error=True)
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self.ole32 = ctypes.OleDLL('ole32')

        self.hwnd = self.get_window_handle()
        self.term_size = self.get_terminal_size()

        try:
            if kwargs["on_resize"]:
                self.on_resize = kwargs["on_resize"]
                del kwargs["on_resize"]
        except KeyError:
            pass

        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()


    def callback(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):

        if self.term_size != self.get_terminal_size():
            self.term_size = self.get_terminal_size()
            self.on_resize(self.term_size[0], self.term_size[1])

            # For correcting window size...
            #hin = self.win32.GetStdHandle(-11)
            #bufsize = ctypes.wintypes._COORD(self.term_size[0], self.term_size[1])
            #self.win32.SetConsoleScreenBufferSize(hin, bufsize)



        # Supposidly needed but not sure how...
        return self.user32.CallNextHookEx(None, hWinEventHook, event, hwnd)


    def run(self):
        EVENT_CONSOLE_LAYOUT = 0x4005
        WINEVENT_OUTOFCONTEXT = 0x0000

        # user32 = ctypes.windll.user32
        # ole32 = ctypes.windll.ole32



        user32 = self.user32
        ole32 = self.ole32

        ole32.CoInitialize(0)

        WinEventProcType = ctypes.WINFUNCTYPE(
            None,
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.HWND,
            ctypes.wintypes.LONG,
            ctypes.wintypes.LONG,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD
        )


        WinEventProc = WinEventProcType(self.callback)

        user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE

        self.hook = user32.SetWinEventHook(
            EVENT_CONSOLE_LAYOUT,
            EVENT_CONSOLE_LAYOUT,
            0,
            WinEventProc,
            0,
            0,
            WINEVENT_OUTOFCONTEXT
        )

        if self.hook == 0:
            raise Exception('Couldn\'t hook window resize event! Reason: SetWinEventHook failed.')
            sys.exit(1)

        msg = ctypes.wintypes.MSG()

        # This function is blocking...
        user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)

        #user32.SetWindowsHookExW(EVENT_CONSOLE_LAYOUT, self.callback, 0, 0)


        # Scary old stuff...
        #while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0 and not self.stopped():
        #    user32.TranslateMessageW(msg)
        #    user32.DispatchMessageW(msg)

        user32.UnhookWinEvent(self.hook)
        ole32.CoUninitialize()


    def stop(self):
        WM_QUIT = 0x0012
        self.user32.PostThreadMessageW(self.ident, WM_QUIT, 0, 0)
        self._stop_event.set()


    def get_terminal_size(self):
        columns = lines = 0

        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(windll.kernel32.GetStdHandle(-11), csbi)
        if res:
            res = struct.unpack("hhhhHhhhhhh", csbi.raw)
            left, top, right, bottom = res[5:9]
            columns = right - left + 1
            lines = bottom - top + 1

        return columns, lines


    def get_window_handle(self):
        hwnd = self.win32.GetConsoleWindow()
        if not hwnd:
            raise Exception("Couldn't connect to Command Prompt!")
        else:
            return hwnd


    def on_resize(self, w, h):
        pass


class Position_Listener(StoppableThread):


    def __init__(self, *args, **kwargs):

        self.win32 = ctypes.WinDLL('kernel32', use_last_error=True)
        self.hwnd = self.get_window_handle()

        try:
            if kwargs["on_move"]:
                self.on_move = kwargs["on_move"]
                del kwargs["on_move"]
        except KeyError:
            pass

        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()


    def run(self):
        window_position = list(self.get_window_position())
        while not self.stopped():
            time.sleep(0.01)
            new_window_position = list(self.get_window_position())

            if window_position != new_window_position:
                window_position = new_window_position
                self.on_move(new_window_position[0], new_window_position[1])


    def get_window_position(self):
        x, y, _, _ = win32gui.GetWindowRect(self.hwnd)
        return (x, y)


    def get_window_handle(self):
        hwnd = self.win32.GetConsoleWindow()
        if not hwnd:
            raise Exception("Couldn't connect to Command Prompt!")
        else:
            return hwnd

    def on_move(self, x, y):
        pass
"""

input("\nPress enter to begin demo...")
print("\nTry moving the window around!\n")


def on_move(x, y):
    print("Move:", x, y)


def on_resize(w, h):
    print("Resize:", w, h)


try:
    testthread = Resize_Listener(on_resize=on_resize)
    testposthread = Position_Listener(on_move=on_move)
    testthread.start()
    testposthread.start()
    testthread.join()

    time.sleep(5)
    testthread.stop()
    time.sleep(10)
except KeyboardInterrupt:
    testthread.stop()
    time.sleep(10)
"""
