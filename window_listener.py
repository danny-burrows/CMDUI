import os
import time
import threading
import win32gui
import win32process


# Credit for stoppable thread...
# https://stackoverflow.com/questions/47912701/python-how-can-i-implement-a-stoppable-thread
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Listener(StoppableThread):


    def __init__(self, *args, **kwargs):

        self.hwnd = 0
        
        try:
            if kwargs["on_move"]:
                self.on_move = kwargs["on_move"]
                del kwargs["on_move"]
        except KeyError:
            pass
        try:
            if kwargs["on_resize"]:
                self.on_resize = kwargs["on_resize"]
                del kwargs["on_resize"]
        except KeyError:
            pass

        self.connect()
        
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        
        
    def run(self):
        window_stats = list(self.get_window_stats())
        while not self.stopped():
            time.sleep(0.01)
            new_window_stats = list(self.get_window_stats())
            
            if window_stats[0] != new_window_stats[0]:
                window_stats[0] = new_window_stats[0]
                self.on_move(new_window_stats[0][0], new_window_stats[0][1])

            if window_stats[1] != new_window_stats[1]:
                window_stats[1] = new_window_stats[1]
                self.on_resize(new_window_stats[1][0], new_window_stats[1][1])
                

    def get_window_stats(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        return ((x, y), (w, h))


    def print_window_stats(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        print("\nWindow %s:" % win32gui.GetWindowText(self.hwnd))
        print("Location: (%d, %d)" % (x, y), end="\t")
        print("    Size: (%d, %d)" % (w, h))


    def get_parent_pid(self, pid):
        try:
            npid = os.popen("wmic process where (processid="+str(pid)+") get parentprocessid")
            parent_pid = npid.read().split()[1]
            return int(parent_pid)
        except IndexError:
            return 0
        

    def enumHandler(self, hwnd, args):
        pid, hwnds = args
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid and win32gui.IsWindowVisible(hwnd):
            hwnds.append(hwnd)


    def find_windows_from_pid(self, pid):
        hwnds = []
        win32gui.EnumWindows(self.enumHandler, (pid, hwnds))
        return hwnds
    

    def connect(self):
        # Try to get window through current process parent...
        # (Checking 'up' from current running python process for an above GUI/py process).
        #print("Getting GUI PID from parent process...")
        pid = os.getpid()
        parent_pid = self.get_parent_pid(pid)
        windows = self.find_windows_from_pid(parent_pid)


        # Try to get window through CMD process id...
        # (Searching 'down' from every GUI/cmd.exe process, for the current running python process).
        if not len(windows):
            #print("Getting GUI PID from CMD processes...")
            cmd_processes = os.popen('for /f "tokens=2 delims=," %a in \
                                    (\'tasklist /fi "imagename eq cmd.exe" /nh /fo:csv\') \
                                    do echo parent=%~a && \
                                    wmic process where (ParentProcessId=%~a) get Caption,ProcessId')
            
            # General format of command response is (<> denote non-terminal)...
            #
            # <random padding>parent=<pid of cmd><random padding><pid of cmd_child_process>
            # <random padding><pid of cmd_child_process><random padding>
            #
            # The above is looped depending on number of cmd processes and cmd_child_processes.
            get_cmd_process_info = cmd_processes.read()
            
            for word in get_cmd_process_info.split():
                try:
                    #print("\t- Child PID:", int(word))
                    if int(word) == parent_pid:
                        #print("Found Terminal PID:", current_terminal)
                        windows = self.find_windows_from_pid(current_terminal)
                        break
                except ValueError:
                    if word[:7] == "parent=":
                        current_terminal = int(word[7:])
                        #print("Checking Terminal PID:", current_terminal)

        # Check that we do have at least one window...
        if not len(windows):
            raise Exception("Couldn't attach self to CMD! (Try running from file and from CMD).")
        elif len(windows) > 1:
            raise Exception("Multiple windows detected?!")

        #print("SUCCESS: Process bound to GUI!")
        self.hwnd = windows[0]


    def on_move(self, x, y):
        pass

    def on_resize(self, w, h):
        pass
    
    
""" DEMO CODE BELLOW
input("\nPress enter to begin demo...")
print("\nTry moving the window around!\n")


def on_move(x, y):
    print("Move:", x, y)


def on_resize(w, h):
    print("Resize:", w, h)



try:
    testthread = Listener(on_move=on_move, on_resize=on_resize)
    testthread.start()
    # testthread.join()
    while True:
        time.sleep(20)
    testthread.stop()
except KeyboardInterrupt:
    testthread.stop()
"""
