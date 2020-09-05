# CMDUI

A GUI toolkit for CMD. This is a project to build a really easy-to-use graphical user interface toolkit entirely runnable in the windows console. The usage of this module is inspired by Tkinter as its ease of use makes it one of the easiest ways to create quick GUI's on the fly.

Eventually I aim to mirror the placement methods available in Tkinter such as Pack, Place, and Grid. I would also like to make a version of CMDUI for ANSI code driven terminals with the same easy to use style. 

## Current Issues

A means of toggling "Wrap text output on resize" really needs to be implemented in the C/C++ bindings for windows and subsequently ctypes or win32console. At the time of writing, this is doable with the GUI settings in CMD but I have found no way of accessing this feature through the bindings. (Or at least the ones I’ve seen in the documentation.)

Due to the aforementioned the GUI has a tendency to explode with artifacts all over the place when the window is resized. The temporary fix I have implemented for this is very unstable and can cause crashes occasionally but I am currently still looking into a better fix for this problem.
