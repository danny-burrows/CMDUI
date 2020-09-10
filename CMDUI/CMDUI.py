from .consolemanager import ConsoleManager


class CMDUI:

    
    def __init__(self):
        self.console_manager = ConsoleManager(on_move=self.on_mouse_move, 
                                              on_click=self.on_mouse_click,
                                              on_resize=self.on_window_resize)

        self.widgets = []
        self.packed_widgets = []

        self.console_manager.init_console_output()

        self.window_width = self.console_manager.console_size[0]
        self.window_height = self.console_manager.console_size[1]

        self.res_c = 0
    
    
    def mainloop(self):
        try:
            self.console_manager.start()

            # (DISABLED FOR DEBUG)
            #self.console_manager.cursor_visable(False)

            # Initially building widgets!
            self.initial_pack()

            self.console_manager.join()
        except (Exception, KeyboardInterrupt) as e:
            self.console_manager.stop()
            raise e


    def on_mouse_move(self, x, y):
        # self.console_manager.print_pos(0, 3, f'Mouse Moved {x}, {y}\t\t')
        for widget in self.packed_widgets:
            widget.update_widget(x, y)


    def on_mouse_click(self, x, y, button, pressed):
        # self.console_manager.print_pos(0, 2, f'Mouse Clicked {x}, {y} {button} {pressed}\t\t')
        if pressed == 1 and button == 1:
            for widget in self.packed_widgets:
                    if widget.is_clicked(x, y):
                        widget.draw_pressed()

        elif not pressed:
            # released buttons draw all normal
            # self.console_manager.print_pos(0, 8, f'Mouse Released {x}, {y}\t\t')

            self.update_pack()

            # for widget in self.packed_widgets:
            #     widget.draw_hover()
            #     pass


    def on_window_resize(self):
        self.window_width = self.console_manager.console_size[0]
        self.window_height = self.console_manager.console_size[1]
        
        # Updating pack twice prevents drawing gaps in ui.
        self.update_pack()
        self.update_pack()


    def initial_pack(self):
        widget_total_space = sum((widget.height for widget in self.packed_widgets))
        widgets_start = (self.window_height // 2) - (widget_total_space // 2)

        widget_yoffset = 0

        for widget in self.packed_widgets:
            widget.x = (self.window_width // 2) - (widget.width // 2)
            widget.y = widgets_start+widget_yoffset

            widget.draw()

            widget_yoffset += widget.height


    def update_pack(self):
        widget_total_space = sum((widget.height for widget in self.packed_widgets))
        widgets_start = (self.window_height // 2) - (widget_total_space // 2)

        widget_yoffset = 0

        for widget in self.packed_widgets:
            
            widget.undraw()

            widget.x = (self.window_width // 2) - (widget.width // 2)
            widget.y = widgets_start+widget_yoffset

            widget.draw()

            widget_yoffset += widget.height


class Widget:


    def __init__(self, cmdui_obj, x=0, y=0):
        cmdui_obj.widgets.append(self)
        self.cmdui_obj = cmdui_obj

        self.x = x
        self.y = y
        #self.width = 0
        #self.height = 0

        self.hovered = False
        self.active = False
        self.display = ""

    
    def pack(self):
        if self not in self.cmdui_obj.packed_widgets:
            self.cmdui_obj.packed_widgets.append(self)
    

    def draw(self):
        # winw, winh = self.cmdui_obj.window_width, self.cmdui_obj.window_height 

        x_coord = self.x if self.x > 0 else 0
        y_coord = self.y if self.y > 0 else 0

        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(x_coord, y_coord+i, self.display[i])


    def undraw(self):
        # winw, winh = self.cmdui_obj.window_width, self.cmdui_obj.window_height

        x_coord = self.x if self.x > 0 else 0
        y_coord = self.y if self.y > 0 else 0

        for i in range(len(self.display)):
            self.cmdui_obj.console_manager.print_pos(x_coord, y_coord+i, " "*len(self.display[i]))


    def check_inside(self, x, y, obj):
        if x >= obj.x and x < obj.x+obj.width and \
           y >= obj.y and y < obj.y+obj.height:
            return True
        else:
            return False


    def update_widget(self, x, y):
        if self.check_inside(x, y, self) and self.hovered == False:
            self.hovered = True
        elif not self.check_inside(x, y, self) and self.hovered == True:
            self.hovered = False


    def is_clicked(self, x, y):
        if self.check_inside(x, y, self):
            return True
        else:
            return False


    def draw_pressed(self):
        pass


class CMDLabel(Widget):


    def __init__(self, cmdui_obj, text, x=0, y=0):
        super().__init__(cmdui_obj)

        self.text = text

        self.display = self.generate_label(text)

        #self.width = len(self.display[0])
        #self.height = len(self.display)


    def generate_label(self, text):
        top = f'┌─{"─"*len(text)}─┐'
        mid = f'│ {    text     } │'
        btm = f'└─{"─"*len(text)}─┘'

        return (top, mid, btm)

    @property
    def width(self):
        return len(self.display[0])

    @property
    def height(self):
        return len(self.display)


class CMDButton(Widget):


    def __init__(self, cmdui_obj, text, x=0, y=0, command=None):
        super().__init__(cmdui_obj, x, y)

        self.text = text

        self.display = self.generate_button(text)
        self.display_active = self.generate_active_button(text)

        self.width = len(self.display[0])
        self.height = len(self.display)

        if command:
            self.command = command


    def command(self):
        pass


    def generate_button(self, text):
        top = f'┌─{"─"*len(text)}─┐'
        mid = f'│ {    text     } │'
        btm = f'└─{"─"*len(text)}─┘'

        return (top, mid, btm)


    def generate_active_button(self, text):
        top = f'╔═{"═"*len(text)}═╗'
        mid = f'║ {    text     } ║'
        btm = f'╚═{"═"*len(text)}═╝'

        return (top, mid, btm)


    def draw_hover(self):
        self.display = self.generate_active_button(self.text)
        self.draw()


    def draw_pressed(self):
        FOREGROUND_INTENSITY = 0x0008

        cur_color = self.cmdui_obj.console_manager.get_color()

        # Bitwise XOR using FOREGROUND_INTENSITY; Keeps the colour, inverts the intensity.
        self.cmdui_obj.console_manager.set_color(cur_color ^ FOREGROUND_INTENSITY)

        #self.display = self.generate_active_button(self.text)
        self.draw()

        self.cmdui_obj.console_manager.set_color(cur_color)


    def update_widget(self, x, y):
        if self.check_inside(x, y, self) and self.hovered == False:
            self.hovered = True
            self.draw_hover()
        elif not self.check_inside(x, y, self) and self.hovered == True:
            self.hovered = False
            self.display = self.generate_button(self.text)
            self.draw()

    
    def is_clicked(self, x, y):
        import time
        if self.check_inside(x, y, self):
            self.draw_pressed()
            self.command()
            return True
        else:
            return False


class CMDInput(Widget):

    
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
        FOREGROUND_INTENSITY = 0x0008

        cur_color = self.cmdui_obj.console_manager.get_color()

        # Bitwise XOR using FOREGROUND_INTENSITY; Keeps the colour, inverts the intensity.
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
        import time
        if self.check_inside(x, y, self):
            self.draw_pressed()
            #time.sleep(0.15)
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


class CMDMenu(Widget):


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


class CMDMenuOption:


    def __init__(self, cmdmenu_obj, text):

        self.text = text

        cmdmenu_obj.options.append(self)
