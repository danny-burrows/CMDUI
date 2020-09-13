class Variable:


    def __init__(self):
        self.widgets = []
        self.value = None


    def set(self, value):
        self.value = value

    
    def get(self):
        return self.value


class StringVar(Variable):


    def __init__(self):
        super().__init__()
        self.value = ""

    
    def set(self, value):
        self.value = str(value)

        for widget in self.widgets:
            widget.undraw()
            widget.update_text(value)
            widget.draw()
