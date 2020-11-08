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


frame_one = CMD.Frame(root)
counter_label = CMD.Label(frame_one, textvariable=txt)
button_one = CMD.Button(frame_one, textvariable=btn_txt, command=stopwatch)
button_two = CMD.Button(frame_one, textvariable=btn_txt, command=stopwatch)

frame_one.pack(side="left")
counter_label.pack()
button_one.pack()
button_two.pack()


frame_two = CMD.Frame(root)
frame2_button_one = CMD.Button(frame_two, textvariable=btn_txt, command=stopwatch)
frame2_button_two = CMD.Button(frame_two, textvariable=btn_txt, command=stopwatch)

frame_two.pack(side="right", expand=True)
frame2_button_one.pack()
frame2_button_two.pack()


root.mainloop()
