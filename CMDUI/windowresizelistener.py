from .stoppablethread import StoppableThread
import ctypes
import ctypes.wintypes


class ResizeListener(StoppableThread):


    def __init__(self, on_resize=None):
        super().__init__()

        if on_resize: self.on_resize = on_resize

        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self.ole32 = ctypes.OleDLL('ole32')


    def callback(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        self.on_resize()
        return self.user32.CallNextHookEx(None, hWinEventHook, event, hwnd)


    def run(self):
        EVENT_CONSOLE_LAYOUT = 0x4005
        WINEVENT_OUTOFCONTEXT = 0x0000

        self.ole32.CoInitialize(0)

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

        self.user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE

        self.hook = self.user32.SetWinEventHook(
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

        msg = ctypes.wintypes.MSG()
        while self.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0 and not self.stopped():
            self.user32.TranslateMessageW(msg)
            self.user32.DispatchMessageW(msg)

        self.user32.UnhookWinEvent(self.hook)
        self.ole32.CoUninitialize()


    def stop(self):
        WM_QUIT = 0x0012
        self.user32.PostThreadMessageW(self.ident, WM_QUIT, 0, 0)
        self._stop_event.set()


    def on_resize(self):
        pass