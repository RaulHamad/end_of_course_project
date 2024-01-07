from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,timedelta

root = Tk()

class Data_base():


    def open_sql(self):
        self.conn = sqlite3.connect("database/luxurywheels.db")
        self.cursor = self.conn.cursor()


    def close_sql(self):
        self.conn.close()


    def table_admin(self):
        self.open_sql()

        admin_table =   """
                        CREATE TABLE IF NOT EXISTS administrators (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name      varchar(30) NOT NULL,
                        password  varchar(50) NOT NULL
                        );
                        """
        self.cursor.execute(admin_table)
        self.conn.commit()
        self.close_sql()

    def table_iva(self):
        self.open_sql()

        iva_table =   """
                        CREATE TABLE IF NOT EXISTS iva_payments (
                        id	INTEGER NOT NULL,
                        name	varchar(30) NOT NULL,
                        type	varchar(50) NOT NULL,
                        price	INTEGER NOT NULL,
                        PRIMARY KEY("id")
                                            );
                        """
        self.cursor.execute(iva_table)
        self.conn.commit()
        self.close_sql()
    def query_admin(self):
        self.open_sql()
        verify_table_admin = """SELECT * FROM  administrators"""
        result = self.cursor.execute(verify_table_admin)

        return result.fetchall()

    def create_admin(self):
        self.open_sql()
        self.query_admin()
        if self.query_admin() == []:

            pass_cryp = generate_password_hash('admin', method='pbkdf2:sha256')
            admin= [1,"admin",pass_cryp]
            admin_login = """INSERT INTO administrators VALUES(?,?,?);"""
            self.cursor.execute(admin_login,admin)
            self.conn.commit()

        self.close_sql()


    def query_vehicle(self):

        self.open_sql()
        vehicle_table = """SELECT 
        v.id,
        v.name,
        CASE WHEN v.status =1 AND v.service = 5 THEN 'Maintenance' 
            WHEN v.status=1 THEN 'Available'
            WHEN v.status=0 THEN 'Rented'
            ELSE 'other'
       END,
        v.service,
        v.date_service,
        v.iva,
        v.next_iva,
        v.price_day,
        c.category
        from vehicles v INNER JOIN vehicle_types t on v.type_id = t.id
        INNER JOIN categories c on v.category_id = c.id
        ORDER BY c.category ASC;
        """
        result = self.cursor.execute(vehicle_table)

        return result

    def query_rents(self):
        self.open_sql()
        rents_table = """
        SELECT 
        rents.id,
        c.name,
        v.name,
        rents.pick_up_date,
        rents.return_date,
        rents.price_day,
        CASE WHEN rents.status_rent =1 THEN 'Rented'
            WHEN rents.status_rent=0 THEN 'EndRent'
            ELSE 'other'
            END,
        rents.total_price
        FROM rents  INNER JOIN clients c on rents.client_id = c.id
        INNER JOIN vehicles v on rents.vehicle_id = v.id
        ORDER BY rents.return_date DESC;
        """
        result = self.cursor.execute(rents_table)

        return result

    def query_service(self):
        self.open_sql()

        service_table = """
        SELECT 
        v.id,
        v.name,
        CASE WHEN v.status=1 THEN 'Available'
            WHEN v.status=0 THEN 'Rented'
            ELSE 'other'
       END,
        v.service,
        v.iva,
        r.return_date,
        v.date_service
               
        
        FROM vehicles v INNER JOIN rents r on v.id = r.vehicle_id
        WHERE v.service > 4 
        GROUP BY v.name
        ORDER BY r.return_date desc ;
        """
        result = self.cursor.execute(service_table)
        return result

    def query_iva(self):
        date = str(datetime.now().date())
        self.open_sql()
        vehicle_table = """SELECT 
                v.id,
                t.type,
                v.name,
                v.iva,
                v.next_iva
                
                from vehicles v INNER JOIN vehicle_types t on v.type_id = t.id
                WHERE v.next_iva < '{}'
                ORDER BY v.iva ASC;
                """.format(date)
        result = self.cursor.execute(vehicle_table)

        return result


