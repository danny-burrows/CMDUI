import CMDUI

cmdui = CMDUI.CMDUI()

but1 = CMDUI.CMDButton(cmdui, "   Button One   ")
but1.pack()

but2 = CMDUI.CMDButton(cmdui, "Button Two")
but2.pack()

inp1 = CMDUI.CMDInput(cmdui, "   Text Input   ")
inp1.pack()
 
pad = CMDUI.DrawPad(cmdui, 50, 6, 12, 30)
pad.pack()

cmdui.mainloop()
input()