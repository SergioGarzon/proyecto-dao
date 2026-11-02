import tkinter as tk
from tkinter import ttk
import platform
import os
from tkinter import messagebox

class PantallaGestionSede:
    
    def __init__(self):
        self.windows_gestion_sede = tk.Toplevel() 
        self.windows_properties()
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_gestion_sede.title("Proyecto DAO")
        self.windows_gestion_sede.geometry("1100x580")
        self.windows_gestion_sede.configure(bg="lightyellow")
        self.windows_gestion_sede.resizable(False, False)
        
    def windows_components(self):
        frame_3 = tk.Frame(self.windows_gestion_sede)   
        frame_3.configure(bg="lightyellow") 
        
        label_name_form = tk.Label(frame_3, text="Gestión de Sedes")
        label_nombre_sede_buscar = tk.Label(frame_3, text="Ingrese el nombre de la Sede:")
        self.textbox_nombre_sede = tk.Entry(frame_3, font=("Arial", 14), width=30)
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))   
            label_nombre_sede_buscar.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            btn_actualizar_sede = tk.Button(frame_3, text="Actualizar tabla de sedes", cursor="Hand2")
            btn_buscar_sede = tk.Button(frame_3, text="Buscar sede", cursor="Hand2")  
            btn_insertar_datos_sedes = tk.Button(frame_3, text="Crear sedes", cursor="Hand2") 
            btn_eliminar_sede = tk.Button(frame_3, text="Eliminar sedes", cursor="Hand2")
            btn_cerrar = tk.Button(frame_3, text="Cerrar ventana", cursor="Hand2")                                      
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")       
            label_nombre_sede_buscar.config(fg="black", bg="lightyellow")  
            btn_actualizar_sede = tk.Button(frame_3, text="Actualizar tabla de sedes")
            btn_buscar_sede = tk.Button(frame_3, text="Buscar sede")
            btn_insertar_datos_sedes = tk.Button(frame_3, text="Crear sedes") 
            btn_eliminar_sede = tk.Button(frame_3, text="Eliminar sedes")
            btn_cerrar = tk.Button(frame_3, text="Cerrar ventana")  
        
        btn_buscar_sede.config(fg="white", bg="blue", font=("Arial", 15, "bold"))  
        #btn_buscar_sede.config(command=self.) 
        
        btn_actualizar_sede.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        #btn_actualizar_sede.config(command=self.)
        
        btn_insertar_datos_sedes.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        #btn_insertar_datos_sedes.config(command=self.) 
        
        btn_eliminar_sede.config(fg="white", bg="orange", font=("Arial", 15, "bold"))  
        #btn_eliminar_sede.config(command=self.)  
        
        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))  
        #btn_cerrar.config(command=self.)  
        
        columnas = ("Codigo_sede", "Nombre", "Direccion_calle_altura", "Barrio", "Localidad", "Telefono", "Email", "Hora_apertura", "Hora_cierre", "Estado")
                
        self.tabla = ttk.Treeview(frame_3, columns=columnas, show="headings")
                
        self.tabla.heading("Codigo_sede", text="Código de Sede")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Direccion_calle_altura", text="Dirección")
        self.tabla.heading("Barrio", text="Barrio")
        self.tabla.heading("Localidad", text="Localidad")
        self.tabla.heading("Telefono", text="Teléfono")
        self.tabla.heading("Email", text="Email")
        self.tabla.heading("Hora_apertura", text="Hora de Apertura")
        self.tabla.heading("Hora_cierre", text="Hora de Cierre")
        self.tabla.heading("Estado", text="Estado")
                
        self.tabla.column("Codigo_sede", width=80, anchor="center")
        self.tabla.column("Nombre", width=120, anchor="w")
        self.tabla.column("Direccion_calle_altura", width=120, anchor="center")
        self.tabla.column("Barrio", width=100, anchor="center")
        self.tabla.column("Localidad", width=100, anchor="center")
        self.tabla.column("Telefono", width=100, anchor="center")
        self.tabla.column("Email", width=120, anchor="center")
        self.tabla.column("Hora_apertura", width=100, anchor="center")
        self.tabla.column("Hora_cierre", width=100, anchor="center")
        self.tabla.column("Estado", width=80, anchor="center")
                
        
        frame_3.pack()
        label_name_form.pack()
        label_nombre_sede_buscar.pack(pady=5)
        self.textbox_nombre_sede.pack(pady=5)
        btn_buscar_sede.pack(pady=5)
        btn_actualizar_sede.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=15)
        btn_eliminar_sede.pack(pady=10, side="right")
        btn_insertar_datos_sedes.pack(pady=10, side="right")
        btn_cerrar.pack(side="left")
            