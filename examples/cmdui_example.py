import sys
sys.path.insert(0,'..')

import CMDUI as CMD
import threading
import time


def counter():
    btn_txt.set("Stop")

    tt = time.time()
    while running:
        t = f"{time.time()-tt:.2f}"
        txt.set(t)
        time.sleep(0.01)
    
    btn_txt.set("Reset")


def stopwatch():
    if btn_txt.get() == "Reset":
        btn_txt.set("Start")
        txt.set("")
        return

    global running
    running = not running
    threading.Thread(target=counter).start()


running = False
root = CMD.CMDUI()

txt = CMD.StringVar()
btn_txt = CMD.StringVar()
btn_txt.set("Start")

# lab = CMD.Label(root, textvariable=txt)
# lab.pack()

# frm = CMD.Frame(root)
# frm.pack()

# but = CMD.Button(root, textvariable=btn_txt, command=stopwatch)
# but.pack()


lab = CMD.Label(root, textvariable=txt)
lab.pack(side="bottom")

but = CMD.Button(root, textvariable=btn_txt, command=stopwatch)
but.pack(side="right")

but = CMD.Button(root, textvariable=btn_txt, command=stopwatch)
but.pack()

but = CMD.Button(root, textvariable=btn_txt, command=stopwatch)
but.pack(side="left")


root.mainloop()