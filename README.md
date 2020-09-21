<div>
  <img height=150 src="https://i.imgur.com/UebexHA.gif">
</div>

## What is it?
This is a project to build an easy-to-use GUI toolkit using just the windows console. The usage of this module is inspired by Tkinter as its ease of use makes it one of the fastest ways to create GUIs on the fly.

Eventually I aim to mirror the placement methods available in Tkinter such as Pack, Place, and Grid. I would also like to make a version of CMDUI for ANSI code driven terminals in the same easy-to-use style, although in the meantime CMDUI is only runnable in the windows console (or CMD). 

## Installation
Clone the repo, download as a zip file, or use the following command...
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

## Current Issues
Due to the way lines of text are wrapped in CMD the GUI had a tendency to explode with artifacts all over the place when the window is resized. The temporary fix I have implemented for this is very unstable and can cause crashes occasionally but I am currently still looking into a better fix for this problem.

A means of toggling "Wrap text output on resize" really needs to be implemented in the C/C++ bindings for windows and subsequently ctypes or win32console for this problem to be fixed completely.