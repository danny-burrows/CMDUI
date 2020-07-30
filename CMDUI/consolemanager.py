from .stoppablethread import StoppableThread
from .windowresizelistener import ResizeListener
import win32console
import pywintypes
import win32file
import win32con
import time


class ConsoleManager(StoppableThread):


    def __init__(self, on_move=None, on_click=None, on_scroll=None, on_resize=None):
        super().__init__()

        if on_move: self.on_move = on_move
        if on_click: self.on_click = on_click
        if on_scroll: self.on_scroll = on_scroll
        if on_resize: self.on_resize = on_resize

        self.window_resize_listener = ResizeListener(on_resize=self.on_window_resize)
        self.virtual_keys = self.get_virtual_keys()

        self.resize_num = 0


    def get_color(self):
        console_screen_info = self.console_output.GetConsoleScreenBufferInfo()
        return console_screen_info["Attributes"]


    def set_color(self, color):
        self.console_output.SetConsoleTextAttribute(color)

    
    def set_cursor_visable(self, visable):
        console_cursor_info = self.console_output.GetConsoleCursorInfo()
        self.console_output.SetConsoleCursorInfo(console_cursor_info[0], visable)


    def print(self, text):
        self.console_output.WriteConsole(f'{text}\n')


    def print_pos(self, x, y, text):
        pos = win32console.PyCOORDType(x, y)
        self.console_output.SetConsoleCursorPosition(pos)
        self.console_output.WriteConsole(f'{text}\n')

    
    def color_pos(self, x, y, color):
        pos = win32console.PyCOORDType(x, y)
        attr=self.console_output.ReadConsoleOutputAttribute(Length=1, ReadCoord=pos)[0]
        new_attr=(attr&~color)|win32console.BACKGROUND_BLUE
        self.console_output.WriteConsoleOutputAttribute((new_attr,), pos)


    def init_console_input(self):
        """Create a new console input buffer, disable quickedit mode and enable mouse and window input."""

        self.console_input = win32console.PyConsoleScreenBufferType(
            win32file.CreateFile(
                "CONIN$",
                win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ,
                None,
                win32con.OPEN_EXISTING,
                0, 
                0
            )
        )

        default_mode = self.console_input.GetConsoleMode()
        disable_quickedit_mode = default_mode & (~0x0040)
        self.console_input.SetConsoleMode(disable_quickedit_mode)
        self.console_input.SetConsoleMode(win32console.ENABLE_WINDOW_INPUT | win32console.ENABLE_MOUSE_INPUT)


    def init_console_output(self):
        """Create a new console output buffer and set it as the active screen buffer."""

        self.console_output = win32console.CreateConsoleScreenBuffer()


    def run(self):
        try:
            self.init_console_input()
            self.console_output.SetConsoleActiveScreenBuffer()
            
            self.window_resize_listener.start()

            self._event_loop()
        except Exception as e:
            self.window_resize_listener.stop()
            self.console_output.Close()
            raise e
            
        self.window_resize_listener.stop()
        self.console_output.Close()

        if self.free_console:
            win32console.FreeConsole()
    

    def _event_loop(self):  
        """Handles console input events.
        
        Some info on state and flags from a mouse perspective...

        Event Flags:
            0 = Button click OR button release.
            1 = Button not down OR button held pressed.
            2 = Button double click.

        Button State:
            0 = Release button.
            1 = Left mouse button.
            2 = Rightmost mouse button.
            3 = Middle mouse button (I think).
        
        """

        move_state_check = 0
        breakout=False

        while not breakout and not self.stopped():
        
            # Calling this block the console and can stop resize events from firing...
            # This is mitigated by the time.sleep at the end of the loop but not
            # a perfect fix as now a bunch of resize events pile up and have to be
            # processed after each loop and read input buffer.
            input_records = self.console_input.ReadConsoleInput(10) 
            
            for input_record in input_records:
                if input_record.EventType == win32console.KEY_EVENT and input_record.KeyDown:
                    if input_record.Char=='\0':
                        self.console_output.WriteConsole(
                            self.virtual_keys.get(
                                input_record.VirtualKeyCode,
                                f'VirtualKeyCode: {input_record.VirtualKeyCode}'
                            )
                        )
                    else:
                        self.console_output.WriteConsole(input_record.Char)
                    if input_record.VirtualKeyCode == win32con.VK_ESCAPE:
                        breakout=True
                        break
                elif input_record.EventType == win32console.MOUSE_EVENT:
                    pos = input_record.MousePosition

                    if input_record.EventFlags in (0, 2):  ## 0 indicates a button event (I think 2 means doubleclick)

                        if input_record.ButtonState != 0:   ## exclude button releases
                            self.on_click(pos.X, pos.Y, input_record.ButtonState, 1)
                            #self.color_flip_fun(pos)
                        else:
                            self.on_click(pos.X, pos.Y, input_record.ButtonState, 0)

                    elif input_record.EventFlags == 1:
                        xpos = (pos.X, pos.Y)
                        if xpos != move_state_check:
                            self.on_move(pos.X, pos.Y)
                        move_state_check = xpos

                    elif input_record.EventFlags == 4:
                        self.on_scroll(pos.X, pos.Y)

                else:
                    pass
                    #self.console_output.WriteConsole(str(input_record))
            time.sleep(0.01)

        
    def on_move(self, x, y):
        self.print(f'MOVE {x}, {y}')


    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == 1:
                self.print(f'L CLICK {x}, {y}')
            elif button == 2:
                self.print(f'R CLICK {x}, {y}')
            elif button == 3:
                self.print(f'BOTH CLICK {x}, {y}')
            elif button == 4:
                self.print(f'MIDDLE CLICK {x}, {y}')
        else:
            self.print(f'RELEASE {x}, {y}')


    def on_scroll(self, x, y):
        self.print(f'SCROLL {x}, {y}')

    
    def on_resize(self):
        pass

    
    def on_window_resize(self):
        # Buffer size to window size can cause crashes. :/ Need to fix.
        self.set_buffersize_to_windowsize()

        # The following two lines are here to help debug the resize/mouse event queue bug...
        self.resize_num += 1
        self.print_pos(0, 2, f'WIN RESIZE {self.resize_num}')

        self.on_resize()


    def set_buffersize_to_windowsize(self):
        buffinfo = self.console_output.GetConsoleScreenBufferInfo()
        windowinfo = buffinfo['Window']

        if windowinfo:
            sizex = windowinfo.Right - windowinfo.Left + 1
            sizey = windowinfo.Bottom - windowinfo.Top + 1

        try:
            self.console_output.SetConsoleScreenBufferSize(win32console.PyCOORDType(sizex, sizey))
        except pywintypes.error:
            pass


    def color_flip_fun(self, pos):
        """ Switch the foreground and background colors of the character that was clicked. """

        attr=self.console_output.ReadConsoleOutputAttribute(Length=1, ReadCoord=pos)[0]
        new_attr=attr
        if attr&win32console.FOREGROUND_BLUE:
            new_attr=(new_attr&~win32console.FOREGROUND_BLUE)|win32console.BACKGROUND_BLUE
        if attr&win32console.FOREGROUND_RED:
            new_attr=(new_attr&~win32console.FOREGROUND_RED)|win32console.BACKGROUND_RED
        if attr&win32console.FOREGROUND_GREEN:
            new_attr=(new_attr&~win32console.FOREGROUND_GREEN)|win32console.BACKGROUND_GREEN

        if attr&win32console.BACKGROUND_BLUE:
            new_attr=(new_attr&~win32console.BACKGROUND_BLUE)|win32console.FOREGROUND_BLUE
        if attr&win32console.BACKGROUND_RED:
            new_attr=(new_attr&~win32console.BACKGROUND_RED)|win32console.FOREGROUND_RED
        if attr&win32console.BACKGROUND_GREEN:
            new_attr=(new_attr&~win32console.BACKGROUND_GREEN)|win32console.FOREGROUND_GREEN
        self.console_output.WriteConsoleOutputAttribute((new_attr,), pos)


    def get_virtual_keys(self):
        consts = win32con.__dict__.items()
        vkeys = {v: k for k, v in consts if k.startswith('VK_')}
        return vkeys


    @property
    def console_size(self):
        buffinfo = self.console_output.GetConsoleScreenBufferInfo()
        windowinfo = buffinfo['Window']

        if windowinfo:
            sizex = windowinfo.Right - windowinfo.Left + 1
            sizey = windowinfo.Bottom - windowinfo.Top + 1
        
        return sizex, sizey


    @property
    def free_console(self):
        """Only free console if one was created successfully."""

        free_console=True
        try:
            win32console.AllocConsole()
        except Exception as exc:
            if exc.winerror != 5:
                raise
            free_console=False
        return free_console


# def on_click():
#     pass

# win = ConsoleManager(on_click=on_click)
# win.start()
# win.join()


# time.sleep(10)
# win.stop()

# print("FUN TIMES")