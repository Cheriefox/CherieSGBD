import mysql.connector

class alumnos:
    def __init__(self):
        self.cnn = mysql.connector.connect(host="localhost", user="root",passwd="Camapared21", database="escuelapy")
    
    def __str__(self):
        datos=self.consulta_alumnos()
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux


    def consulta_alumnos(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM  alumnos  ")
        datos = cur.fetchall()
        cur.close()
        self.cnn.close()
        return datos
    
    def inserta_alumnos(self, nombre, apellido, edad, dni):
        cur = self.cnn.cursor()
        sql = "INSERT INTO alumnos (Nombre, Apellido, Edad, DNI) VALUES (%s, %s, %s, %s);"
        try:
            cur.execute(sql, (nombre, apellido, edad, dni))
            n = cur.rowcount
            self.cnn.commit()
        except Exception as e:
            print(f"Error al insertar: {e}")
            n = 0
        finally:
            cur.close()
        return n


    def borrar_alumno(self,id_alumno):
        cur = self.cnn.cursor()
        try:
            cur.execute("DELETE FROM alumnos WHERE Id = %s", (id_alumno,))
            n = cur.rowcount  
            self.cnn.commit()  
        except Exception as e:
            print(f"Error al borrar el alumno: {e}")
            n = 0  
        finally:
            cur.close()
        return n  

    def editar_alumno(self, id_alumno, Nombre, Apellido, Edad, DNI):
        cur = self.cnn.cursor()
        try:
            cur.execute("UPDATE alumnos SET Nombre=%s, Apellido=%s, Edad=%s, DNI=%s WHERE Id = %s",(Nombre, Apellido, Edad, DNI, id_alumno))
            n = cur.rowcount  
            self.cnn.commit()  
        except Exception as e:
            print(f"Error al borrar el alumno: {e}")
            n = 0  
        finally:
            cur.close()
        return n  