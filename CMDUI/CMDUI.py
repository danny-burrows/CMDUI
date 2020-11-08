from CMDUI.console.consolemanager import ConsoleManager
from CMDUI.components import Frame, Widget


class CMDUI(Frame):

    
    def __init__(self):
        self.console_manager = ConsoleManager(
            on_move=self.on_mouse_move, 
            on_click=self.on_mouse_click,
            on_resize=self.on_window_resize
        )

        self.cmdui_obj = self
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
