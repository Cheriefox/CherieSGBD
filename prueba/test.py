import mysql.connector

cnn = mysql.connector.connect(host="localhost", user="root",passwd="Camapared21", database="escuelapy")

def consulta_alumnos():
    cur = cnn.cursor()
    cur.execute("SELECT * FROM  alumnos WHERE Apellido = 'Chamorro' ")
    datos = cur.fetchall()
    cur.close()
    cnn.close()
    return datos

def inserta_alumnos():
    cur = cnn.cursor()
    sql = "INSERT INTO alumnos (Nombre, Apellido, Edad, DNI) VALUES ('Gonzalo', 'Montenegro', 17, 48097928);"
    try:
        cur.execute(sql)
        n = cur.rowcount
        cnn.commit()
    except Exception as e:
        print(f"Error al insertar: {e}")
        n = 0  # O algún valor que indique fallo
    finally:
        cur.close()
    return n


def borrar_alumno(id_alumno):
    cur = cnn.cursor()
    try:
        cur.execute("DELETE FROM alumnos WHERE Id = %s", (id_alumno,))
        n = cur.rowcount  
        cnn.commit()  
    except Exception as e:
        print(f"Error al borrar el alumno: {e}")
        n = 0  
    finally:
        cur.close()
    return n  

def editar_alumno(id_alumno):
    cur = cnn.cursor()
    try:
        cur.execute("UPDATE alumnos SET DNi=46097928 WHERE Id = %s", (id_alumno,))
        n = cur.rowcount  
        cnn.commit()  
    except Exception as e:
        print(f"Error al borrar el alumno: {e}")
        n = 0  
    finally:
        cur.close()
    return n  

print(editar_alumno(1))

print(borrar_alumno(4))
 
print(inserta_alumnos())

tabla = consulta_alumnos()
for fila in tabla:
    print(fila)
