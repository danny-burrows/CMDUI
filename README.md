<div>
  <img height=150 src="https://i.imgur.com/UebexHA.gif">
</div>

## What is it?
This is a project to build an easy-to-use GUI toolkit using just the windows console. The usage of this module is inspired by Tkinter as its ease of use makes it one of the fastest ways to create GUIs on the fly.

Eventually I aim to mirror the placement methods available in Tkinter such as Pack, Place, and Grid. I would also like to make a version of CMDUI for ANSI code driven terminals in the same easy-to-use style, although in the meantime CMDUI is only runnable in the windows console (or CMD). 

## Notes for 0.2.0 release
Thanks for checking out the project! CMDUI is still in very early development and this release has added a new pack algorithm. This algorithm has been a tricky one to implement and there are still a lot of bugs that need to be ironed out. Feel free to open an issue if you encounter any. I hope you enjoy. :-)

## Installation
CMDUI is now available on pip...
```sh
pip install CMDUI
```

## Example Usage - Stop Watch
A simple stopwatch UI. This example demonstrates the use of buttons, labels, and text variables.
```python
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
```
