import sys

sys.path.insert(0,'..')

import threading
import time

import CMDUI as CMD


def counter():
    btn_txt.set("Stop")

    tt = time.time()
    while running:
        t = f"{(time.time()-tt)**10:.2f}"
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

frm = CMD.Frame(root)
frm.pack(side="left")


lab = CMD.Label(frm, textvariable=txt)
lab.pack()

but = CMD.Button(frm, textvariable=btn_txt, command=stopwatch)
but.pack()

but = CMD.Button(frm, textvariable=btn_txt, command=stopwatch)
but.pack()

frm2 = CMD.Frame(root)
frm2.pack(side="right", expand=True)

but = CMD.Button(frm2, textvariable=btn_txt, command=stopwatch)
but.pack()

but = CMD.Button(frm2, textvariable=btn_txt, command=stopwatch)
but.pack()

root.mainloop()
