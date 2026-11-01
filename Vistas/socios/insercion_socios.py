from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import platform
from Controlador.controlador_socio import ControladorSocio

class InsercionSocios:
    
    def __init__(self):
        self.windows_insercion_socio = tk.Toplevel() 
        self.windows_properties()
        
        # esto despues lo sacamos, porque es para crear la tabla, pero solo una igual
        self.controlador_socios = ControladorSocio()
        
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_insercion_socio.title("Proyecto DAO")
        self.windows_insercion_socio.geometry("800x550")
        self.windows_insercion_socio.configure(bg="lightyellow")
        self.windows_insercion_socio.resizable(False, False)
        
    def windows_components(self):
        frame_5 = tk.Frame(self.windows_insercion_socio)   
        frame_5.configure(bg="lightyellow") 
            
        label_name_form = tk.Label(frame_5, text="Creacion de Socios")
        
        label_legajo = tk.Label(frame_5, text="Ingrese el legajo:")
        self.textbox_legajo_socio = tk.Entry(frame_5, font=("Arial", 14), width=30)
        
        label_nombre = tk.Label(frame_5, text="Ingrese el nombre:")
        self.textbox_nombre_socio = tk.Entry(frame_5, font=("Arial", 14), width=30)
        
        label_apellido = tk.Label(frame_5, text="Ingrese el apellido:")
        self.textbox_apellido_socio = tk.Entry(frame_5, font=("Arial", 14), width=30)
                 
        label_fecha_inscripcion = tk.Label(frame_5, text="Ingrese la fecha de inscripcion:")
        self.textbox_fecha_inscripcion = tk.Entry(frame_5, font=("Arial", 14), width=30)
        
        label_domicilio = tk.Label(frame_5, text="Ingrese el domicilio:")
        self.textbox_domicilio = tk.Entry(frame_5, font=("Arial", 14), width=30)
                
        label_barrio = tk.Label(frame_5, text="Ingrese el barrio:")
        self.textbox_barrio = tk.Entry(frame_5, font=("Arial", 14), width=30)
                
        label_localidad = tk.Label(frame_5, text="Ingrese la localidad:")
        self.textbox_localidad = tk.Entry(frame_5, font=("Arial", 14), width=30)                
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))   
            label_legajo.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            label_nombre.config(fg="black", bg="lightyellow", font=("Arial", 15))   
            label_apellido.config(fg="black", bg="lightyellow", font=("Arial", 15))     
            label_fecha_inscripcion.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            label_domicilio.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            label_barrio.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            label_localidad.config(fg="black", bg="lightyellow", font=("Arial", 15)) 
            btn_insertar_datos = tk.Button(frame_5, text="Confirmar creación", cursor="Hand2")   
            btn_cerrar = tk.Button(frame_5, text="Cerrar ventana", cursor="Hand2")              
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")    
            label_legajo.config(fg="black", bg="lightyellow")  
            label_nombre.config(fg="black", bg="lightyellow")   
            label_apellido.config(fg="black", bg="lightyellow")
            label_fecha_inscripcion.config(fg="black", bg="lightyellow")
            label_domicilio.config(fg="black", bg="lightyellow")
            label_barrio.config(fg="black", bg="lightyellow")
            label_localidad.config(fg="black", bg="lightyellow")
            btn_insertar_datos = tk.Button(frame_5, text="Confirmar creación")
            btn_cerrar = tk.Button(frame_5, text="Cerrar ventana")                   
            
        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))  
        btn_cerrar.config(command=self.cerrar_ventana)  
        
        btn_insertar_datos.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        btn_insertar_datos.config(command=self.insertar_socio)  
                
        frame_5.pack()
        label_name_form.pack()
        label_legajo.pack()
        self.textbox_legajo_socio.pack()
        label_nombre.pack()
        self.textbox_nombre_socio.pack()
        label_apellido.pack()
        self.textbox_apellido_socio.pack()
        label_fecha_inscripcion.pack()
        self.textbox_fecha_inscripcion.pack()
        label_domicilio.pack()
        self.textbox_domicilio.pack()
        label_barrio.pack()
        self.textbox_barrio.pack()
        label_localidad.pack()
        self.textbox_localidad.pack()         
        btn_insertar_datos.pack()
        btn_cerrar.pack()
                

    def cerrar_ventana(self):
        self.windows_insercion_socio.destroy()

    def insertar_socio(self):
        legajo = self.textbox_legajo_socio.get()
        nombre = self.textbox_nombre_socio.get()
        apellido = self.textbox_apellido_socio.get()
        fecha = self.textbox_fecha_inscripcion.get()
        domicilio = self.textbox_domicilio.get()
        barrio = self.textbox_barrio.get()
        localidad = self.textbox_localidad.get()
        
        if str(legajo) != "" and str(nombre) != "" and str(apellido) != "" and str(fecha) != "" and str(domicilio) != "" and str(barrio) != "" and str(localidad) != "":
            
            # Vamos a verificar si el socio ya existe, con ese legajo
            
            query_sql = f"SELECT * FROM socios WHERE legajo_dni = {legajo}"
            
            lista_devuelta = self.controlador_socios.consultar_socios(query_sql)
            
            if len(lista_devuelta) != 0:
                messagebox.showwarning("Advertencia", "Ya existe un usuario con el legajo ingresado, no se puede cargar el mismo!")
                return         
            
            insert_sql = f'''
                INSERT INTO socios(legajo_dni, nombre, apellido, fecha_inscripcion, domicilio_calle, barrio, localidad, estado_socio) 
                VALUES({legajo}, '{nombre}', '{apellido}', '{fecha}', '{domicilio}', '{barrio}', '{localidad}', 'Activo')
                '''
            
            self.controlador_socios.insertar_socios(insert_sql)
            
            messagebox.showinfo("Información", "Socio insertado correctamente!")
        
            self.textbox_legajo_socio.delete(0, tk.END)
            self.textbox_nombre_socio.delete(0, tk.END)
            self.textbox_apellido_socio.delete(0, tk.END)
            self.textbox_fecha_inscripcion.delete(0, tk.END)
            self.textbox_domicilio.delete(0, tk.END)
            self.textbox_barrio.delete(0, tk.END)
            self.textbox_localidad.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Faltan llenar datos! No se puede insertar ningun usuario")
    
    