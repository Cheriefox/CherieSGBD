from tkinter import *
from tkinter import ttk
from alumnos import alumnos

class Ventana(Frame):

    alumno=alumnos()


    def __init__(self, master=None):
        super().__init__(master, width=700, height=260)
        self.master = master
        self.pack()
        self.create_widgets()
        self.llenadatos()

    def llenadatos(self):
        datos = self.alumno.consulta_alumnos()
        for row in datos:
            print()
            self.grid.insert("", END, text=row[0],values=(row[1],row[2],row[3],row[4]))

    def fNuevo():
        pass
       
        
       

    def fModificar(self):
        pass

    def fEliminar(self):
        pass
    def fGuardar(self):
        pass
    def fCancelar(self):
        pass
    def create_widgets(self):
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93,height=259)

        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80,height=30)
     
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80,height=30)
     
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80,height=30)

        frame2 = Frame(self, bg="#d3dde3")
        frame2.place(x=93,y=0,width=150,height=259)

        lbl1 = Label(frame2,text="Nombre: ")
        lbl1.place(x=3,y=5)
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=25,width=100, height=20)


        lbl2 = Label(frame2,text="Apellido: ")
        lbl2.place(x=3,y=55)
        self.txtApellido=Entry(frame2)
        self.txtApellido.place(x=3,y=75,width=100, height=20)

        lbl3 = Label(frame2,text="Edad: ")
        lbl3.place(x=3,y=105)
        self.txtEdad=Entry(frame2)
        self.txtEdad.place(x=3,y=125,width=100, height=20)

        lbl4 = Label(frame2,text="DNI: ")
        lbl4.place(x=3,y=155)
        self.txtDNI=Entry(frame2)
        self.txtDNI.place(x=3,y=175,width=100, height=20)

        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=210,width=60,height=30)
     
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=210,width=60,height=30)

        self.grid = ttk.Treeview(self, columns=("col1","col2","col3","col4"))

        self.grid.column("#0",width=50)
        self.grid.column("col1",width=60, anchor=CENTER)
        self.grid.column("col2",width=90, anchor=CENTER)
        self.grid.column("col3",width=90, anchor=CENTER)
        self.grid.column("col4",width=90, anchor=CENTER)

        self.grid.heading("#0",text="id", anchor=CENTER)
        self.grid.heading("col1",text="Nombre", anchor=CENTER)
        self.grid.heading("col2",text="Apellido", anchor=CENTER)
        self.grid.heading("col3",text="Edad", anchor=CENTER)
        self.grid.heading("col4",text="DNI", anchor=CENTER)

        self.grid.place(x=247,y=0,width=420,height=259)

        
