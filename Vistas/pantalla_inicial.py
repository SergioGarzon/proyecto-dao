import tkinter as tk
import platform
import os
from tkinter import messagebox

from Vistas.sedes.gestion_sede import PantallaGestionSede
from Vistas.socios.gestion_socio import PantallaGestionSocio

# Instalar PILLOW 'pip install pillow'
from PIL import ImageTk, Image

class PantallaInicial:
    
    def __init__(self):
        self.windows_inicial = tk.Tk()
        self.windows_properties()
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_inicial.title("Proyecto DAO")
        self.windows_inicial.geometry("1200x650")
        self.windows_inicial.configure(bg="lightyellow")
        self.windows_inicial.resizable(False, False)
        
    def windows_components(self):
        frame_2 = tk.Frame(self.windows_inicial)   
        frame_2.configure(bg="lightyellow") 
            
        label_name_subject = tk.Label(frame_2, text="Biblioteca de Prestamos a Socios")                     
            
        if str(platform.system()) == "Windows":
            label_name_subject.config(fg="black", bg="lightyellow", font=("Arial", 25))                    
            btn_gestion_sedes = tk.Button(self.windows_inicial, text="Gestionar Sedes", cursor="Hand2")
            btn_gestion_socios = tk.Button(self.windows_inicial, text="Gestionar Socios", cursor="Hand2")
            btn_gestion_libros = tk.Button(self.windows_inicial, text="Gestionar Libros", cursor="Hand2")
            btn_gestion_prestamos = tk.Button(self.windows_inicial, text="Gestionar Prestamos", cursor="Hand2")
            btn_gestion_reservas = tk.Button(self.windows_inicial, text="Gestionar Reservas", cursor="Hand2")
            btn_gestion_devoluciones = tk.Button(self.windows_inicial, text="Gestionar Devoluciones", cursor="Hand2")
            btn_salir_sistema = tk.Button(self.windows_inicial, text="Salir del sistema", cursor="Hand2")
        else:    
            label_name_subject.config(fg="black", bg="lightyellow")  
            btn_gestion_sedes = tk.Button(self.windows_inicial, text="Gestionar Sedes")
            btn_gestion_socios = tk.Button(self.windows_inicial, text="Gestionar Socios")
            btn_gestion_libros = tk.Button(self.windows_inicial, text="Gestionar Libros")
            btn_gestion_prestamos = tk.Button(self.windows_inicial, text="Gestionar Prestamos")
            btn_gestion_reservas = tk.Button(self.windows_inicial, text="Gestionar Reservas")
            btn_gestion_devoluciones = tk.Button(self.windows_inicial, text="Gestionar Devoluciones")
            btn_salir_sistema = tk.Button(self.windows_inicial, text="Salir del sistema")
                                        
        btn_gestion_sedes.config(fg="white", bg="gray", font=("Arial", 15, "bold"))  
        btn_gestion_sedes.config(command=self.activar_ventana_gestion_sede)
        
        btn_gestion_socios.config(fg="white", bg="blue", font=("Arial", 15, "bold"))
        btn_gestion_socios.config(command=self.activar_ventana_gestion_socios) 
        
        btn_gestion_libros.config(fg="white", bg="black", font=("Arial", 15, "bold"))
        btn_gestion_libros.config(command=self.mensaje_botones) 
        
        btn_gestion_prestamos.config(fg="white", bg="green", font=("Arial", 15, "bold"))
        btn_gestion_prestamos.config(command=self.mensaje_botones) 
        
        btn_gestion_reservas.config(fg="white", bg="pink", font=("Arial", 15, "bold"))
        btn_gestion_reservas.config(command=self.mensaje_botones) 
        
        btn_gestion_devoluciones.config(fg="white", bg="orange", font=("Arial", 15, "bold"))
        btn_gestion_devoluciones.config(command=self.mensaje_botones)   
        
        btn_salir_sistema.config(fg="white", bg="red", font=("Arial", 15, "bold"))
        btn_salir_sistema.config(command=self.salir_sistema)
                    
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        image_path = os.path.join(project_root, "Recursos", "biblioteca_utn_frc.png")

        image_open = Image.open(image_path)
        image_open = ImageTk.PhotoImage(image_open)
                    
        image_label = tk.Label(frame_2, image=image_open)
        image_label.image = image_open 
        
        frame_2.pack()
        label_name_subject.pack()
        image_label.pack() 
        btn_salir_sistema.pack()
        btn_gestion_sedes.pack(side="left")
        btn_gestion_socios.pack(side="right")
        btn_gestion_libros.pack(side="left")
        btn_gestion_prestamos.pack(side="right")
        btn_gestion_reservas.pack(side="left")
        btn_gestion_devoluciones.pack(side="right")
        
    
    def mensaje_botones(self):
        messagebox.showinfo("Información", "Todavia no funciona, en proceso :)")
        
    def activar_ventana_gestion_sede(self):
        PantallaGestionSede()
    
    def activar_ventana_gestion_socios(self):
        PantallaGestionSocio()
        
    def salir_sistema(self):
        self.windows_inicial.destroy()