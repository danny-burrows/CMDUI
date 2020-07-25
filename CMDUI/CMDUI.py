import os
import sys
import time
import win32gui
import threading
from pynput.mouse import Listener, Controller

from . import new_window_listener
from . import control_quickedit

from . import curser_position as cur
from . import color_console as cons


os.system("color a")
default_colors = cons.get_text_attr()
default_bg = default_colors & 0x0070
default_fg = default_colors & 0x0007

# CONSTS...

# Charicters
char_height = 16 # pixels
char_width = 8 # pixels

# CMD
x_offset = 8 # pixels (from left hand besel)
y_offset = 32 # pixels (including menu bar)

"""BOX CHARS
│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌
"""
##def scribble(x, y):
##    x1, y1, _, _ = get_window_position_and_size()
##
##    manual_correct_x = 1
##    manual_correct_y = 2
##
##    cur.move(((x - x1)//char_width)-manual_correct_x, ((y - y1)//char_height)-manual_correct_y)
##    print("X")



class CMDUI():


    def __init__(self):
        self.win_listener = new_window_listener.Resize_Listener(on_resize=self.on_window_resize)
        self.winpos_listener = new_window_listener.Position_Listener(on_move=self.on_window_move)
        self.mouse_listener = Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)

        self.widgets = []
        self.packed_widgets = []
        self.mouse_down = False
        self.window_width = self.win_listener.term_size[0]
        self.window_height = self.win_listener.term_size[1]


    def mainloop(self):
        os.system("cls && color a")
        cmd_obj = control_quickedit.CMD_Object()
        try:
            cmd_obj.disable_quickedit()

            # Initial building widgets!
            self.update_pack()


            # Starting all listeners!
            self.win_listener.start()
            self.winpos_listener.start()
            self.mouse_listener.start()
            self.mouse_listener.join()
        except (Exception, KeyboardInterrupt) as e:
            self.win_listener.stop()
            self.winpos_listener.stop()
            self.mouse_listener.stop()
            cmd_obj.enable_quickedit()
            os.system("color 7")
            raise e


    def on_move(self, x, y):
        # print("Mouse moved to ({0}, {1})".format(x, y))

        for widget in self.packed_widgets:
            widget.update_button(x, y)

        # if mouse_down:
        #     wid_han.pad.update_pad(x, y)



    def on_click(self, x, y, button, pressed):
        self.mouse_down = not self.mouse_down

        if pressed:
            # print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

            for widget in self.packed_widgets:
                if widget.is_clicked(x, y):
                    cur.move(0, 1)
                    print("Pressed", widget.text)


    def on_scroll(self, x, y, dx, dy):
        raise Exception("Quitting Program On Scroll!")
        # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


    def on_window_move(self, x, y):
        pass
        #print("MOVED:", x, y)


    def on_window_resize(self, w, h):
        self.update_pack()
        self.window_width = w
        self.window_height = h


    def update_pack(self):

        # Old method of calcing the size of window.
        #winx1, winy1, winx2, winy2 = get_window_position_and_size()
        #winw, winh = winx2-winx1, winy2-winy1
        #winw, winh = depixelize(winw-x_offset, winh-y_offset)

        total_space = sum((widget.height for widget in self.packed_widgets))
        start = (self.window_height // 2) - (total_space // 2)

        widget_yoffset = 0

        for _, widget in enumerate(self.packed_widgets):

            widget.undraw()

            widget.x = (self.window_width // 2) - (widget.width // 2)
            widget.y = start+widget_yoffset

            widget.draw()

            widget_yoffset += widget.height


class Widget:


    def __init__(self, cmdui_obj, x=0, y=0):

        cmdui_obj.widgets.append(self)
        self.cmdui_obj = cmdui_obj

        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.display = ""


    def draw(self):
        winx1, winy1, winx2, winy2 = get_window_position_and_size()

        winw, winh = winx2 - winx1, winy2 - winy1
        winw, winh = depixelize(winw-x_offset, winh-y_offset)


        y_coord = 0
        if self.y+self.height >= winh-3:
            y_coord = winh - (self.height+3)
        elif self.y <= 0:
            y_coord = 0
        else:
            y_coord = self.y

        for i in range(len(self.display)):
            x_coord = 0
            if self.x+self.width >= winw - 5:
                x_coord = winw - self.width - 5
            elif self.x <= 0:
                x_coord = 0
            else:
                x_coord = self.x


            cur.move(x_coord, y_coord+i)
            print(self.display[i])


    def undraw(self):
        winx1, winy1, winx2, winy2 = get_window_position_and_size()

        winw, winh = winx2 - winx1, winy2 - winy1
        winw, winh = depixelize(winw-x_offset, winh-y_offset)

        y_coord = 0
        if self.y+self.height >= winh-3:
            y_coord = winh - (self.height+3)
        elif self.y <= 0:
            y_coord = 0
        else:
            y_coord = self.y

        for i in range(len(self.display)):
            x_coord = 0
            if self.x+self.width >= winw - 5:
                x_coord = winw - self.width - 5
            elif self.x <= 0:
                x_coord = 0
            else:
                x_coord = self.x

            cur.move(x_coord, y_coord+i)
            print(" "*len(self.display[i]))


    def update_pack(self):

        self.undraw()

        winx1, winy1, winx2, winy2 = get_window_position_and_size()

        winw, winh = winx2-winx1, winy2-winy1
        winw, winh = depixelize(winw-x_offset, winh-y_offset)

        total_space = sum((widget.height for widget in self.packed_widgets))


        start = (winh // 2) - (total_space // 2)

        offfsssss = 0

        for _, widget in enumerate(self.packed_widgets):
            cur.move((winw // 2) - (widget.width // 2), start+offfsssss)

            #widget.undraw()

            widget.x = (winw // 2) - (widget.width // 2)
            widget.y = start+offfsssss

            widget.draw()

            offfsssss += widget.height

        """
        yy_offset = -(len(self.packed_widgets)/2)+0.5
        if len(self.packed_widgets) % 2 == 0:
            yy_offset -= 0.5
        yy_offset = int(yy_offset)


        yy_offset = -(len(self.packed_widgets)/2)+0.5
        if len(self.packed_widgets) % 2 == 0:
            yy_offset -= 0.5
        yy_offset = int(yy_offset)

        ###############################
        self.undraw()
        ###############################

        for i, widget in enumerate(self.packed_widgets):

            #widget.undraw()

            widget.x = (winw // 2) - (widget.width // 2)
            widget.y = ((winh // 2) - (widget.height // 2)) + ((yy_offset+i)*3)

            widget.draw()
        """

    def pack(self):
        if self not in self.cmdui_obj.packed_widgets:
            self.cmdui_obj.packed_widgets.append(self)


class CMDButton(Widget):

    def __init__(self, cmdui_obj, text, x=0, y=0):
        super().__init__(cmdui_obj, x=x, y=y)

        self.active = False

        self.x = x
        self.y = y
        self.width = len(text) + 6
        self.height = 3

        self.text = text

        self.display = self.generate_button(text)
        self.display_action = self.generate_action_button(text)


    def generate_button(self, text):
        top = "┌──" + "─"*len(text) + "──┐"
        middle = "│  " + text + "  │"
        bottom = "└──" + "─"*len(text) + "──┘"
        return (top, middle, bottom)


    def generate_action_button(self, text):
        top = "╔══" + "═"*len(text) + "══╗"
        middle = "║  " + text + "  ║"
        bottom = "╚══" + "═"*len(text) + "══╝"
        return (top, middle, bottom)

##    def undraw(self, winx1=0, winy1=0, winx2=0, winy2=0):
##        if not winx1+winy1+winx2+winy2:
##            winx1, winy1, winx2, winy2 = get_window_position_and_size()
##
##        winw, winh = winx2 - winx1, winy2 - winy1
##        winw, winh = depixelize(winw-x_offset, winh-y_offset)
##
##        y_coord = 0
##        if self.y+self.height >= winh-3:
##            y_coord = winh - (self.height+3)
##        elif self.y <= 0:
##            y_coord = 0
##        else:
##            y_coord = self.y
##
##        for i in range(len(self.display)):
##            x_coord = 0
##            if self.x+self.width >= winw - 5:
##                x_coord = winw - self.width - 5
##            elif self.x <= 0:
##                x_coord = 0
##            else:
##                x_coord = self.x
##
##            cur.move(x_coord, y_coord+i)
##            print(" "*len(self.display[i]))
##
##
##    def draw(self, winx1=0, winy1=0, winx2=0, winy2=0):
##        if not winx1+winy1+winx2+winy2:
##            winx1, winy1, winx2, winy2 = get_window_position_and_size()
##
##        winw, winh = winx2 - winx1, winy2 - winy1
##        winw, winh = depixelize(winw-x_offset, winh-y_offset)
##
##
##        y_coord = 0
##        if self.y+self.height >= winh-3:
##            y_coord = winh - (self.height+3)
##        elif self.y <= 0:
##            y_coord = 0
##        else:
##            y_coord = self.y
##
##        for i in range(len(self.display)):
##            x_coord = 0
##            if self.x+self.width >= winw - 5:
##                x_coord = winw - self.width - 5
##            elif self.x <= 0:
##                x_coord = 0
##            else:
##                x_coord = self.x
##
##
##            cur.move(x_coord, y_coord+i)
##            print(self.display[i])

    def draw_hover(self):
        self.display = self.generate_action_button(self.text)
        self.draw()

    def draw_pressed(self):
        sys.stdout.flush()
        cons.set_text_attr(cons.FOREGROUND_RED | default_bg |
                        cons.FOREGROUND_INTENSITY)

        self.display = self.generate_action_button(self.text)
        self.draw()

        sys.stdout.flush()
        cons.set_text_attr(default_fg | default_bg |
                        cons.FOREGROUND_INTENSITY)



    def update_button(self, x, y):
        if check_inside(x, y, self) and self.active == False:
            self.draw_hover()
            self.active = True
        elif not check_inside(x, y, self) and self.active == True:
            self.display = self.generate_button(self.text)
            self.draw()
            self.active = False

    def is_clicked(self, x, y):
        if check_inside(x, y, self):
            self.draw_pressed()
            time.sleep(0.05)
            self.draw_hover()
            return True
        else:
            return False


class CMDInput(Widget):

    def __init__(self, cmdui_obj, text, x=0, y=0):
        super().__init__(cmdui_obj, x=x, y=y)
        self.active = False

        self.x = x
        self.y = y
        self.width = len(text) + 6
        self.height = 3

        self.text = text

        self.display = self.generate_button(text)
        self.display_action = self.generate_action_button(text)


    def generate_button(self, text):
        top = "┌──" + "─"*len(text) + "──┐"
        middle = "│  " + text + "  │"
        bottom = "└──" + "─"*len(text) + "──┘"
        return (top, middle, bottom)


    def generate_action_button(self, text):
        top = "╔══" + "═"*len(text) + "══╗"
        middle = "║  " + text + "  ║"
        bottom = "╚══" + "═"*len(text) + "══╝"
        return (top, middle, bottom)

    def draw_hover(self):
        self.display = self.generate_action_button(self.text)
        self.draw()

    def draw_pressed(self):
        sys.stdout.flush()
        cons.set_text_attr(cons.FOREGROUND_RED | default_bg |
                        cons.FOREGROUND_INTENSITY)

        self.display = self.generate_action_button(self.text)
        self.draw()


        input_thread = threading.Thread(target=self.handle_input)
        input_thread.start()
        input_thread.join()

        sys.stdout.flush()
        cons.set_text_attr(default_fg | default_bg |
                        cons.FOREGROUND_INTENSITY)

    def handle_input(self):
        cur.move(self.x+1, self.y+1)
        user_input = input()

        cur.move(self.x+1, self.y+1)
        print(" "*len(user_input))

        cur.move(0, 0)
        print("User said:", user_input)


    def update_button(self, x, y):
        if check_inside(x, y, self) and self.active == False:
            self.draw_hover()
            self.active = True
        elif not check_inside(x, y, self) and self.active == True:
            self.display = self.generate_button(self.text)
            self.draw()
            self.active = False

    def is_clicked(self, x, y):
        if check_inside(x, y, self):
            self.draw_pressed()
            time.sleep(0.05)
            self.draw_hover()
            return True
        else:
            return False


class DrawPad(Widget):

    def __init__(self, x=0, y=0, h=1, w=1):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

        self.display = self.generate_pad()

    def generate_pad(self):
        pad = ["┌──" + "─"*(self.width-6) + "──┐\n"]

        for _ in range(self.height-2):
            pad.append("│  " + " "*(self.width-6) + "  │\n")

        pad.append("└──" + "─"*(self.width-6) + "──┘")
        return pad

    def draw(self):
        for i in range(len(self.display)):


            cur.move(self.x, self.y+i)
            print(self.display[i])

    def undraw(self):
        for i in reversed(range(len(self.display))):
            cur.move(self.x+len(self.display[i]), self.y+i)
            print("\b \b"*len(self.display[i]))

    def update_pad(self, x, y):
        if check_inside(x, y, self):
            x1, y1, _, _ = get_window_position_and_size()

            manual_correct_x = 1
            manual_correct_y = 2

            cur.move(((x - x1)//char_width)-manual_correct_x, ((y - y1)//char_height)-manual_correct_y)
            print("X")


# Apply the pixel offset (charictor dimensions in cmd) to two values...
def pixelize(x, y):
    return (x*char_width, y*char_height)

def depixelize(x, y):
    return (x//char_width, y//char_height)


# Return a tuple with the pixel origin.
def get_origin():
   x1, y1, _, _ = get_window_position_and_size()
   return (x1 + x_offset, y1 + y_offset)


def get_window_position_and_size(self):
    rect = win32gui.GetWindowRect(self.win_listener.hwnd) # x1, y1, x2, y2
    return rect


def check_inside_window(x, y):
   win_pos = get_window_position_and_size()
   if x > win_pos[0] and x < win_pos[2] and y > win_pos[1] and y < win_pos[3]:
      return True
   else:
      return False

def check_inside(x, y, obj):
    if not check_inside_window(x, y):
        return False

    pix_width, pix_height = pixelize(obj.width, obj.height)
    pix_x, pix_y = pixelize(obj.x, obj.y)
    ox, oy = get_origin()

    if x > (ox+pix_x) and x < (ox+pix_x+pix_width) and y > (oy+pix_y) and y < (oy+pix_y+pix_height):
        return True
    else:
        return False



##def enumHandler(hwnd, args):
##    pid, hwnds = args
##    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
##    if found_pid == pid and win32gui.IsWindowVisible(hwnd):
##        hwnds.append(hwnd)
##
##
##def find_windows_from_pid(pid):
##    hwnds = []
##    win32gui.EnumWindows(self.enumHandler, (pid, hwnds))
##    return hwnds
##
##
##def get_window_hwnd():
##        # Try to get window through current process parent...
##        # (Checking 'up' from current running python process for an above GUI/py process).
##        pid = os.getpid()
##        parent_pid = self.get_parent_pid(pid)
##        windows = find_windows_from_pid(parent_pid)
##
##
##        # Try to get window through CMD process id...
##        # (Searching 'down' from every GUI/cmd.exe process, for the current running python process).
##        if not len(windows):
##            cmd_processes = os.popen('for /f "tokens=2 delims=," %a in \
##                                    (\'tasklist /fi "imagename eq cmd.exe" /nh /fo:csv\') \
##                                    do echo parent=%~a && \
##                                    wmic process where (ParentProcessId=%~a) get Caption,ProcessId')
##
##            # General format of command response is (<> denote non-terminal)...
##            #
##            # <random padding>parent=<pid of cmd><random padding><pid of cmd_child_process>
##            # <random padding><pid of cmd_child_process><random padding>
##            #
##            # The above is looped depending on number of cmd processes and cmd_child_processes.
##            get_cmd_process_info = cmd_processes.read()
##
##            for word in get_cmd_process_info.split():
##                try:
##                    if int(word) == parent_pid:
##                        windows = find_windows_from_pid(current_terminal)
##                        break
##                except ValueError:
##                    if word[:7] == "parent=":
##                        current_terminal = int(word[7:])
##
##        # Check that we do have at least one window...
##        if not len(windows):
##            raise Exception("Couldn't attach self to CMD! (Try running from file and from CMD).")
##        elif len(windows) > 1:
##            raise Exception("Multiple windows detected?!")
##
##        return windows[0]


##def pack(button, yoffset=0):
##    winx1, winy1, winx2, winy2 = get_window_position_and_size()
##    winw, winh = winx2-winx1, winy2-winy1
##
##    winw, winh = depixelize(winw-x_offset, winh-y_offset)
##
##    button.undraw(winx1, winy1, winx2, winy2)
##
##
##    xx = (winw // 2) - (button.width // 2)
##    yy = ((winh // 2) - (button.height // 2)) + yoffset
##    button.x = xx
##    button.y = yy
##
##    button.draw(winx1, winy1, winx2, winy2)
##
##    #cur.move(0,0)
##    #print("X:", xx)
##    #cur.move(0,1)
##    #print("Y:", yy)









##class TestWidgetHandler():
##
##    def __init__(self):
##        pass
##
##wid_han = TestWidgetHandler()

""" MAIN FUNC NOW UNEEDED!
def main():
    os.system("cls && color a")

    # cur.move(27, 4)
    # print("Welcome to CMDUI")

    wid_han.but1 = CMDButton("   Button One   ", 24, 6)
    wid_han.but2 = CMDButton("   Button Two   ", 24, 9)
    wid_han.but3 = CMDButton("  Button Three  ", 0, 0)
    wid_han.quitbut = CMDButton("      Quit      ", 24, 15)

    wid_han.inp1 = CMDInput("   Input Text   ")

    wid_han.pad = DrawPad(50, 6, 12, 30)




    global win_listener
    win_listener = new_window_listener.Resize_Listener(on_resize=on_window_resize)
    winpos_listener = new_window_listener.Position_Listener(on_move=on_window_move)



    wid_han.but1.pack()
    wid_han.but2.pack()
    wid_han.but3.pack()
    wid_han.quitbut.pack()

    wid_han.inp1.pack()

    wid_han.pad.pack()


    #pad.draw()

    #but1.draw()
    #but2.draw()

    #but3.draw()
    #quitbut.draw()

    mouse = Controller()

    global mouse_down
    mouse_down = False


    try:

        #hwnd = win_listener.hwnd
        win_listener.start()
        winpos_listener.start()

        with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
            listener.join()

    except (Exception, KeyboardInterrupt) as e:
        win_listener.stop()
        listener.stop()
        winpos_listener.stop()
        raise e

"""


"""
cmd_obj = control_quickedit.CMD_Object()

try:
    cmd_obj.disable_quickedit()
    main()
except Exception as e:
    print(e)
    os.system("color 7")
    cmd_obj.enable_quickedit()


"""
