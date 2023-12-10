from tkinter import *
from tkinter import ttk
import sqlite3

# root = Tk()
class App_admin():
    db = "database/luxurywheels.db"

    def __init__(self,root):
        self.first_root = root
        self.variable()
        self.colors()
        self.screen()
        self.screen_frame()
        self.login_screen()

        # root.mainloop()

    def variable(self):
        self.var_login = (StringVar())
        self.var_password = StringVar()

    def colors(self):
        self.aliceblue = "#F0F8FF"
        self.brown4 = "#8B2323"

    def screen(self):
        self.first_root.title("Luxury Wheels")  # altera titulo da janela
        self.first_root.resizable(True, True)  # permite redimensionar a janela
        self.first_root.geometry("700x500")
        self.first_root.configure()
        self.first_root.minsize(width=700,height=500)
        self.first_root.maxsize(width=900,height=800)
        self.first_root.iconbitmap('./static/assets/car.ico')

    def screen_frame(self):
        self.frame_1 = Frame(self.first_root,)
        self.frame_1.place(relx=0.05,rely=0.03,relwidth=0.9, relheight=0.2)
        self.frame_2 = Frame(self.first_root)
        self.frame_2.place(relx=0.05, rely=0.30, relwidth=0.9, relheight=0.6)

    def login_screen(self):
        self.label_title = ttk.Label(self.frame_1,text="Luxury Wheels", font=("times",30,"bold"))
        self.label_title.place(relx=0.3, rely=0.2)
        global photo_title
        photo_title = PhotoImage(file="static\img\mercedesglc.png").subsample(2,2)
        self.label_photo_title = ttk.Label(self.frame_1,image=photo_title)
        self.label_photo_title.place(relx =0.01, rely=0.03)
        self.label_photo_title_2 = ttk.Label(self.frame_1, image=photo_title)
        self.label_photo_title_2.place(relx=0.75, rely=0.03)

        self.label_login_title = ttk.LabelFrame(self.frame_2,text="Admin",relief="solid")
        self.label_login_title.place(relx=0.01,rely=0.01,width=700,height=300)

        self.login = ttk.Label(self.label_login_title,text="Login: ", font=("times",20,"bold"))
        self.login.place(relx=0.15,rely=0.2)
        self.entry_login = ttk.Entry(self.label_login_title,textvariable=self.var_login,font=("times",15))
        self.entry_login.place(relx=0.35,rely=0.21,relwidth=0.4, relheight=0.1)
        self.entry_login.focus()


        self.password = ttk.Label(self.label_login_title, text="Password: ", font=("times", 20, "bold"))
        self.password.place(relx=0.15, rely=0.4)
        self.entry_password = ttk.Entry(self.label_login_title, textvariable=self.var_password,show="*",font=(20))
        self.entry_password.place(relx=0.35, rely=0.41, relwidth=0.4, relheight=0.1)

        self.photo_login = PhotoImage(file="static/assets/butonlogin.png").subsample(10,11)
        self.button_login = ttk.Button(self.label_login_title, image=self.photo_login)
        self.button_login.place(relx=0.45 , rely=0.6)







# if __name__ == '__main__':
#
#     App_admin()


