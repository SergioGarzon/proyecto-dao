from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import platform
import platform
import os
from PIL import ImageTk, Image
from Controlador.controlador_socio import ControladorSocio
from Vistas.socios.insercion_socios import InsercionSocios

class PantallaReportesGenerales:
    
    def __init__(self):
        self.windows_reportes = tk.Toplevel()
        self.windows_properties()
        self.windows_components()          
    
    def windows_properties(self):
        self.windows_reportes.title("Proyecto DAO")
        self.windows_reportes.geometry("800x650")
        self.windows_reportes.configure(bg="lightyellow")
        self.windows_reportes.resizable(False, False)
        
    def windows_components(self):
        frame_5 = tk.Frame(self.windows_reportes)   
        frame_5.configure(bg="lightyellow") 
        
        label_name_form = tk.Label(frame_5, text="Reportes Generales")
        label_reportes_data = tk.Label(frame_5, text="En esta seccion podremos ver diferentes reportes del sistema, \npara visualizar reportes, se debe hacer click en el boton correspondiente \nal reporte que se quiera visualizar")
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))
            label_reportes_data.config(fg="black", bg="lightyellow", font=("Arial", 15))
            btn_prestamos_activos = tk.Button(frame_5, text="Prestamos activos", cursor="Hand2")
            btn_prestamos_vencidos = tk.Button(frame_5, text="Prestamos vencidos", cursor="Hand2")
            btn_material_transito = tk.Button(frame_5, text="Material en transito", cursor="Hand2")
            btn_multas_acumuladas = tk.Button(frame_5, text="Multas acumuladas", cursor="Hand2")
            btn_salir = tk.Button(frame_5, text="Salir de reportes", cursor="Hand2")
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")
            label_reportes_data.config(fg="black", bg="lightyellow")  
            btn_prestamos_activos = tk.Button(frame_5, text="Prestamos activos")
            btn_prestamos_vencidos = tk.Button(frame_5, text="Prestamos vencidos")
            btn_material_transito = tk.Button(frame_5, text="Material en transito")
            btn_multas_acumuladas = tk.Button(frame_5, text="Multas acumuladas")
            btn_salir = tk.Button(frame_5, text="Salir de reportes") 
         
        btn_prestamos_activos.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        #btn_prestamos_activos.config(command=self.)  
        
        btn_prestamos_vencidos.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        #btn_prestamos_activos.config(command=self.)     
        
        btn_multas_acumuladas.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        #btn_prestamos_activos.config(command=self.)  
        
        btn_material_transito.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        #btn_material_transito.config(command=self.)      
           
        btn_salir.config(fg="white", bg="red", font=("Arial", 15, "bold"))  
        btn_salir.config(command=self.cerrar_ventana)      
        
        dir_reportes = os.path.dirname(os.path.abspath(__file__))
        dir_vistas = os.path.dirname(dir_reportes)                 
        root_dir = os.path.dirname(dir_vistas)                     
        
        image_path = os.path.join(root_dir, "Recursos", "reportes_imagen.png")
        
        image_open = Image.open(image_path)
        image_open = ImageTk.PhotoImage(image_open)
                            
        image_label = tk.Label(frame_5, image=image_open)
        image_label.image = image_open 
                
        frame_5.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack(pady=5)
        label_reportes_data.pack(pady=15)
        image_label.pack(pady=10, side="left")
        btn_prestamos_activos.pack()
        btn_prestamos_vencidos.pack()
        btn_material_transito.pack()
        btn_multas_acumuladas.pack()
        btn_salir.pack()
                       
        
    # Metodo para el boton que cierra la ventana
    def cerrar_ventana(self):
        self.windows_reportes.destroy()
        
       