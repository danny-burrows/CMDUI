from .components import Widget


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