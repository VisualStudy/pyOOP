from tkinter import *

def printing():
    print("버튼이 눌렸다!")

def funny():
    a = entry.get()
    print(a)

root = Tk()
root.geometry("300x200")

label = Label(root, text="이것은 라벨이다")
label.pack()

button = Button(root, text="출력", command=printing)
button.pack()

entry = Entry(root)
entry.pack()

but = Button(root, text="엔트리출력", command=funny)
but.pack()

root.mainloop()