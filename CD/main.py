
from tkinter import *
from tkinter import ttk
from utils.taskwindow import TaskWindow

# entry point of the application
# create a ui window for checking tasks and setting sources 
# further actions arise from button clicks in that ui window

root = Tk()
treeview = TaskWindow(root)
root.mainloop()