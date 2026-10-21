from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
import os
from PIL import ImageTk, Image

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
        
        opciones_reporte = ["Reporte de prestamos activos", "Reporte de prestamos vencidos", "Reporte de multas acumuladas", "Reporte de material de transito"]
                
        frame_derecho = tk.Frame(frame_5, bg="lightyellow")
        
        cmb_reporte = ttk.Combobox(frame_derecho, values=opciones_reporte, state="readonly", width=40)
        cmb_reporte.current(0)
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))
            label_reportes_data.config(fg="black", bg="lightyellow", font=("Arial", 15))
            btn_generar_reporte = tk.Button(frame_derecho, text="Generar reporte", cursor="Hand2")
            btn_salir = tk.Button(frame_derecho, text="Salir de reportes", cursor="Hand2")            
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")
            label_reportes_data.config(fg="black", bg="lightyellow")  
            btn_generar_reporte = tk.Button(frame_derecho, text="Generar reporte")
            btn_salir = tk.Button(frame_derecho, text="Salir de reportes") 
             
        btn_generar_reporte.config(fg="white", bg="green", font=("Arial", 15, "bold"))   
           
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
        
        image_label.pack(side="left", padx=40, pady=10)
        frame_derecho.pack(side="right", expand=True, fill=tk.BOTH, pady=40)
        
        cmb_reporte.pack(pady=20)
        btn_generar_reporte.pack(pady=20)
        btn_salir.pack(pady=20)
        
    # Metodo para el boton que cierra la ventana
    def cerrar_ventana(self):
        self.windows_reportes.destroy()
        
       