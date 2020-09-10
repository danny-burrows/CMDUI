import CMDUI as CMD

cmdui = CMD.CMDUI()

menu = CMD.CMDMenu(cmdui)

menuOpt = CMD.CMDMenuOption(menu, "File")

menuOpt = CMD.CMDMenuOption(menu, "Edit")
menu.pack()

import time
import threading

running = False


def tst():
    global running
    tt = time.time()

    but1.undraw()

    but1.text = "Stop"
    but1.display = but1.generate_button("Stop")
    
    while running:
        lab1.undraw()
        t = time.time() - tt
        lab1.display = lab1.generate_label(str(round(t, 2)))
        cmdui.update_pack()
        time.sleep(0.01)
    
    but1.undraw()
    but1.text = "Reset"
    but1.display = but1.generate_button("Reset")
    cmdui.update_pack()


def com2():

    if but1.text == "Reset":
        lab1.undraw()
        lab1.display = lab1.generate_label("")
        
        but1.undraw()
        but1.text = "Start"
        but1.display = but1.generate_button("Start")
        
        cmdui.update_pack()
        return

    global running
    running = not running
    threading.Thread(target=tst).start()

lab1 = CMD.CMDLabel(cmdui,  "")
lab1.pack()

but1 = CMD.CMDButton(cmdui, "Start", command=com2)
but1.pack()

# but2 = CMDUI.CMDButton(cmdui, "Button Two")
# but2.pack()

# inp1 = CMDUI.CMDInput(cmdui, "   Text Input   ")
# inp1.pack()

cmdui.mainloop()
input()