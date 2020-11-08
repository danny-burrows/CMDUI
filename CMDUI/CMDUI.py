import math
import random
import time

from CMDUI.colors import get_color
from CMDUI.console.consolemanager import ConsoleManager
from CMDUI.variables import BooleanVar, DoubleVar, IntVar, StringVar


class Frame:


    def __init__(self, parent, x=0, y=0, width=0, height=0):
        if isinstance(parent, CMDUI):
            self.cmdui_obj = parent
        elif isinstance(parent, Frame):
            self.cmdui_obj = parent.cmdui_obj

        self.parent = parent
        self.packed_items = []
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.expand = False
        self.side = "top"
        self.fill = "none"


    def pack(self, expand=False, side="top", fill="none"):
        assert isinstance(expand, bool), \
            "Parameter 'expand' must be a boolean!"
        assert side in ("top", "bottom", "left", "right"), \
            "Parameter 'side' must be one of the following 'top', 'bottom', 'left', or 'right'."
        assert fill in ("none", "both", "x", "y"), \
            "Parameter 'fill' must be one of the following 'none', 'both', 'x', or 'y'."

        if self in self.parent.packed_items:
            return False
        self.parent.packed_items.append(self)
        self.cmdui_obj.visable_widgets.append(self)
        
        self.expand = expand
        self.side = side
        self.fill = fill


    def draw(self):
        x = ["a","c","d","0","1","2","3","4","5","6","7","8","9"]
        h = int(f"0x{random.choice(x)}f", 16)
        self.paint_background(h)


    def undraw(self):
        pass

    
    def paint_background(self, color):
        self.cmdui_obj.console_manager.color_area(
            self.x, 
            self.y, 
            self.width, 
            self.height, 
            color
        )

    
    def update_pack(self, force_draw=False):
        # https://www.tcl.tk/man/tcl8.6/TkCmd/pack.htm

        # PASS #1

        width = max_width = 0
        height = max_height = 0

        for widget in self.packed_items:
            if widget.side == "top" or widget.side == "bottom":
                tmp = widget.width + width
                if tmp > max_width:
                    max_width = tmp
                height += widget.height
            else:
                tmp = widget.height + height
                if tmp > max_height:
                    max_height = tmp
                width += widget.width
        
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

        # Expand window or frame if required...
        if max_width > self.width:
            self.width = max_width
        if max_height > self.height:
            self.height = max_height

        # If window size already changed then just stop and try again in a mo...
        # if max_width != self.width or max_height != self.height:
        #     self.update_pack()
        
        # PASS #2

        cavity_x = self.x
        cavity_y = self.y

        cavity_width = self.width
        cavity_height = self.height

        for widget_num, widget in enumerate(self.packed_items):
            if widget.side == "top" or widget.side == "bottom":
                frame_width = cavity_width
                frame_height = widget.height
                if widget.expand:
                    frame_height += self.y_expansion(widget_num, cavity_height)

                cavity_height -= frame_height
                if cavity_height < 0:
                    frame_height += cavity_height
                    cavity_height = 0

                frame_x = cavity_x
                if widget.side == "top":
                    frame_y = cavity_y
                    cavity_y += frame_height
                else:
                    frame_y = cavity_y + cavity_height
            else:
                frame_height = cavity_height
                frame_width = widget.width
                if widget.expand:
                    frame_width += self.x_expansion(widget_num, cavity_width)

                cavity_width -= frame_width
                if cavity_width < 0:
                    frame_width += cavity_width
                    cavity_width = 0

                frame_y = cavity_y
                if widget.side == "left":
                    frame_x = cavity_x
                    cavity_x += frame_width
                else:
                    frame_x = cavity_x + cavity_width

            widget.pack_frame = [frame_x, frame_y, frame_width, frame_height]            
            
            # Extra for CMDUI...
            x = ["a","c","d","1","2","3","4","5","6","7","8","9"]
            h = int(f"0x{random.choice(x)}f", 16)
            self.cmdui_obj.console_manager.color_area(frame_x, frame_y, frame_width, frame_height, h)
            #time.sleep(0.7)
            
            new_wx = math.floor((frame_width / 2) - (widget.width / 2)) + frame_x if widget.width <= frame_width else frame_x 
            new_wy = math.floor((frame_height / 2) - (widget.height / 2)) + frame_y if widget.height <= frame_height else frame_y    

            if not force_draw and new_wx == widget.x and new_wy == widget.y:
                return

            widget.x = new_wx
            widget.y = new_wy
            
            widget.draw()
            if isinstance(widget, Frame):
                widget.update_pack(force_draw=True)


    def x_expansion(self, widget_num, cavity_width):
        minExpand = cavity_width
        num_expand = 0
        for widget_n in range(widget_num, len(self.packed_items)):
            widget = self.packed_items[widget_n]
            child_width = widget.width
            
            if widget.side == "top" or widget.side == "bottom":
                if num_expand:
                    cur_expand = (cavity_width - child_width) / num_expand
                    if cur_expand < minExpand:
                        minExpand = cur_expand
            else:
                cavity_width -= child_width
                if widget.expand:
                    num_expand += 1
        
        if num_expand:
            cur_expand = cavity_width / num_expand
            if cur_expand < minExpand:
                minExpand = cur_expand
        
        return int(minExpand) if not (minExpand < 0) else 0


    def y_expansion(self, widget_num, cavity_height):
        minExpand = cavity_height
        num_expand = 0
        for widget_n in range(widget_num, len(self.packed_items)):
            widget = self.packed_items[widget_n]
            child_height = widget.height
            
            if widget.side == "left" or widget.side == "right":
                if num_expand:
                    cur_expand = (cavity_height - child_height) / num_expand
                    if cur_expand < minExpand:
                        minExpand = cur_expand
            else:
                cavity_height -= child_height
                if widget.expand:
                    num_expand += 1
        
        if num_expand:
            cur_expand = cavity_height / num_expand
            if cur_expand < minExpand:
                minExpand = cur_expand
        
        return int(minExpand) if not (minExpand < 0) else 0


