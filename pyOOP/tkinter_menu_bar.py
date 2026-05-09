from tkinter import *
from tkinter import messagebox # 메시지박스는 하위 모듈이라 *로 안 불러와짐. 따로 불러와야 한다!
# 명쾌한 답을 찾아서

def new_file():
    messagebox.showinfo("New", "새 파일을 만듭니다.")

def open_file():
    messagebox.showinfo("Open", "파일을 엽니다.")

def save_file():
    messagebox.showinfo("Save", "파일을 저장합니다.")

def exit_app():
    root.quit()

def show_about():
    messagebox.showinfo("About", "Tkinter Menu Example\n메뉴 예제 프로그램입니다.")

# 메인 윈도우 생성
root = Tk()
root.title("Tkinter 메뉴 예제")
root.geometry("500x300")
# 창 크기 조절 가능
root.resizable(True, False)

# 메뉴 바 생성
menu_bar = Menu(root)

# File 메뉴 생성
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# 메뉴 바에 File 메뉴 추가
menu_bar.add_cascade(label="File", menu=file_menu)

# Help 메뉴 생성
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)

# 메뉴 바에 Help 메뉴 추가
menu_bar.add_cascade(label="Help", menu=help_menu)

# 윈도우에 메뉴 바 연결
root.config(menu = menu_bar)

# 화면에 표시할 라벨
label = Label(root, text="상단 메뉴에서 File 또는 Help를 선택하시오.", font=("Arial", 14))
label.pack(expand=True)

# 이벤트 루프 실행
root.mainloop()