import CMDUI as CMD
import threading
import time


def counter():
    btn_txt.set("Stop")

    tt = time.time()
    while running:
        lab_txt.set(f"{time.time()-tt:.2f}")
        time.sleep(0.01)
    
    btn_txt.set("Reset")


def stopwatch():
    if btn_txt.get() == "Reset":
        btn_txt.set("Start")
        lab_txt.set("")
        return

    global running
    running = not running
    threading.Thread(target=counter).start()


cmdui = CMD.CMDUI()
running = False

lab_txt = CMD.StringVar()
btn_txt = CMD.StringVar()
btn_txt.set("Start")

lab = CMD.Label(cmdui, textvariable=lab_txt)
lab.pack()

but = CMD.Button(cmdui, textvariable=btn_txt, command=stopwatch)
but.pack()

cmdui.mainloop()