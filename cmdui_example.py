import CMDUI as CMD
import threading
import time

cmdui = CMD.CMDUI()

txt = CMD.StringVar()
btn_txt = CMD.StringVar()
btn_txt.set("Start")

running = False


def counter():
    btn_txt.set("Stop")

    tt = time.time()
    while running:
        t = "%.2f" % (time.time() - tt)
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


lab = CMD.Label(cmdui, textvariable=txt)
lab.pack()

but = CMD.Button(cmdui, textvariable=btn_txt, command=stopwatch)
but.pack()

cmdui.mainloop()