class CMDUI(Frame):

    
    def __init__(self):
        self.console_manager = ConsoleManager(
            on_move=self.on_mouse_move, 
            on_click=self.on_mouse_click,
            on_resize=self.on_window_resize
        )

        self.console_manager.init_console_output()
        
        super().__init__(
            self, 
            x=0, 
            y=0, 
            width=self.console_manager.console_size[0], 
            height=self.console_manager.console_size[1]
        )
        self.visable_widgets = []


    def mainloop(self):
        try:
            self.console_manager.start()

            # (DISABLED FOR DEBUG)
            # self.console_manager.set_cursor_visable(False)

            # Initially building widgets!
            self.update_pack()

            self.console_manager.join()
        finally:
            self.console_manager.stop()


    def on_mouse_move(self, x, y):
        for widget in self.visable_widgets:
            if isinstance(widget, Widget):
                widget.check_hover(x, y)


    def on_mouse_click(self, x, y, button_state):
        if button_state == 1:
            for widget in self.visable_widgets:
                if isinstance(widget, Widget):
                    if widget.check_inside(x, y):
                        widget.on_press(x, y)
                    
        elif button_state == 0:
            for widget in self.visable_widgets:
                if isinstance(widget, Widget):
                    widget.on_release()


    def on_window_resize(self):
        self.width = self.console_manager.console_size[0]
        self.height = self.console_manager.console_size[1]
        self.update_pack(force_draw=True)


