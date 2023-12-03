from tkinter import *
from tkinter import ttk
import sqlite3


class App_admin():
    db = "database/luxurywheels.db"

    def __init__(self, root):
        self.janela = root
        self.janela.title("Luxury Wheels")#altera titulo da janela
        self.janela.resizable(True,True)#permite redimensionar a janela



