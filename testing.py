import CMDUI
cmdui = CMDUI.CMDUI()


but1 = CMDUI.CMDButton(cmdui, "   Button One   ")
but1.pack()

but2 = CMDUI.CMDButton(cmdui, "   Button Two   ")
but2.pack()

but3 = CMDUI.CMDButton(cmdui, "  Button Three  ")
but3.pack()

quitbut = CMDUI.CMDButton(cmdui, "      Quit      ")
quitbut.pack()

inp1 = CMDUI.CMDInput(cmdui, "   Input Text   ")
inp1.pack()
 
# pad = CMDUI.DrawPad(cmdui, 50, 6, 12, 30)
# pad.pack()

cmdui.mainloop()
input()