class Widget:


    def __init__(self, parent, x=0, y=0):
        if isinstance(parent, CMDUI):
            self.cmdui_obj = parent
        elif isinstance(parent, Frame):
            self.cmdui_obj = parent.cmdui_obj

        self.parent = parent
        self.x = x
        self.y = y

        self.display = ""

        self.expand = False
        self.side = "top"
        self.fill = "none"
        self.pack_frame = [0, 0, 0, 0]


    def pack(self, expand=False, side="top", fill="none"):
        assert isinstance(expand, bool), \
            "Parameter 'expand' must be a boolean!"
        assert side in ("top", "bottom", "left", "right"), \
            "Parameter 'side' must be one of the following 'top', 'bottom', 'left', or 'right'."
        assert fill in ("none", "both", "x", "y"), \
            "Parameter 'fill' must be one of the following 'none', 'both', 'x', or 'y'."

        if self in self.parent.packed_items:
            return False
        self.parent.packed_items.append(self)
        self.cmdui_obj.visable_widgets.append(self)
        
        self.expand = expand
        self.side = side
        self.fill = fill
    

    def re_pack(self):

        # Need to check if the windows new position is too big for the current frame!
        if self.width > (self.pack_frame[2]-self.pack_frame[0]) or self.height > (self.pack_frame[3]-self.pack_frame[1]):
            self.cmdui_obj.update_pack(force_draw=True)
            return

        new_wx = math.floor((self.pack_frame[2] / 2) - (self.width / 2)) + self.pack_frame[0] if self.width <= self.pack_frame[2] else self.pack_frame[0] 
        new_wy = math.floor((self.pack_frame[3] / 2) - (self.height / 2)) + self.pack_frame[1] if self.height <= self.pack_frame[3] else self.pack_frame[1] 
        self.undraw()
        self.x = new_wx
        self.y = new_wy
        self.draw()


    def draw(self):
        x_coord = self.x if self.x > 0 else 0
        y_coord = self.y if self.y > 0 else 0

        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(x_coord, y_coord+i, self.display[i])


    def undraw(self):
        x_coord = self.x if self.x > 0 else 0
        y_coord = self.y if self.y > 0 else 0

        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(x_coord, y_coord+i, " "*len(self.display[i]))


    def check_inside(self, x, y):
        if x >= self.x and x < self.x+self.width and \
           y >= self.y and y < self.y+self.height:
            return True
        else:
            return False


    def check_hover(self, x, y):
        pass


    def on_press(self, x, y):
        pass


    def on_release(self):
        pass

    
    @property
    def width(self):
        return len(self.display[0])


    @property
    def height(self):
        return len(self.display)


class Label(Widget):


    def __init__(self, cmdui_obj, text="", textvariable=None, x=0, y=0):
        super().__init__(cmdui_obj, x, y)

        if textvariable:
            self.text = textvariable.get()
            textvariable.widgets.append(self)
        else:
            self.text = text

        self.display = self.generate_display()


    def update_text(self, text):
        pk_update_needed = True if len(self.text) != len(text) else False
        
        self.text = text
        self.display = self.generate_display()

        if pk_update_needed:
            self.re_pack()


    def generate_display(self):
        top = f'┌─{"─"*len(self.text)}─┐'
        mid = f'│ {    self.text     } │'
        btm = f'└─{"─"*len(self.text)}─┘'

        return (top, mid, btm)


class Button(Widget):


    def __init__(self, cmdui_obj, text="", textvariable=None, x=0, y=0, command=None):
        super().__init__(cmdui_obj, x, y)

        if textvariable:
            self.text = textvariable.get()
            textvariable.widgets.append(self)
        else:
            self.text = text

        if command:
            self.command = command
            
        self.display = self.generate_display()
        self.hovered = False
        self.pressed = False


    def command(self):
        pass


    def update_text(self, text):
        pk_update_needed = True if len(self.text) != len(text) else False

        self.text = text
        if self.hovered:
            self.display = self.generate_active_display()
        else:
            self.display = self.generate_display()

        if pk_update_needed:
            self.re_pack()

      
    def generate_display(self):
        top = f'┌─{"─"*len(self.text)}─┐'
        mid = f'│ {    self.text     } │'
        btm = f'└─{"─"*len(self.text)}─┘'
        return (top, mid, btm)


    def generate_active_display(self):
        top = f'╔═{"═"*len(self.text)}═╗'
        mid = f'║ {    self.text     } ║'
        btm = f'╚═{"═"*len(self.text)}═╝'
        return (top, mid, btm)


    def draw_hover(self):
        self.display = self.generate_active_display()
        self.draw()


    def draw_pressed(self):
        FOREGROUND_INTENSITY = 0x0008

        cur_color = self.cmdui_obj.console_manager.get_console_color_code()

        # Bitwise XOR using FOREGROUND_INTENSITY; Keeps the colour, inverts the intensity.
        select_color = cur_color ^ FOREGROUND_INTENSITY
        
        self.cmdui_obj.console_manager.color_area(
            self.x, 
            self.y, 
            self.width, 
            self.height, 
            select_color
        )


    def check_hover(self, x, y):
        if self.check_inside(x, y) and self.hovered == False:
            self.hovered = True
            self.draw_hover()
        elif not self.check_inside(x, y) and self.hovered == True:
            if not self.pressed:
                self.hovered = False
                self.display = self.generate_display()
                self.draw()


    def on_press(self, x, y):
        self.draw_pressed()
        self.pressed = True


    def on_release(self):
        if self.pressed:
            self.command()
            self.pressed = False


