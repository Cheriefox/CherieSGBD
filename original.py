import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import mysql.connector

BASES=[]
TABLAS=[]

class SqlFrame(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

                
        self.etiq = ttk.Label(self)
        self.etiq["text"] = ("Ingresar query")
        self.etiq.pack()
        
        self.sql_txt = ttk.Entry(self)
        self.sql_txt.pack()
        
        
        self.sql_button = ttk.Button(self, text="Ejecutar")
        self.sql_button.pack(pady=10)
        
        

class AdminDb:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("Administracion de Bases de Datos MySql")
        self.ventana1.geometry("1200x840")
        #menubar1 = tk.Menu(self.ventana1)
        #self.ventana1.config(menu=menubar1)
        #opciones1 = tk.Menu(menubar1)
        #opciones1.add_command(label="Seleccionar", command=self.fijarrojo)
        #opciones1.add_command(label="Crear", command=self.fijarverde)
        #opciones1.add_command(label="Eliminar", command=self.fijarazul)
        #menubar1.add_cascade(label="Base de Datos", menu=opciones1)        
        #opciones2 = tk.Menu(menubar1)
        #opciones2.add_command(label="Crear", command=self.ventanachica)
        #opciones2.add_command(label="Editar", command=self.ventanagrande)
        #opciones2.add_command(label="Eliminar", command=self.ventanagrande)
        #menubar1.add_cascade(label="Tablas", menu=opciones2)    
        #opciones3 = tk.Menu(menubar1)
        #opciones3.add_command(label="Sql", command=self.ventanachica)
        #opciones3.add_command(label="Imortar", command=self.ventanagrande)
        #opciones3.add_command(label="Exportar", command=self.ventanagrande)
        #menubar1.add_cascade(label="Herramientas", menu=opciones3)
        
        #Crear y configurar panel de pestañas
        self.panel = ttk.Notebook(self.ventana1)
        #self.panel.pack(fill="both",expand="yes")
        self.panel.grid(column=5, row=2, padx=55, pady=0)
        self.panel.config(width=200,height=220)

        #pestaña sql query
        #self.sql_label = ttk.Label(self.panel,text="Query Sql")
        #self.panel.add(self.sql_label, text="Query Sql", padding=20)
        #self.panel.txtSql=ttk.Entry(self.sql_label)
        #self.sql_txt = ttk.Entry(self.panel)
        #self.panel.add(self.sql_txt)
        self.sql_frame = SqlFrame(self.panel)
        self.panel.add(self.sql_frame, text="Sql Query", padding=10)
        
        

        #Pestaña crear BD
        self.createBD_label = ttk.Label(self.panel,text="Crear Base")
        self.panel.add(self.createBD_label, text="Crear Base", padding=20)

        #Pestaña Crear Tabla
        self.createTabla_label = ttk.Label(self.panel,text="Crear Tabla") 
        self.panel.add(self.createTabla_label, text="Crear Tabla", padding=20)

        #pestaña importacion
        self.importar_label = ttk.Label(self.panel,text="Importar") 
        self.panel.add(self.importar_label, text="Importar", padding=20)

        #pestaña exportacion
        self.exportar_label = ttk.Label(self.panel,text="Exportar")
        self.panel.add(self.exportar_label, text="Exportar", padding=20)
        
        
        

        #COnexion al servidor
        labelSrv=ttk.Label(text="Servidor:")
        labelSrv.grid(column=0, row=0, padx=4, pady=4)
        self.ServerName=ttk.Entry()
        self.ServerName.insert(0,"localhost")
        self.ServerName.grid(column=1, row=0, padx=4, pady=4) 
        
        labelUser=ttk.Label(text="Usuario:")
        labelUser.grid(column=2, row=0, padx=4, pady=4)
        self.UserName=ttk.Entry()
        self.UserName.insert(0,"root")
        self.UserName.grid(column=3, row=0, padx=4, pady=4)
        
        labelPass=ttk.Label(text="Password:")
        labelPass.grid(column=4, row=0, padx=4, pady=4)
        self.PassName=ttk.Entry(show="*")
        self.PassName.insert(0,"lp4458")
        self.PassName.grid(column=5, row=0, padx=4, pady=4)
        
        labelPuerto=ttk.Label(text="Puerto:")
        labelPuerto.grid(column=6, row=0, padx=4, pady=4)
        self.PuertoName=ttk.Entry()
        self.PuertoName.insert(0,"3306")
        self.PuertoName.grid(column=7, row=0, padx=4, pady=4)

        botonConn=ttk.Button(text="Conectar",command=self.ConectarServidor)
        botonConn.grid(column=8, row=0, padx=4, pady=4)

        self.labelStsServer=ttk.Label(text="Sin Conexion")
        self.labelStsServer.grid(column=9, row=0, padx=4, pady=4)

        labelBaseSel=ttk.Label(text="Base: ")
        labelBaseSel.grid(column=2, row=1, padx=4, pady=4)
        self.BaseSel=ttk.Entry()
        self.BaseSel.grid(column=3, row=1, padx=4, pady=4)

        labelTablaSel=ttk.Label(text="Tabla: ")
        labelTablaSel.grid(column=4, row=1, padx=4, pady=4)
        self.TablaSel=ttk.Entry()
        self.TablaSel.grid(column=5, row=1, padx=4, pady=4)

        #arbol de bases de datos
        self.TvBases = ttk.Treeview(self.ventana1, selectmode="browse",columns="#1")
        self.TvBases.heading('#1', text='BASES DE DATOS')
        self.TvBases.place(x=0, y=60, width=250, height=400)
        self.TvBases.bind('<<TreeviewSelect>>', self.base_selected)
        

        self.TvTablas= ttk.Treeview(self.ventana1, selectmode="browse")
        self.TvTablas.place(x=250, y=60, width=250, height=400)
        self.TvTablas.bind('<<TreeviewSelect>>', self.tabla_selected)
        
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")  
        self.TvCampos= ttk.Treeview(self.ventana1,show="headings",height="5", columns=columns) 
        self.TvCampos.place(x=0, y=400, width=500, height=600) 
        self.TvCampos.heading('#1', text='P.Key', anchor='nw')  
        self.TvCampos.column('#1', width=60, anchor='nw', stretch=False)  
        self.TvCampos.heading('#2', text='Nombre', anchor='center')  
        self.TvCampos.column('#2', width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#3', text='Tipo', anchor='center')  
        self.TvCampos.column('#3',width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#4', text='Not NULL', anchor='center')  
        self.TvCampos.column('#4',width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#5', text='Auto Inc', anchor='center')  
        self.TvCampos.column('#5',width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#6', text='Flags', anchor='center')  
        self.TvCampos.column('#6', width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#7', text='Default', anchor='center')  
        self.TvCampos.column('#7', width=10, anchor='nw', stretch=True)  
        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        #vsb= ttk.Scrollbar(self.ventana1, orient=tk.VERTICAL,command=self.TvCampos.yview)  
        #vsb.place(x=400 + 660 + 1, y=310, height=180 + 20)  
        #self.TvCampos.configure(yscroll=vsb.set)  
        #hsb = ttk.Scrollbar(self.ventana1, orient=tk.HORIZONTAL, command=self.TvCampos.xview)  
        #hsb.place(x=40 , y=310+200+1, width=620 + 20)  
        #self.TvCampos.configure(xscroll=hsb.set)  
        #self.TvCampos.bind("<<TreeviewSelect>>", self.MostrarCampos)     
        

        self.ventana1.mainloop()
        
    def tabla_selected(self,event):
        for selected_item in self.TvTablas.selection():
            item = self.TvTablas.item(selected_item)
            record = item['values']   
        i=int(selected_item)
        self.TablaSel.delete(0, tk.END)
        self.TablaSel.insert(0,TABLAS[i]) 
        self.MostrarCampos(TABLAS[i])
    
    def base_selected(self,event):
        for selected_item in self.TvBases.selection():
            item = self.TvBases.item(selected_item)
            record = item['values']
        i=int(selected_item)
        self.BaseSel.delete(0, tk.END)
        self.BaseSel.insert(0,BASES[i]) 
        self.MostrarTablas(BASES[i])
    
    def MostrarTablas(self,base): 
        #db_connection = mysql.connector.connect(host=self.ServerName.get(),  
        #user=self.UserName.get(),  
        #password=self.PassName.get())
        #db_cursor = db_connection.cursor(buffered=True)
        #if db_connection.is_connected() == False:  
        #    db_connection.connect() 

        #if db_connection.is_connected() == True:
        #    self.labelStsServer['text']=" Conectado "
        #else:
        #    self.labelStsServer['text']="Sin Conexion"
        #self.ConectarServidor()
        sql = "SHOW TABLES FROM "+ self.BaseSel.get() 
        print(sql)
        self.db_cursor.execute(sql)
        total = self.db_cursor.rowcount
        rows = self.db_cursor.fetchall()
        self.TvTablas.delete(*self.TvTablas.get_children())
        k=0
        TABLAS.clear()
        for row in rows: 
            TABLAS.append(row[0])
            self.TvTablas.insert("", tk.END,iid=k, text=row[0]) 
            k=k+1
        i=0
        
        while i< len(TABLAS):
            print(TABLAS[i])
            i=i+1
    
    
    def MostrarCampos(self,tabla): 
        
        sql = "SHOW FULL COLUMNS FROM "+ self.TablaSel.get() + " FROM " +  self.BaseSel.get()
        self.db_cursor.execute(sql)
        total = self.db_cursor.rowcount
        rows = self.db_cursor.fetchall()
        self.TvCampos.delete(*self.TvCampos.get_children())
        k=0
        for row in rows: 
            key = row[4]
            Nombre = row[0]
            tipo = row[1]
            nulo = row[3]
            default = row[6]
            otro = row[5]
            
            self.TvCampos.insert("", 'end', text=Nombre, values=(key, Nombre, tipo, nulo, default, otro)) 
            k=k+1
        i=0
        
        while i< len(TABLAS):
            print(TABLAS[i])
            i=i+1
    
    def ConectarServidor(self):
        
        self.labelStsServer=ttk.Label(text="Sin Conexion")
        self.labelStsServer.grid(column=9, row=0, padx=4, pady=4)
        self.db_connection = mysql.connector.connect(host=self.ServerName.get(),  
        user=self.UserName.get(),  
        password=self.PassName.get())
        self.db_cursor = self.db_connection.cursor(buffered=True)
        if self.db_connection.is_connected() == False:  
            self.db_connection.connect() 

        if self.db_connection.is_connected() == True:
            self.labelStsServer['text']=" Conectado "
        else:
            self.labelStsServer['text']="Sin Conexion"

        sql = "SHOW DATABASES"  
        self.db_cursor.execute(sql)
        total = self.db_cursor.rowcount
        rows = self.db_cursor.fetchall()
        self.TvBases.delete(*self.TvBases.get_children())
        k=0
        BASES.clear()
        for row in rows: 
            BASES.append(row[0])
            self.TvBases.insert("", tk.END,iid=k, text=row[0]) 
            k=k+1
        i=0
        
        while i< len(BASES):
            print(BASES[i])
            i=i+1
    
    def fijarrojo(self):
        self.ventana1.configure(background="red")

    def fijarverde(self):
        self.ventana1.configure(background="green")

    def fijarazul(self):
        self.ventana1.configure(background="blue")

    def ventanachica(self):
        self.ventana1.geometry("640x480")

    def ventanagrande(self):
        self.ventana1.geometry("1024x800")

AdminDb1=AdminDb()