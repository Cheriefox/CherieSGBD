import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import mysql.connector
import configparser
import os
import tkinter.messagebox as msgbox

BASES=[]
TABLAS=[]


class SqlFrame(ttk.Frame):

    def __init__(self, admin_db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_db = admin_db  # Recibe la instancia de AdminDb
        
        self.etiq = ttk.Label(self)
        self.etiq["text"] = ("Ingresar query")
        self.etiq.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Caja de texto para el query
        self.sql_txt = ttk.Entry(self)
        self.sql_txt.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Botón para ejecutar la consulta
        self.sql_button = ttk.Button(self, text="Ejecutar", command=self.ejecutar_query)
        self.sql_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        # Configuramos el layout para que las filas y columnas se ajusten
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # Crear un Treeview para mostrar los resultados dentro de esta pestaña
        self.result_tree = ttk.Treeview(self, show="headings")  # Inicializar el Treeview
        self.result_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Ubicar el Treeview debajo del formulario

        # Barra de desplazamiento vertical
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.result_tree.yview)
        self.scrollbar_y.grid(row=1, column=3, sticky="ns")  # Barra de desplazamiento vertical
        self.result_tree.configure(yscrollcommand=self.scrollbar_y.set)

        # Barra de desplazamiento horizontal
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.result_tree.xview)
        self.scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")  # Barra de desplazamiento horizontal
        self.result_tree.configure(xscrollcommand=self.scrollbar_x.set)

        # Configuramos la fila para que el Treeview ocupe el espacio disponible
        self.grid_rowconfigure(1, weight=1)

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
        # Limpiar el Treeview antes de mostrar nuevos resultados
        self.result_tree.delete(*self.result_tree.get_children())  # Elimina todas las filas actuales

        if not rows:
            showinfo("Resultado", "No se encontraron resultados.")
        else:
            # Obtener los nombres de las columnas (usando description del cursor)
            column_names = [desc[0] for desc in self.admin_db.db_cursor.description]

            # Configurar las columnas dinámicamente según los nombres de las columnas en la consulta SELECT
            self.result_tree["columns"] = column_names  # Usamos los nombres de las columnas

            # Configurar las cabeceras de las columnas
            for col in column_names:
                self.result_tree.heading(col, text=col)  # Usamos los nombres reales de las columnas
                self.result_tree.column(col, stretch=True, anchor="w")  # Permitir que las columnas se estiren automáticamente

            # Insertar los datos en las filas
            for row in rows:
                self.result_tree.insert("", "end", values=row)

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
        
        self.cargar_configuracion()
        

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
        self.ServerName.insert(0, self.config['database']['host'])  # Configuración desde el archivo
        self.ServerName.grid(row=0, column=1, padx=10, pady=10)
        
        labelUser = ttk.Label(conn_frame, text="Usuario:")
        labelUser.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.UserName = ttk.Entry(conn_frame)
        self.UserName.insert(0, self.config['database']['user'])  # Configuración desde el archivo
        self.UserName.grid(row=1, column=1, padx=10, pady=10)
        
        labelPass = ttk.Label(conn_frame, text="Password:")
        labelPass.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.PassName = ttk.Entry(conn_frame, show="*")
        self.PassName.insert(0, self.config['database']['password'])  # Configuración desde el archivo
        self.PassName.grid(row=2, column=1, padx=10, pady=10)

        labelPuerto = ttk.Label(conn_frame, text="Puerto:")
        labelPuerto.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.PuertoName = ttk.Entry(conn_frame)
        self.PuertoName.insert(0, self.config['database']['port'])  # Configuración desde el archivo
        self.PuertoName.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        botonConn = ttk.Button(conn_frame, text="Conectar", command=self.ConectarServidor)
        botonConn.grid(row=4, column=1, padx=10, pady=10)

        self.labelStsServer = ttk.Label(conn_frame, text="Sin Conexion", foreground="red")
        self.labelStsServer.grid(row=4, column=2, padx=10, pady=10, sticky="w")


        # Ajustamos el espacio para que el botón de ayuda esté al fondo
        conn_frame.grid_rowconfigure(4, weight=1)  # Hace que la fila 4 sea expansible

        # Agregar el botón de Ayuda
        botonAyuda = ttk.Button(conn_frame, text="Ayuda", command=self.abrir_ayuda)
        botonAyuda.grid(row=4, column=0, padx=10, pady=10, sticky="w")  # Colocamos el botón en la fila 5


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

    def cargar_configuracion(self):
        """Carga la configuración desde el archivo .ini y la asigna a self.config."""
        config = configparser.ConfigParser()
        try:
            # Cargar el archivo de configuración
            config.read('config.ini')

            # Guardar la configuración en self.config
            self.config = config

            # Aquí puedes asegurarte de que los valores son correctos (opcional)
            print(f"Servidor: {self.config['database']['host']}")
            print(f"Usuario: {self.config['database']['user']}")

        except Exception as e:
            print(f"Error al leer el archivo de configuración: {e}")
            self.config = {}  # Definir una configuración vacía si hay un error.

    def crear_widgets(self):
        """Crear los widgets utilizando self.config."""
        conn_frame = ttk.Frame(self.ventana1)
        conn_frame.grid(row=0, column=0, padx=10, pady=10)

        labelSrv = ttk.Label(conn_frame, text="Servidor:")
        labelSrv.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ServerName = ttk.Entry(conn_frame)
        self.ServerName.insert(0, self.config['database']['host'])  # Configuración desde el archivo
        self.ServerName.grid(row=0, column=1, padx=10, pady=10)

        labelUser = ttk.Label(conn_frame, text="Usuario:")
        labelUser.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.UserName = ttk.Entry(conn_frame)
        self.UserName.insert(0, self.config['database']['user'])  # Configuración desde el archivo
        self.UserName.grid(row=1, column=1, padx=10, pady=10)

        labelPass = ttk.Label(conn_frame, text="Password:")
        labelPass.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.PassName = ttk.Entry(conn_frame, show="*")
        self.PassName.insert(0, self.config['database']['password'])  # Configuración desde el archivo
        self.PassName.grid(row=2, column=1, padx=10, pady=10)

        labelPuerto = ttk.Label(conn_frame, text="Puerto:")
        labelPuerto.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.PuertoName = ttk.Entry(conn_frame)
        self.PuertoName.insert(0, self.config['database']['port'])  # Configuración desde el archivo
        self.PuertoName.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def abrir_ayuda(self):
        """Función para abrir el archivo de ayuda en formato .docx."""
        try:
            # Aquí debes poner la ruta de tu archivo .docx de ayuda
            archivo_ayuda = "CherieSGBD.docx"
            
            if os.path.exists(archivo_ayuda):
                os.startfile(archivo_ayuda)  # Windows
                # Para Mac o Linux, usa el siguiente:
                # os.system(f'open "{archivo_ayuda}"')  # Mac
                # os.system(f'xdg-open "{archivo_ayuda}"')  # Linux
            else:
                msgbox.showerror("Error", "El archivo de ayuda no se encuentra.")
        except Exception as e:
            msgbox.showerror("Error", f"No se pudo abrir el archivo de ayuda: {str(e)}")


    def ConectarServidor(self):
        # Utilizar los valores del archivo de configuración para la conexión
        try:
            self.db_connection = mysql.connector.connect(
                host=self.ServerName.get(),
                user=self.UserName.get(),
                password=self.PassName.get(),
                port=self.PuertoName.get()
            )
            self.db_cursor = self.db_connection.cursor(buffered=True)
            if self.db_connection.is_connected():
                self.labelStsServer.config(text="Conectado", foreground="green")
            else:
                self.labelStsServer.config(text="Sin Conexion", foreground="red")
        except mysql.connector.Error as err:
            showinfo("Error", f"Error al conectar: {err}")
            self.labelStsServer.config(text="Error de conexión", foreground="red")

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
