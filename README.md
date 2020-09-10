<div>
  <img height=150 src="https://i.imgur.com/UebexHA.gif">
</div>

A GUI toolkit for CMD. This is a project to build an easy-to-use GUI toolkit using just the windows console. The usage of this module is inspired by Tkinter as its ease of use makes it one of the fastest ways to create GUIs on the fly.

Eventually I aim to mirror the placement methods available in Tkinter such as Pack, Place, and Grid. I would also like to make a version of CMDUI for ANSI code driven terminals with the same easy to use style, although in the meantime CMDUI is only runnable in the windows console (or CMD). 

## Current Issues

Due to the way lines of text are wrapped in CMD the GUI had a tendency to explode with artifacts all over the place when the window is resized. The temporary fix I have implemented for this is very unstable and can cause crashes occasionally but I am currently still looking into a better fix for this problem.

A means of toggling "Wrap text output on resize" really needs to be implemented in the C/C++ bindings for windows and subsequently ctypes or win32console for this problem to be fixed completely.