class App_admin(Data_base):


    def __init__(self):
        self.first_root = root
        self.variable()
        self.colors()
        self.screen()
        self.screen_frame_1()
        self.screen_frame_2()
        self.label_notification()
        self.table_iva()
        self.table_admin()
        self.query_admin()
        self.create_admin()





        root.mainloop()

    def variable(self):
        self.var_login = StringVar()
        self.var_password = StringVar()


    def colors(self):
        self.deepskyblue = "#00688B"
        self.deepskyblue4 = "#1C86EE"
        self.darkslategray ="#2F4F4F"
        self.brown1 = "#FF4040" #vermelho para aviso
        self.ghostwhite = "#F8F8FF"

    def screen(self):
        self.first_root.title("Luxury Wheels")  # altera titulo da janela
        self.first_root.resizable(True, True)  # permite redimensionar a janela
        self.first_root.geometry("700x500")
        self.first_root.configure()
        self.first_root.minsize(width=700,height=500)
        self.first_root.maxsize(width=900,height=800)
        self.first_root.iconbitmap('./static/assets/car.ico')

    def screen_frame_1(self):
        self.frame_1 = Frame(self.first_root)
        self.frame_1.place(relx=0.05,rely=0.03,relwidth=0.9, relheight=0.2)

        self.label_title = ttk.Label(self.frame_1, text="Luxury Wheels", font=("times", 30, "bold"))
        self.label_title.place(relx=0.3, rely=0.2)

        global photo_title
        photo_title = PhotoImage(file="static\img\mercedesglc.png").subsample(2, 2)
        self.label_photo_title = ttk.Label(self.frame_1, image=photo_title)
        self.label_photo_title.place(relx=0.01, rely=0.03)

        self.label_photo_title_2 = ttk.Label(self.frame_1, image=photo_title)
        self.label_photo_title_2.place(relx=0.75, rely=0.03)



    def screen_frame_2(self):
        self.frame_2 = Frame(self.first_root)
        self.frame_2.place(relx=0.05, rely=0.30, relwidth=0.9, relheight=0.6)

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
        self.button_login = ttk.Button(self.label_login_title,command=self.autentication_login, image=self.photo_login)
        self.button_login.place(relx=0.45 , rely=0.6)
        self.button_login.bind('<Return>',lambda x: x==self.autentication_login())

    def label_notification(self):
        self.label_login = ttk.Label(self.frame_2,text="",font=(15),background=self.brown1,foreground=self.ghostwhite)
        self.label_login.place(relx=0.5,rely=0.07)
        self.label_login.place_forget()


    def autentication_login(self):

        # print(self.var_login.get(),self.var_password.get())
        # if len(self.var_login.get()) == 0 or len(self.var_password.get()) == 0:
        #     self.label_login["text"] = "Login or Password does not exist"
        #     self.label_login.place(relx=0.5, rely=0.07)
        #     self.var_login.set("")
        #     self.var_password.set("")
        #
        # else:
        #     for i in self.query_admin():
        #         pass_cryp = check_password_hash(i[2], self.var_password.get())
        #
        #         if self.var_login.get() != i[1] and pass_cryp == False:
        #             self.label_login["text"] = "Login ou senha inválidos"
        #             self.label_login.place(relx=0.5, rely=0.07)
        #             self.var_login.set("")
        #             self.var_password.set("")
        #
        #         else:
        #
        #             self.label_login["text"] = "Logado"
        #             self.label_login.place(relx=0.5, rely=0.07)
        #             self.var_login.set("")
        #             self.var_password.set("")
                    return self.screen_frame_main_data()
    def screen_frame_main_data(self):

        self.frame_1.place_forget()
        self.frame_2.place_forget()

        self.frame_3 = Frame(self.first_root,background=self.deepskyblue)
        self.frame_3.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.99)

        self.label_main_options = ttk.Label(self.frame_3,background=self.deepskyblue)
        self.label_main_options.place(relx=0.02, rely=0.03, relwidth=0.96, relheight=0.2)

        self.label_main_view_vehicle = ttk.Label(self.frame_3,background="white")
        self.label_main_view_vehicle.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.7)

        self.button_list_vehicle = Button(self.label_main_options, text="VEHICLES",command=self.list_vehicle,
                                          font=("bold"),foreground="white",
                                          bg=self.darkslategray,relief="raise")
        self.button_list_vehicle.place(relx=0.01, rely=0.02, relwidth=0.2, relheight=0.25)

        self.button_list_rent = Button(self.label_main_options, text="RENTS",command=self.list_rents,
                                       font=("bold"),foreground="white",
                                          bg=self.darkslategray, relief="raise")
        self.button_list_rent.place(relx=0.27, rely=0.02, relwidth=0.2, relheight=0.25)

        self.button_service = Button(self.label_main_options, text="VERIFY SERVICE", font=("bold"),
                                     command=self.service_maintenance, foreground="white",
                                     bg=self.darkslategray, relief="raise")
        self.button_service.place(relx=0.53, rely=0.02, relwidth=0.2, relheight=0.25)


        self.button_iva = Button(self.label_main_options, text="VERIFY IVA", font=("bold"),foreground="white",
                                         command=self.list_iva, bg=self.darkslategray, relief="raise")
        self.button_iva.place(relx=0.79, rely=0.02, relwidth=0.2, relheight=0.25)



    def clear_checklist(self):

        return self.label_main_view_vehicle.place_forget()
    def list_vehicle(self):

        try:
            self.button_start_service.place_forget()
        except:
            pass

        try:
            self.button_pay_iva.place_forget()
        except:
            pass

        self.label_main_view_vehicle.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.7)
        self.check_data = ttk.Treeview(self.label_main_view_vehicle,height=3,style="mystyle.Treeview",
                                       column=("col1","col2","col3","col4","col5","col6","col7","col8",'col9'))
        self.check_data.tag_configure('bg', background='yellow')
        self.check_data.tag_configure('fg', foreground="red")
        self.check_data.tag_configure('bg2', background="red")
        self.check_data.tag_configure('fg2', foreground="black")
        self.check_data.place(relx=0.01, rely=0.02, relwidth=0.96, relheight=0.95)

        self.check_data.heading("#0", text="", anchor=CENTER)
        self.check_data.heading("#1", text="id", anchor=CENTER)
        self.check_data.heading("#2", text="Vehicle", anchor=CENTER)
        self.check_data.heading("#3", text="Status", anchor=CENTER)
        self.check_data.heading("#4", text="Service", anchor=CENTER)
        self.check_data.heading("#5", text="Date Service", anchor=CENTER)
        self.check_data.heading("#6", text="IVA", anchor=CENTER)
        self.check_data.heading("#7", text="Next IVA", anchor=CENTER)
        self.check_data.heading("#8", text="Price", anchor=CENTER)
        self.check_data.heading("#9", text="Category", anchor=CENTER)


        self.check_data.column("#0",width=1)
        self.check_data.column("#1", width=20)
        self.check_data.column("#2", width=100)
        self.check_data.column("#3", width=85)
        self.check_data.column("#4", width=60)
        self.check_data.column("#5", width=70)
        self.check_data.column("#6", width=70)
        self.check_data.column("#7", width=65)
        self.check_data.column("#8", width=70)
        self.check_data.column("#9", width=90)

        self.scrool = Scrollbar(self.label_main_view_vehicle,orient="vertical")
        self.check_data.configure(yscrollcommand=self.scrool.set)
        self.scrool.place(relx=0.96, rely=0.02, relwidth=0.05, relheight=0.95)

        self.check_data.delete(*self.check_data.get_children())


        for check_vehicle in self.query_vehicle():

            if check_vehicle[2] == 'Rented':
                self.check_data.insert("",END,values=check_vehicle,tags=('fg','bg'))
            elif check_vehicle[3] > 4:
                if check_vehicle[4] < str(datetime.now().date()):
                    self.check_data.insert("", END, values=check_vehicle, tags=('fg', 'bg'))
                else:
                    self.check_data.insert("", END, values=check_vehicle, tags=('fg', 'bg'))
            elif datetime.strptime(check_vehicle[6],'%Y-%m-%d').date() <= datetime.now().date():
                self.check_data.insert("", END, values=check_vehicle, tags=('fg','bg'))

            else:
                self.check_data.insert("", END, values=check_vehicle)
        for check_vehicle in self.query_vehicle():

            if check_vehicle[3] > 4 and check_vehicle[4] < str(datetime.now().date()):
                messagebox.showinfo("Service Car", "Vehicle need service!")
                break
        for check_vehicle in self.query_vehicle():
            if datetime.strptime(check_vehicle[6],'%Y-%m-%d').date() <= datetime.now().date():
                messagebox.showinfo("Service Car", "Vehicle need to pay IVA!")
                break
        self.close_sql()
    def list_rents(self):

        try:
            self.button_start_service.place_forget()
        except:
            pass

        try:
            self.button_pay_iva.place_forget()
        except:
            pass

        self.label_main_view_vehicle.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.7)
        self.check_data = ttk.Treeview(self.label_main_view_vehicle,height=3,style="mystyle.Treeview",
                                       columns=("col1","col2","col3","col4","col5","col6","col7","col8"))
        self.check_data.tag_configure('bg', background='yellow')
        self.check_data.tag_configure('fg', foreground="red")
        self.check_data.place(relx=0.01, rely=0.02, relwidth=0.96, relheight=0.95)

        self.check_data.heading("#0", text="", anchor=CENTER)
        self.check_data.heading("#1", text="id", anchor=CENTER)
        self.check_data.heading("#2", text="Client", anchor=CENTER)
        self.check_data.heading("#3", text="Vehicle", anchor=CENTER)
        self.check_data.heading("#4", text="Pick_up_date", anchor=CENTER)
        self.check_data.heading("#5", text="Return_date", anchor=CENTER)
        self.check_data.heading("#6", text="Price_day", anchor=CENTER)
        self.check_data.heading("#7", text="Status_rent", anchor=CENTER)
        self.check_data.heading("#8", text="Total_price", anchor=CENTER)


        self.check_data.column("#0",width=1)
        self.check_data.column("#1", width=20)
        self.check_data.column("#2", width=90)
        self.check_data.column("#3", width=115)
        self.check_data.column("#4", width=60)
        self.check_data.column("#5", width=60)
        self.check_data.column("#6", width=60)
        self.check_data.column("#7", width=50)
        self.check_data.column("#8", width=90)

        self.scrool = Scrollbar(self.label_main_view_vehicle,orient="vertical")
        self.check_data.configure(yscrollcommand=self.scrool.set)
        self.scrool.place(relx=0.96, rely=0.02, relwidth=0.05, relheight=0.95)

        self.check_data.delete(*self.check_data.get_children())
        for check_rent in self.query_rents():

            if check_rent[6] == 'Rented':
                self.check_data.insert("",END,values=check_rent,tags=('fg','bg'))

            else:
                self.check_data.insert("", END, values=check_rent)
        self.close_sql()
    def service_maintenance(self):

        try:
            self.button_pay_iva.place_forget()
        except:
            pass

        self.label_main_view_vehicle.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.7)
        self.check_data = ttk.Treeview(self.label_main_view_vehicle, height=3, style="mystyle.Treeview",
                                       column=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.check_data.tag_configure('bg', background='yellow')
        self.check_data.tag_configure('fg', foreground="red")
        self.check_data.place(relx=0.01, rely=0.02, relwidth=0.96, relheight=0.95)

        self.button_start_service = Button(self.label_main_options, text="START SERVICE", font=("bold")
                                    ,command=self.start_maintenance, foreground="white",
                                     bg=self.darkslategray, relief="raise")
        self.button_start_service.place(relx=0.53, rely=0.35, relwidth=0.2, relheight=0.25)

        self.check_data.heading("#0", text="", anchor=CENTER)
        self.check_data.heading("#1", text="id", anchor=CENTER)
        self.check_data.heading("#2", text="Name", anchor=CENTER)
        self.check_data.heading("#3", text="Status", anchor=CENTER)
        self.check_data.heading("#4", text="Service", anchor=CENTER)
        self.check_data.heading("#5", text="IVA", anchor=CENTER)
        self.check_data.heading("#6", text="Return_date", anchor=CENTER)
        self.check_data.heading("#7", text="Date Service", anchor=CENTER)


        self.check_data.column("#0", width=1)
        self.check_data.column("#1", width=20)
        self.check_data.column("#2", width=90)
        self.check_data.column("#3", width=115)
        self.check_data.column("#4", width=60)
        self.check_data.column("#5", width=60)
        self.check_data.column("#6", width=60)
        self.check_data.column("#7", width=70)


        self.scrool = Scrollbar(self.label_main_view_vehicle, orient="vertical")
        self.check_data.configure(yscrollcommand=self.scrool.set)
        self.scrool.place(relx=0.96, rely=0.02, relwidth=0.05, relheight=0.95)

        self.check_data.delete(*self.check_data.get_children())
        date_now = datetime.now().date()
        for check_rent in self.query_service():

            if check_rent[6] < str(date_now):
                self.check_data.insert("", END, values=check_rent, tags=('fg', 'bg'))
        if self.check_data.get_children() == ():
            self.button_start_service.place_forget()
            messagebox.showinfo("Service Car", "All vehicles service conclued!")
        self.close_sql()
    def start_maintenance(self):
        self.check_data.delete(*self.check_data.get_children())
        date_maintenance = timedelta(days=30)

        for check_rent in self.query_service():
            if check_rent[6] < str(datetime.now().date()):
                print(check_rent)

                convert_for_date = datetime.strptime(check_rent[5],'%Y-%m-%d').date()
                new_date_finish_maintenance = str(convert_for_date + date_maintenance)
                print(new_date_finish_maintenance,type(new_date_finish_maintenance))

                date_finish_maintenance = '''UPDATE vehicles SET date_service ='{}'
                 WHERE service = 5'''.format(new_date_finish_maintenance)

                self.cursor.execute(date_finish_maintenance)
                self.conn.commit()
        self.button_start_service.place_forget()
        self.list_vehicle()
        self.close_sql()
    def list_iva(self):

        try:
            self.button_start_service.place_forget()
        except:
            pass

        self.label_main_view_vehicle.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.7)
        self.check_data = ttk.Treeview(self.label_main_view_vehicle, height=3, style="mystyle.Treeview",
                                       column=("col1", "col2", "col3", "col4", "col5"))
        self.check_data.tag_configure('bg', background='yellow')
        self.check_data.tag_configure('fg', foreground="red")
        self.check_data.tag_configure('bg2', background="red")
        self.check_data.tag_configure('fg2', foreground="black")
        self.check_data.place(relx=0.01, rely=0.02, relwidth=0.96, relheight=0.95)

        self.button_pay_iva = Button(self.label_main_options, text="Pay IVA", font=("bold")
                                           , foreground="white",command=self.pay_iva,
                                           bg=self.darkslategray, relief="raise")
        self.button_pay_iva.place(relx=0.79, rely=0.35, relwidth=0.2, relheight=0.25)

        self.check_data.heading("#0", text="", anchor=CENTER)
        self.check_data.heading("#1", text="id", anchor=CENTER)
        self.check_data.heading("#2", text="Type", anchor=CENTER)
        self.check_data.heading("#3", text="Name", anchor=CENTER)
        self.check_data.heading("#4", text="Iva", anchor=CENTER)
        self.check_data.heading("#5", text="Next Iva", anchor=CENTER)



        self.check_data.column("#0", width=1)
        self.check_data.column("#1", width=50)
        self.check_data.column("#2", width=100)
        self.check_data.column("#3", width=100)
        self.check_data.column("#4", width=100)
        self.check_data.column("#5", width=100)


        self.scrool = Scrollbar(self.label_main_view_vehicle, orient="vertical")
        self.check_data.configure(yscrollcommand=self.scrool.set)
        self.scrool.place(relx=0.96, rely=0.02, relwidth=0.05, relheight=0.95)

        self.check_data.delete(*self.check_data.get_children())


        date_now = datetime.now().date()
        for check_iva in self.query_iva():
            date_table = datetime.strptime(check_iva[4],'%Y-%m-%d').date()
            self.check_data.insert("", END, values=check_iva, tags=('fg', 'bg'))

        if self.check_data.get_children() == ():
            self.button_pay_iva.place_forget()
            messagebox.showinfo("Service Car", "All vehicles paid!")

    def pay_iva(self):
        self.check_data.delete(*self.check_data.get_children())
        date_yearly_iva = timedelta(days=365)
        date_now = datetime.now().date()

        for check_iva in self.query_iva():
            date_table = datetime.strptime(check_iva[4], '%Y-%m-%d').date()
            new_date_iva = str(date_table + date_yearly_iva)



            # date_pay_iva = '''UPDATE vehicles SET iva ='{}', next_iva = '{}' WHERE next_iva > '{}'
            #                   '''.format(str(check_iva[4]),new_date_iva,str(date_now))
            # self.cursor.execute(date_pay_iva)
            # self.conn.commit()
            if check_iva[1] == 'Car':
                print('car')
                print(check_iva)

                # update_iva_prices_car = """
                #                 INSERT INTO iva_payments (name,type,price) VALUES (?,?,?);
                #                 """
                # self.cursor.execute(update_iva_prices_car,(check_iva[2],check_iva[1],250))
                # self.conn.commit()


            elif check_iva[1] == 'Motorcycle':
                print('moto')
                print(check_iva)

                # update_iva_prices_moto = """
                #         INSERT INTO iva_payments (name,type,price) VALUES (?,?,?);
                #         """
                # self.cursor.execute(update_iva_prices_moto,(check_iva[2],check_iva[1],150))
                # self.conn.commit()



        self.button_pay_iva.place_forget()
        self.list_iva()
        self.close_sql()

if __name__ == '__main__':

    App_admin()



