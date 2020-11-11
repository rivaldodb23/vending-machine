#  Most code adopted from Codemy.com

from tkinter import *
from tkinter import ttk
import threading
import time
import sys
    
# Most class code adopted from https://www.semicolonworld.com/question/43088/how-do-you-run-your-own-code-alongside-tkinter-s-event-loop   
# Progress bar coded added by @author Rivaldo De Bruin 
class App(threading.Thread):
    
    root = None
    my_progress = None
    gui_set = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.title('Progress')
        self.root.geometry("310x50")
        self.my_progress = ttk.Progressbar(self.root, orient=HORIZONTAL, len=300, mode='determinate')
        self.my_progress.pack(pady=20)
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.gui_set = True
        self.root.mainloop()
    
    def update_bar(self, val):
        while (self.gui_set == False):
            time.sleep(0.1)

        time.sleep(0.01)
        self.my_progress['value'] = val
    
    def hide(self):
        while self.gui_set == False:
            time.sleep(0.001)
        time.sleep(0.001)
        self.root.withdraw()

    def show(self):
        while self.gui_set == False:
            time.sleep(0.001)
        time.sleep(0.001)
        self.root.deiconify()
    
    def stop(self):
        time.sleep(0.01)
        self.root.quit()
        return True

if __name__ == '__main__':
    app = App()
    app.update_bar(10)
    time.sleep(1)
    quit = app.stop()
    print("Quit = ", str(quit))