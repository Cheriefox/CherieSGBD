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
        self.etiq.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        self.sql_txt = ttk.Entry(self)
        self.sql_txt.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        
        self.sql_button = ttk.Button(self, text="Ejecutar")
        self.sql_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        

class AdminDb:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("CherieSGBD")
        self.ventana1.geometry("1200x840")

        #Crear y configurar panel de pestañas
        self.panel = ttk.Notebook(self.ventana1)
        self.panel.grid(column=1, row=1, padx=10, pady=10)

        #self.panel.pack(fill="both",expand="yes")
        self.panel.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
        self.panel.config(width=200,height=220)

        self.tree_frame = ttk.Frame(self.ventana1)  # Crea el Frame para contener los tres árboles
        self.tree_frame.place(x=0, y=400, width=1200, height=300)  # Coloca el frame en la parte inferior de la ventana

        # Pestaña SQL Query
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
        
        
        # Contenedor para los formularios de conexión (Servidor, Usuario, etc.)
        conn_frame = ttk.Frame(self.ventana1)
        conn_frame.grid(column=0, row=0, padx=10, pady=10, sticky='w')

        #Conexion al servidor
        labelSrv = ttk.Label(conn_frame, text="Servidor:")
        labelSrv.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ServerName = ttk.Entry(conn_frame)
        self.ServerName.insert(0, "localhost")
        self.ServerName.grid(row=0, column=1, padx=10, pady=10) 
        
        labelUser = ttk.Label(conn_frame, text="Usuario:")
        labelUser.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.UserName = ttk.Entry(conn_frame)
        self.UserName.insert(0, "root")
        self.UserName.grid(row=1, column=1, padx=10, pady=10)
        
        labelPass = ttk.Label(conn_frame, text="Password:")
        labelPass.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.PassName = ttk.Entry(conn_frame, show="*")
        self.PassName.insert(0, "")
        self.PassName.grid(row=2, column=1, padx=10, pady=10)

        labelPuerto = ttk.Label(conn_frame, text="Puerto:")
        labelPuerto.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.PuertoName = ttk.Entry(conn_frame)
        self.PuertoName.insert(0, "3306")
        self.PuertoName.grid(row=3, column=1, padx=10, pady=10)

        botonConn = ttk.Button(conn_frame, text="Conectar", command=self.ConectarServidor)
        botonConn.grid(row=4, column=1, padx=10, pady=10)

        self.labelStsServer = ttk.Label(conn_frame, text="Sin Conexion")
        self.labelStsServer.grid(row=4, column=2, padx=10, pady=10)


        labelBaseSel=ttk.Label(text="Base: ")
        labelBaseSel.grid(column=2, row=1, padx=4, pady=4)
        self.BaseSel=ttk.Entry()
        self.BaseSel.grid(column=3, row=1, padx=4, pady=4)

        labelTablaSel=ttk.Label(text="Tabla: ")
        labelTablaSel.grid(column=4, row=1, padx=4, pady=4)
        self.TablaSel=ttk.Entry()
        self.TablaSel.grid(column=5, row=1, padx=4, pady=4)


        


        #arbol de bases de datos
        self.TvBases = ttk.Treeview(self.tree_frame, selectmode="browse", columns="#1")
        self.TvBases.heading('#1', text='BASES DE DATOS')
        self.TvBases.grid(row=0, column=0, padx=0 , pady=10, sticky="nsew")
        
        # Árbol de tablas   
        self.TvTablas = ttk.Treeview(self.tree_frame, selectmode="browse")
        self.TvTablas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        
         # Árbol de campos
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.TvCampos = ttk.Treeview(self.tree_frame, show="headings", height=5, columns=columns)
        self.TvCampos.heading('#1', text='P.Key', anchor='nw')
        self.TvCampos.column('#1', width=60, anchor='nw', stretch=False)
        self.TvCampos.heading('#2', text='Nombre', anchor='center')
        self.TvCampos.column('#2', width=10, anchor='nw', stretch=True)
        self.TvCampos.heading('#3', text='Tipo', anchor='center')
        self.TvCampos.column('#3', width=10, anchor='nw', stretch=True)
        self.TvCampos.heading('#4', text='Not NULL', anchor='center')
        self.TvCampos.column('#4', width=10, anchor='nw', stretch=True)
        self.TvCampos.heading('#5', text='Auto Inc', anchor='center')
        self.TvCampos.column('#5', width=10, anchor='nw', stretch=True)
        self.TvCampos.heading('#6', text='Flags', anchor='center')
        self.TvCampos.column('#6', width=10, anchor='nw', stretch=True)
        self.TvCampos.heading('#7', text='Default', anchor='center')
        self.TvCampos.column('#7', width=10, anchor='nw', stretch=True)
        self.TvCampos.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Configurar que las columnas del tree_frame se ajusten al tamaño
        self.tree_frame.grid_columnconfigure(0, weight=0)  # Base de Datos
        self.tree_frame.grid_columnconfigure(1, weight=1)  # Tablas
        self.tree_frame.grid_columnconfigure(2, weight=2)# Campos (ajustado a un peso de 1 también)
    
        self.tree_frame.grid_rowconfigure(0, weight=1)  # Fila 0 (con los tres árboles)
        
        # Configurar el sistema de filas y columnas
        self.ventana1.grid_rowconfigure(5, weight=1)
        self.ventana1.grid_rowconfigure(6, weight=1)
        self.ventana1.grid_columnconfigure(0, weight=1)
        self.ventana1.grid_columnconfigure(1, weight=2)
        self.ventana1.grid_columnconfigure(2, weight=1)
        self.ventana1.grid_columnconfigure(3, weight=1)

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
        # Si ya existe la etiqueta, solo se actualiza su texto
        if hasattr(self, 'labelStsServer'):
            self.labelStsServer.config(text="Conectando...")

        try:
            # Intentar conectar a la base de datos
            self.db_connection = mysql.connector.connect(
                host=self.ServerName.get(),
                user=self.UserName.get(),
                password=self.PassName.get(),
                port=self.PuertoName.get()  # Añadir el puerto aquí
            )

            # Si la conexión es exitosa
            if self.db_connection.is_connected():
                # Cambiar el texto de la etiqueta para mostrar el estado de "Conectado"
                if hasattr(self, 'labelStsServer'):
                    self.labelStsServer.config(text="Conectado")
            else:
                if hasattr(self, 'labelStsServer'):
                    self.labelStsServer.config(text="Sin Conexion")

        except mysql.connector.Error as err:
            # En caso de error de conexión, mostrar mensaje de error
            if hasattr(self, 'labelStsServer'):
                self.labelStsServer.config(text=f"Error: {err}")

        # Consultar bases de datos disponibles
        sql = "SHOW DATABASES"
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute(sql)
        rows = self.db_cursor.fetchall()

        # Limpiar el árbol de bases de datos y agregar las nuevas
        self.TvBases.delete(*self.TvBases.get_children())
        for row in rows:
            self.TvBases.insert("", tk.END, text=row[0])

    def ventanachica(self):
        self.ventana1.geometry("640x480")

    def ventanagrande(self):
        self.ventana1.geometry("1024x800")

AdminDb1=AdminDb()