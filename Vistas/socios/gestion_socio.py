from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
from Controlador.controlador_socio import ControladorSocio
from Vistas.socios.insercion_socios import InsercionSocios

class PantallaGestionSocio:
    
    def __init__(self):
        self.windows_gestion_socio = tk.Toplevel() 
        self.windows_properties()
        
        # esto despues lo sacamos, porque es para crear la tabla, pero solo una igual
        self.controlador_socios = ControladorSocio()
        
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_gestion_socio.title("Proyecto DAO")
        self.windows_gestion_socio.geometry("800x650")
        self.windows_gestion_socio.configure(bg="lightyellow")
        self.windows_gestion_socio.resizable(False, False)
        
    def windows_components(self):
        frame_4 = tk.Frame(self.windows_gestion_socio)   
        frame_4.configure(bg="lightyellow") 
        
        label_name_form = tk.Label(frame_4, text="Gestión de Socios")
        label_socio_legajo_buscar = tk.Label(frame_4, text="Ingrese el legajo del Socio:")
        textbox_legajo_socio = tk.Entry(frame_4, font=("Arial", 14), width=30)
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))     
            label_socio_legajo_buscar.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            btn_buscar_socio = tk.Button(frame_4, text="Buscar socio", cursor="Hand2")                                      
            btn_actualizar = tk.Button(frame_4, text="Actualizar tabla de socios", cursor="Hand2")
            btn_insertar_datos_socios = tk.Button(frame_4, text="Crear socios", cursor="Hand2") 
            btn_cerrar = tk.Button(frame_4, text="Cerrar ventana", cursor="Hand2") 
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")
            label_socio_legajo_buscar.config(fg="black", bg="lightyellow") 
            btn_buscar_socio = tk.Button(frame_4, text="Buscar socio") 
            btn_actualizar = tk.Button(frame_4, text="Actualizar tabla de socios")  
            btn_insertar_datos_socios = tk.Button(frame_4, text="Crear socios") 
            btn_cerrar = tk.Button(frame_4, text="Cerrar ventana")          
        
        btn_buscar_socio.config(fg="white", bg="blue", font=("Arial", 15, "bold"))  
        
        columnas = ("Legajo", "Nombre", "Apellido", "Fecha_Inscripcion", "Domicilio", "Barrio", "Localidad", "Estado")
        
        self.tabla = ttk.Treeview(frame_4, columns=columnas, show="headings")
        
        self.tabla.heading("Legajo", text="Legajo Socio")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Fecha_Inscripcion", text="Fecha de Inscripcion")
        self.tabla.heading("Domicilio", text="Domicilio")
        self.tabla.heading("Barrio", text="Barrio")
        self.tabla.heading("Localidad", text="Localidad")
        self.tabla.heading("Estado", text="Estado")
        
        self.tabla.column("Legajo", width=60, anchor="center")
        self.tabla.column("Nombre", width=120, anchor="w")
        self.tabla.column("Apellido", width=120, anchor="center")
        self.tabla.column("Fecha_Inscripcion", width=120, anchor="center")
        self.tabla.column("Domicilio", width=100, anchor="center")
        self.tabla.column("Barrio", width=100, anchor="center")
        self.tabla.column("Localidad", width=100, anchor="center")
        self.tabla.column("Estado", width=80, anchor="center")
        
        # Traemos los datos de la base de datos
        self.actualizar_tabla()
        
        btn_actualizar.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        btn_actualizar.config(command=self.actualizar_tabla)  
        
        btn_insertar_datos_socios.config(fg="white", bg="blue", font=("Arial", 15, "bold"))  
        btn_insertar_datos_socios.config(command=self.insertar_informacion)          
        
        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))  
        btn_cerrar.config(command=self.cerrar_ventana)  
                
        frame_4.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack(pady=5)
        label_socio_legajo_buscar.pack(pady=5)
        textbox_legajo_socio.pack(pady=5)
        btn_buscar_socio.pack(pady=5) 
        btn_actualizar.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=15)
        btn_insertar_datos_socios.pack(pady=10)
        btn_cerrar.pack()
                
        
    def consultar_datos(self):
        query_ejemplo = "SELECT legajo_dni, nombre, apellido, fecha_inscripcion, domicilio_calle, barrio, localidad, estado_socio FROM socios"
        lista_resultados = self.controlador_socios.consultar_socios(query_ejemplo)  
        return lista_resultados      

    def actualizar_tabla(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)
            
        lista_resultados = self.consultar_datos()
        
        for fila in lista_resultados:
            self.tabla.insert("", tk.END, values=fila)

    def insertar_informacion(self):
        InsercionSocios()
    
    def cerrar_ventana(self):
        self.windows_gestion_socio.destroy()
        
       