class Input(Widget):

    
    def __init__(self, cmdui_obj, text, x=0, y=0):
        super().__init__(cmdui_obj, x=x, y=y)

        self.text = text

        self.display = self.generate_input(text)
        self.display_active = self.generate_hovered_input(text)

        self.width = len(self.display[0])
        self.height = len(self.display)

    
    def generate_input(self, text):
        top = f'┌─{"─"*len(text)}─┐'
        mid = f'│ {    text     } │'
        btm = f'└─{"─"*len(text)}─┘'

        return (top, mid, btm)


    def generate_hovered_input(self, text):
        top = f'╔═{"═"*len(text)}═╗'
        mid = f'║ {    text     } ║'
        btm = f'╚═{"═"*len(text)}═╝'

        return (top, mid, btm)

    
    def generate_active_input(self, text):
        top = f'╔═{"═"*len(text)}═╗'
        mid = f'║ {" "*len(text)} ║'
        btm = f'╚═{"═"*len(text)}═╝'

        return (top, mid, btm)


    def draw_hover(self):
        self.display = self.generate_hovered_input(self.text)
        self.draw()


    def draw_pressed(self):
        cur_color = self.cmdui_obj.console_manager.get_console_color_code()

        # Bitwise XOR using FOREGROUND_INTENSITY; Keeps the colour, inverts the intensity.
        FOREGROUND_INTENSITY = 0x0008
        self.cmdui_obj.console_manager.set_color(cur_color ^ FOREGROUND_INTENSITY)

        self.draw()

        # Handle user input; currently needs rewrite.
        self.handle_input()

        self.cmdui_obj.console_manager.set_color(cur_color)

    
    def handle_input(self):
        # We can use the new console manager input buffer to fix the freezing with this!

        self.cmdui_obj.console_manager.print_pos(self.x+1, self.y+1, "")

        #cur.move(self.x+1, self.y+1)
        user_input = input()

        self.cmdui_obj.console_manager.print_pos(self.x+1, self.y+1, ' '*len(user_input))
        # self.cmdui_obj.console_manager.print_pos(0, 0, f'User said: {user_input}')


    def update_widget(self, x, y):
        if self.check_inside(x, y, self) and self.hovered == False:
            self.hovered = True
            self.draw_hover()
        elif not self.check_inside(x, y, self) and self.hovered == True:
            self.hovered = False
            self.display = self.generate_input(self.text)
            self.draw()

    
    def is_clicked(self, x, y):
        if self.check_inside(x, y, self):
            self.draw_pressed()
            #self.draw_hover()
            return True
        else:
            return False


class DrawPad(Widget):


    def __init__(self, cmdui_obj, x=0, y=0, h=1, w=1):
        super().__init__(cmdui_obj, x=x, y=y)
        
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
            self.cmdui_obj.console_manager.print_pos(self.x, self.y+i, self.display[i])


    def undraw(self):
        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(self.x+len(self.display[i]), self.y+i, " "*len(self.display[i]))


    def draw_pressed(self):
        pass


    def update_widget(self, x, y):
        if self.check_inside(x, y, self):
            self.cmdui_obj.console_manager.print_pos(x, y, "X")


class Menu(Widget):


    def __init__(self, cmdui_obj):
        super().__init__(cmdui_obj, x=0, y=0)

        self.width = self.cmdui_obj.main_frame.width
        self.height = 2
        
        self.options = []

        self.display = self.generate_menu()


    def generate_menu(self):
        btns = ''.join(f' {option.text} │' for option in self.options)
        btm = ''.join(f'─{"─"*len(option.text)}─┴' for option in self.options)

        if len(btns) < self.width:
            btm = f'{btm}{"─"*(self.width - len(btm))}'

        return (btns, btm)


    def draw(self):
        self.x = 0
        self.y = 0
        self.width = self.cmdui_obj.main_frame.width
        self.display = self.generate_menu()

        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(self.x, self.y+i, self.display[i])


    def undraw(self):
        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(0, self.y+i, " "*len(self.display[i]))


class MenuOption:


    def __init__(self, menu_obj, text):
        menu_obj.options.append(self)

        self.text = text
