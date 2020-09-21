class Variable:

    _default = ""

    def __init__(self, master=None, value=None):

        self.widgets = [master] if master else []
        self.value = value if value else self._default


    def set(self, value):
        self.value = value

        for widget in self.widgets:
            widget.undraw()
            widget.update_text(self.get())
            widget.draw()

    
    def get(self):
        return self.value


class StringVar(Variable):
    _default = ""

    def __init__(self, master=None, value=None):
        super().__init__(master, value)
      
    def get(self):
        return str(self.value)


class IntVar(Variable):
    _default = 0

    def __init__(self, master=None, value=None):
        super().__init__(master, value)

    def get(self):
        return int(self.value)


class DoubleVar(Variable):
    _default = 0.0

    def __init__(self, master=None, value=None):
        super().__init__(master, value)  

    def get(self):
        return float(self.value)


class BooleanVar(Variable):
    _default = False

    def __init__(self, master=None, value=None):
        super().__init__(master, value)

    def get(self):
        return bool(self.value)