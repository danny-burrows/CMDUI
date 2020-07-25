import CMDUI
cmdui = CMDUI.CMDUI()


but1 = CMDUI.CMDButton(cmdui, "   Button One   ", 24, 6)
but1.pack()

input1 = CMDUI.CMDInput(cmdui, "   Input Some Text!   ")
input1.pack()


cmdui.mainloop()


input()
