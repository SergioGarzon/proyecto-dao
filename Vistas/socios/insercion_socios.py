from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import platform
from Controlador.controlador_socio import ControladorSocio
from Entidades.excepciones import ReglaNegocioError

class InsercionSocios:
    
    def __init__(self, al_guardar=None, datos=None):
        self.windows_insercion_socio = tk.Toplevel() 
        self.windows_properties()
        
        self.controlador_socios = ControladorSocio()
        # Con datos, el formulario edita un socio existente; sin datos, da de alta uno nuevo
        self.datos = datos
        # Función que se llama después de guardar (para refrescar la tabla de gestión)
        self.al_guardar = al_guardar
        
        self.windows_components()
        if self.datos:
            self.precargar_datos()
    
    def windows_properties(self):
        self.windows_insercion_socio.title("Proyecto DAO")
        self.windows_insercion_socio.geometry("800x550")
        self.windows_insercion_socio.configure(bg="lightyellow")
        self.windows_insercion_socio.resizable(False, False)
        
    def windows_components(self):
        frame_5 = tk.Frame(self.windows_insercion_socio)   
        datos_edicion = self.datos is not None
        texto_confirmar = "Guardar cambios" if datos_edicion else "Confirmar creación"
        frame_5.configure(bg="lightyellow") 
            
        label_name_form = tk.Label(frame_5, text="Modificación de Socio" if datos_edicion else "Creacion de Socios")
        
        label_legajo = tk.Label(frame_5, text="Ingrese el legajo:")
        self.textbox_legajo_socio = tk.Entry(frame_5, font=("Arial", 14), width=30)
        
        label_nombre = tk.Label(frame_5, text="Ingrese el nombre:")
        self.textbox_nombre_socio = tk.Entry(frame_5, font=("Arial", 14), width=30)
        
        label_apellido = tk.Label(frame_5, text="Ingrese el apellido:")
        self.textbox_apellido_socio = tk.Entry(frame_5, font=("Arial", 14), width=30)
                 
        label_fecha_inscripcion = tk.Label(frame_5, text="Ingrese la fecha de inscripcion (AAAA-MM-DD):")
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
            btn_insertar_datos = tk.Button(frame_5, text=texto_confirmar, cursor="Hand2")   
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
            btn_insertar_datos = tk.Button(frame_5, text=texto_confirmar)
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

    def precargar_datos(self):
        campos = ((self.textbox_legajo_socio, "legajo"), (self.textbox_nombre_socio, "nombre"),
                  (self.textbox_apellido_socio, "apellido"), (self.textbox_fecha_inscripcion, "fecha"),
                  (self.textbox_domicilio, "domicilio"), (self.textbox_barrio, "barrio"),
                  (self.textbox_localidad, "localidad"))
        for textbox, clave in campos:
            textbox.insert(0, self.datos[clave])
        # El legajo es la clave del socio: no se puede cambiar
        self.textbox_legajo_socio.config(state="disabled")

    def insertar_socio(self):
        legajo = self.textbox_legajo_socio.get()
        valores = (self.textbox_nombre_socio.get(), self.textbox_apellido_socio.get(),
                   self.textbox_fecha_inscripcion.get(), self.textbox_domicilio.get(),
                   self.textbox_barrio.get(), self.textbox_localidad.get())

        if not str(legajo).strip() or any(not str(valor).strip() for valor in valores):
            messagebox.showerror("Error", "Faltan llenar datos! No se puede guardar el socio",
                                 parent=self.windows_insercion_socio)
            return

        try:
            if self.datos:
                self.controlador_socios.modificar_socio(legajo, *valores)
            else:
                self.controlador_socios.insertar_socio(legajo, *valores)
        except ReglaNegocioError as error:
            messagebox.showerror("Error", str(error), parent=self.windows_insercion_socio)
            return

        if self.al_guardar:
            self.al_guardar()

        if self.datos:
            messagebox.showinfo("Información", "Socio modificado correctamente!", parent=self.windows_insercion_socio)
            self.cerrar_ventana()
            return

        messagebox.showinfo("Información", "Socio insertado correctamente!", parent=self.windows_insercion_socio)
        for textbox in (self.textbox_legajo_socio, self.textbox_nombre_socio, self.textbox_apellido_socio,
                        self.textbox_fecha_inscripcion, self.textbox_domicilio, self.textbox_barrio,
                        self.textbox_localidad):
            textbox.delete(0, tk.END)
