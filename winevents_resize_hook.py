import sys
import time
import win32gui
import win32process
import ctypes
import ctypes.wintypes


def print_window_stats(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        
        #print("\nWindow %s:" % win32gui.GetWindowText(hwnd))
        #print("Location: (%d, %d)" % (x, y), end="\t")
        print("Size: (%d, %d)" % (w, h))
        print("x"*(w//16))


# This isnt what is says it is.... its acually event console layout
EVENT_SYSTEM_DIALOGSTART = 0x4005
WINEVENT_OUTOFCONTEXT = 0x0000

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32

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


class coords:
    x = 1000
    y = 1000


def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    length = user32.GetWindowTextLengthA(hwnd)
    buff = ctypes.create_string_buffer(length + 1)
    user32.GetWindowTextA(hwnd, buff, length + 1)
    #print(buff.value)
    print_window_stats(hwnd)


    win32 = ctypes.windll.kernel32
    hin = win32.GetStdHandle(-11)


    bufsize = ctypes.wintypes._COORD(1000, 1000) # rows, columns
    win32.SetConsoleScreenBufferSize(hin, bufsize)


WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_SYSTEM_DIALOGSTART,
    EVENT_SYSTEM_DIALOGSTART,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)
if hook == 0:
    print('SetWinEventHook failed')
    sys.exit(1)

msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
    user32.TranslateMessageW(msg)
    user32.DispatchMessageW(msg)

user32.UnhookWinEvent(hook)
ole32.CoUninitialize()

