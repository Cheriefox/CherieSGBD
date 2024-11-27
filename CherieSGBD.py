import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import mysql.connector

BASES=[]
TABLAS=[]

class SqlFrame(ttk.Frame):

    def __init__(self, admin_db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_db = admin_db  # Recibe la instancia de AdminDb
        
        self.etiq = ttk.Label(self)
        self.etiq["text"] = ("Ingresar query")
        self.etiq.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        self.sql_txt = ttk.Entry(self)
        self.sql_txt.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        
        self.sql_button = ttk.Button(self, text="Ejecutar", command=self.ejecutar_query)
        self.sql_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
    def ejecutar_query(self):
        query = self.sql_txt.get()  # Obtener la consulta de la entrada de texto
        if not query:
            showinfo("Error", "Por favor ingrese una consulta SQL.")
            return

        try:
            # Acceder al cursor de la instancia de AdminDb
            db_cursor = self.admin_db.db_cursor
            db_cursor.execute(query)
            
            # Si la consulta es una SELECT, mostramos los resultados
            if query.strip().lower().startswith("select"):
                rows = db_cursor.fetchall()
                self.mostrar_resultados(rows)
            else:
                self.admin_db.db_connection.commit()  # Si no es un SELECT, ejecutamos el commit
        except mysql.connector.Error as err:
            showinfo("Error", f"Error al ejecutar la consulta: {err}")
    
    def mostrar_resultados(self, rows):
    # Mostrar los resultados en algún lugar, como en un Treeview o Label
        if not rows:
            showinfo("Resultado", "No se encontraron resultados.")
        else:
            # Usamos un Treeview para mostrar los resultados
            result_tree = ttk.Treeview(self)
            result_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            # Añadir columnas según el número de columnas en la respuesta (basado en el primer resultado)
            result_tree["columns"] = [str(i) for i in range(len(rows[0]))]
            for col in result_tree["columns"]:
                result_tree.heading(col, text=f"Columna {col}")

            # Insertar los datos
            for row in rows:
                result_tree.insert("", "end", values=row)
            self.grid_rowconfigure(2, weight=1)
            self.grid_columnconfigure(0, weight=1)

class AdminDb:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("CherieSGBD")
        self.ventana1.geometry("1200x840")

        self.db_connection = None
        self.db_cursor = None

        style = ttk.Style()
        style.theme_use("clam")

        # Personalización de colores
        style.configure("TButton",
                        padding=6,
                        relief="flat",
                        background="#61a0d1",  # Celeste claro
                        foreground="white")
        style.map("TButton",
                  background=[('active', '#558abf')])  # Color azul al hacer clic

        style.configure("TLabel",
                        background="#e6f7ff",  # Color de fondo azul claro
                        foreground="#333333")  # Texto oscuro

        style.configure("TEntry",
                        padding=6,
                        relief="flat",
                        background="#cce0ff",  # Fondo celeste
                        foreground="#333333")

        #Crear y configurar panel de pestañas
        self.panel = ttk.Notebook(self.ventana1)
        self.panel.grid(column=1, row=1, padx=10, pady=10)

        #self.panel.pack(fill="both",expand="yes")
        self.panel.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
        self.panel.config(width=200,height=220)

        self.tree_frame = ttk.Frame(self.ventana1)  # Crea el Frame para contener los tres árboles
        self.tree_frame.place(x=0, y=400, width=1200, height=300)  # Coloca el frame en la parte inferior de la ventana

        # Pestaña SQL Query
        self.sql_frame = SqlFrame(self, self.panel)
        self.panel.add(self.sql_frame, text="Sql Query", padding=10)
        
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

        self.labelStsServer = ttk.Label(conn_frame, text="Sin Conexion", foreground="red")
        self.labelStsServer.grid(row=4, column=2, padx=10, pady=10, sticky="w")


        labelBaseSel = ttk.Label(conn_frame, text="Base: ")
        labelBaseSel.grid(column=0, row=5, padx=4, pady=4)  # Movido a fila 5
        self.BaseSel = ttk.Entry(conn_frame)
        self.BaseSel.grid(column=1, row=5, padx=4, pady=4)  # Movido a fila 5

        labelTablaSel = ttk.Label(conn_frame, text="Tabla: ")
        labelTablaSel.grid(column=0, row=6, padx=4, pady=4)  # Movido a fila 6, debajo de "Base"
        self.TablaSel = ttk.Entry(conn_frame)
        self.TablaSel.grid(column=1, row=6, padx=4, pady=4)
        


        #arbol de bases de datos
        self.TvBases = ttk.Treeview(self.tree_frame, selectmode="browse", columns="#0")
        self.TvBases.heading('#0', text='BASES DE DATOS')
        self.TvBases.grid(row=0, column=0, padx=0 , pady=10, sticky="nsew")
        self.TvBases.bind('<<TreeviewSelect>>', self.base_selected)
        
        self.TvTablas = ttk.Treeview(self.tree_frame, selectmode="browse", columns="#1")  # Añadimos la columna "#1"
        self.TvTablas.heading('#0', text='TABLAS')  # Aquí agregamos el heading para el árbol de tablas
        self.TvTablas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.TvTablas.bind('<<TreeviewSelect>>', self.tabla_selected)
        
         # Árbol de campos
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.TvCampos = ttk.Treeview(self.tree_frame, show="headings", height=5, columns=columns)
        self.TvCampos.heading('#1', text='P.Key', anchor='nw')
        self.TvCampos.column('#1', width=40, anchor='nw', stretch=False)
        self.TvCampos.heading('#2', text='Nombre', anchor='center')
        self.TvCampos.column('#2', width=30, anchor='nw', stretch=True)
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
        self.tree_frame.grid_columnconfigure(1, weight=0)  # Tablas
        self.tree_frame.grid_columnconfigure(2, weight=5)  # Campos (ajustado a un peso de 1 también)
    
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
        selected_item = self.TvBases.selection()
        if not selected_item:
            showinfo("Advertencia", "Por favor selecciona una base de datos.")
            return
        item = self.TvBases.item(selected_item)
        base = item['text']
        self.BaseSel.delete(0, tk.END)
        self.BaseSel.insert(0, base)
        self.MostrarTablas(base)
    
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
        self.db_connection = mysql.connector.connect(host=self.ServerName.get(),  
        user=self.UserName.get(),  
        password=self.PassName.get())
        self.db_cursor = self.db_connection.cursor(buffered=True)
        if self.db_connection.is_connected() == False:  
            self.db_connection.connect() 

        if self.db_connection.is_connected():
                self.labelStsServer.config(text="Conectado", foreground="green")
        else:
                self.labelStsServer.config(text="Sin Conexion", foreground="red")

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

    def ventanachica(self):
        self.ventana1.geometry("640x480")

    def ventanagrande(self):
        self.ventana1.geometry("1024x800")

AdminDb1=AdminDb()
