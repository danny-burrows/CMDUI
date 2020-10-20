from CMDUI.console.consolemanager import ConsoleManager
from CMDUI.variables import StringVar, IntVar, DoubleVar, BooleanVar
from CMDUI.colors import get_color
import math


class CMDUI:

    
    def __init__(self):
        self.console_manager = ConsoleManager(on_move=self.on_mouse_move, 
                                              on_click=self.on_mouse_click,
                                              on_resize=self.on_window_resize)

        self.packed_widgets = []

        self.console_manager.init_console_output()

        self.window_width = self.console_manager.console_size[0]
        self.window_height = self.console_manager.console_size[1]


    def mainloop(self):
        try:
            self.console_manager.start()

            # (DISABLED FOR DEBUG)
            # self.console_manager.set_cursor_visable(False)

            # Initially building widgets!
            self.update_pack(undraw=False)

            self.console_manager.join()
        finally:
            self.console_manager.stop()


    def on_mouse_move(self, x, y):
        for widget in self.packed_widgets:
            if isinstance(widget, Widget):
                widget.check_hover(x, y)


    def on_mouse_click(self, x, y, button_state):
        if button_state == 1:
            for widget in self.packed_widgets:
                if isinstance(widget, Widget):
                    if widget.check_inside(x, y):
                        widget.on_press(x, y)
                    
        elif button_state == 0:
            for widget in self.packed_widgets:
                if isinstance(widget, Widget):
                    widget.on_release()


    def on_window_resize(self):
        self.window_width = self.console_manager.console_size[0]
        self.window_height = self.console_manager.console_size[1]
        self.update_pack(undraw=False)


    def pack_widget(self, widget):
        if widget in self.packed_widgets:
            return False
        self.packed_widgets.append(widget)


    def update_pack(self, undraw=False):
        # https://www.tcl.tk/man/tcl8.6/TkCmd/pack.htm

        # PASS #1

        width = max_width = self.window_width
        height = max_height = self.window_height

        for widget in self.packed_widgets:
            if widget.pack_options["side"] == "top" or widget.pack_options["side"] == "bottom":
                tmp = widget.width
                if tmp > max_width:
                    max_width = tmp
                height += widget.height
            else:
                tmp = widget.height
                if tmp > max_height:
                    max_height = tmp
                width += widget.width
        
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

        if max_width < self.window_width:
            max_width = self.window_width
        if max_height < self.window_height:
            max_height = self.window_height

        # If window size already changed then just stop and try again in a mo...
        if max_width == self.window_width or max_height == self.window_height:
            self.update_pack()
        
        # PASS #2

        cavity_x = 0
        cavity_y = 0

        cavity_width = self.window_width
        cavity_height = self.window_height

        for widget_num, widget in enumerate(self.packed_widgets):
            if widget.pack_options["side"] == "top" or widget.pack_options["side"] == "bottom":
                frame_width = cavity_width
                frame_height = widget.height
                if widget.pack_options["expand"]:
                    frame_height += self.y_expansion(widget_num, cavity_height)

                cavity_height -= frame_height
                if cavity_height < 0:
                    frame_height += cavity_height
                    cavity_height = 0

                frame_x = cavity_x
                if widget.pack_options["side"] == "top":
                    frame_y = cavity_y
                    cavity_y += frame_height
                else:
                    frame_y = cavity_y + cavity_height
            else:
                frame_height = cavity_height
                frame_width = widget.width
                if widget.pack_options["expand"]:
                    frame_width += self.x_expansion(widget_num, cavity_width)

                cavity_width -= frame_width
                if cavity_width < 0:
                    frame_width += cavity_width
                    cavity_width = 0

                frame_y = cavity_y
                if widget.pack_options["side"] == "top":
                    frame_x = cavity_x
                    cavity_x += frame_width
                else:
                    frame_x = cavity_x + cavity_width

            
            # Extra for CMDUI...
            import time
            import random
            x = ["a","c","d","1","2","3","4","5","6","7","8","9"]
            h = int(f"0x{str(random.choice(x))}f", 16)
            self.console_manager.color_area(frame_x, frame_y, frame_width, frame_height, h)
            time.sleep(0.1)
            if undraw:
                widget.undraw()

            if widget.pack_options["side"] == "top" or widget.pack_options["side"] == "bottom":
                widget.x = math.floor((frame_width / 2) - (widget.width / 2)) + frame_x if widget.width <= frame_width else frame_x 
                widget.y = math.floor((frame_height / 2) - (widget.height / 2)) + frame_y if widget.height <= frame_height else frame_y 
            else:
                widget.x = frame_x
                widget.y = math.floor((frame_height / 2) - (widget.height / 2)) + frame_y if widget.height <= frame_height else frame_y 

            widget.draw()


    def x_expansion(self, widget_num, cavity_width):
        minExpand = cavity_width
        num_expand = 0
        for widget_n in range(widget_num, len(self.packed_widgets)):
            widget = self.packed_widgets[widget_n]
            child_width = widget.width
            
            if widget.pack_options["side"] == "top" or widget.pack_options["side"] == "bottom":
                if num_expand:
                    cur_expand = (cavity_width - child_width) / num_expand
                    if cur_expand < minExpand:
                        minExpand = cur_expand
            else:
                cavity_width -= child_width
                if widget.pack_options["expand"]:
                    num_expand += 1
        
        if num_expand:
            cur_expand = cavity_width / num_expand
            if cur_expand < minExpand:
                minExpand = cur_expand
        
        return int(minExpand) if not (minExpand < 0) else 0


    def y_expansion(self, widget_num, cavity_height):
        minExpand = cavity_height
        num_expand = 0
        for widget_n in range(widget_num, len(self.packed_widgets)):
            widget = self.packed_widgets[widget_n]
            child_height = widget.height
            
            if widget.pack_options["side"] == "left" or widget.pack_options["side"] == "right":
                if num_expand:
                    cur_expand = (cavity_height - child_height) / num_expand
                    if cur_expand < minExpand:
                        minExpand = cur_expand
            else:
                cavity_height -= child_height
                if widget.pack_options["expand"]:
                    num_expand += 1
        
        if num_expand:
            cur_expand = cavity_height / num_expand
            if cur_expand < minExpand:
                minExpand = cur_expand
        
        return int(minExpand) if not (minExpand < 0) else 0


