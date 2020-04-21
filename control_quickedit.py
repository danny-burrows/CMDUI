# SOME GOD DID THIS...
# https://stackoverflow.com/questions/25943194/windows-cmd-console-stops-printing?answertab=votes#tab-top

# They didn't explain it but it basically just disables quickEdit mode in cmd.
# I was looking for a way to do this for hours!

import time
import random
import ctypes

class CMD_Object:

    def __init__(self):
        # win32 is an object which allows us to talk to the STDIO of cmd.exe.
        self.win32 = ctypes.windll.kernel32
        
        # hin is bascially just specific handle for 'STD_INPUT_HANDLE = -10'.
        self.hin = self.win32.GetStdHandle(-10)
        
        self.get_cmd_modes()
        

    def get_cmd_modes(self):
        mode = ctypes.c_int(0)
        self.win32.GetConsoleMode(self.hin, ctypes.byref(mode))
        #print(self.win32.GetConsoleWindow())

        #print(self.win32.GetConsoleCursorInfo(self.hin))


        # Standard mode (Assuming quickedit is already on).
        self.default_mode = mode.value
        
        # Disable Windows console(cmd.exe) quick edit mode.
        self.disable_quickedit_mode = self.default_mode & (~0x0040)

        # Disable test wrapping, to stop widget glitches!!
        self.disable_wrap_at_eol_output  = 0x0008


    def disable_quickedit(self):
        x = self.win32.SetConsoleMode(self.hin, self.disable_quickedit_mode)
        #print(x)

    def disable_wrap_at_eol(self):
        x = self.win32.SetConsoleMode(self.hin, self.disable_wrap_at_eol_output)
        print(x)

    #def enable_wrap_at_eol_output(self):
    #    self.win32.SetConsoleMode(self.hin, self.disable_wrap_at_eol_output)


    def enable_quickedit(self):
        self.win32.SetConsoleMode(self.hin, self.default_mode)


##
##BELLOW IS EXAMPLE USAGE
##
##cmd_obj = CMD_Object()
##
##
##running = True
##while running:
##    try:
##        cmd_obj.disable_quickedit()
##        r = random.randint(1, 100)
##        print('hello %s' % r)
##        time.sleep(1)
##    except (Exception, KeyboardInterrupt):
##        cmd_obj.enable_quickedit()
##        running = False

