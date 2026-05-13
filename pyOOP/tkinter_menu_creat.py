from tkinter import *

wnd = Tk()
wnd.geometry("1920x1080")
wnd.resizable(True, True)

MyMenu = Menu(wnd)
menu1 = Menu(MyMenu, tearoff = 0)
frame = Frame()
frame.pack()

wnd.mainloop()