class Frame:


    def __init__(self, parent, x=0, y=0):
        if isinstance(parent, CMDUI):
            self.cmdui_obj = parent
        elif isinstance(parent, Frame):
            self.cmdui_obj = parent.cmdui_obj

        self.parent = parent

        self.frames = []

        self.packed_widgets = []
        
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

        self.pack_options = {
            "expand": False,
            "side": "top",
            "fill":"None"
        }


    def pack(self):
        if self not in self.cmdui_obj.packed_widgets:
            self.cmdui_obj.packed_widgets.append(self)


    def pack_widget(self, widget):
        if widget in self.packed_widgets:
            return False

        self.packed_widgets.append(widget)
        self.cmdui_obj.packed_widgets.append(widget)
        self.calc_frame_size()
    

    def calc_frame_size(self):
        self.height = sum(widget.height for widget in self.packed_widgets)
        try:
            self.width = max(widget.width for widget in self.packed_widgets)
        except ValueError:
            assert len(self.packed_widgets) == 0
        
        print(self.x, self.y, self.width, self.height)


    def draw(self):
        import random
        x = ["a","c","d","0","1","2","3","4","5","6","7","8","9"]
        h = int(f"0x{str(random.choice(x))}f", 16)
        print(h)
        self.paint_background(h)


    def undraw(self):
        pass


    def update_pack(self, undraw=False):
        # If expand=True...
        # height_of_widgets = sum(widget.height for widget in self.packed_widgets)
        # self.y = math.floor((self.height / 2) - (height_of_widgets / 2))

        widget_yoffset = 0

        for widget in self.packed_widgets:
            
            if undraw:
                widget.undraw()

            widget.x = math.floor((self.x + self.width / 2) - (widget.width / 2))
            widget.y = self.y + widget_yoffset

            if isinstance(widget, Frame):
                widget_yoffset = widget.update_pack()

            widget.draw()

            widget_yoffset += widget.height
        
        return widget_yoffset

    
    def paint_background(self, color):
        self.cmdui_obj.console_manager.color_area(
            self.x, 
            self.y, 
            self.width, 
            self.height, 
            color
        )
        


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

        self.pack_options = {
            "expand": False,
            "side": "top",
            "fill":"None"
        }

        
    def pack(self, expand=False, side="top", fill="none"):
        self.parent.pack_widget(self)

        assert isinstance(expand, bool), "Parameter 'expand' must be a boolean!"
        assert side in ("top", "bottom", "left", "right"), "Parameter 'side' must one of the following 'top', 'bottom', 'left', or 'right'."
        assert fill in ("none", "both", "x", "y"), "Parameter 'fill' must one of the following 'none', 'both', 'x', or 'y'."

        self.pack_options["expand"] = expand
        self.pack_options["side"] = side
        self.pack_options["fill"] = fill
    

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
            self.undraw()
            self.x = math.floor((self.cmdui_obj.window_width / 2) - (self.width / 2))
            self.draw()


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
            self.undraw()
            self.x = math.floor((self.cmdui_obj.window_width / 2) - (self.width / 2))
            self.draw()

      
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

        self.width = self.cmdui_obj.window_width
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
        self.width = self.cmdui_obj.window_width
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

