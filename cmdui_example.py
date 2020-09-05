import CMDUI

cmdui = CMDUI.CMDUI()

# menu = CMDUI.CMDMenu(cmdui)

# menuOpt = CMDUI.CMDMenuOption(menu, "File")
# menu.pack()

# menuOpt = CMDUI.CMDMenuOption(menu, "Edit")
# menu.pack()

# menuOpt = CMDUI.CMDMenuOption(menu, "Options")
# menu.pack()

# menuOpt = CMDUI.CMDMenuOption(menu, "Options")
# menu.pack()

but1 = CMDUI.CMDButton(cmdui, "   Button One   ")
but1.pack()

# but2 = CMDUI.CMDButton(cmdui, "Button Two")
# but2.pack()

# inp1 = CMDUI.CMDInput(cmdui, "   Text Input   ")
# inp1.pack()

cmdui.mainloop()
input()