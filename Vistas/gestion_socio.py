import tkinter as tk
import platform
import os
from tkinter import messagebox

# Instalar PILLOW 'pip install pillow'
from PIL import ImageTk, Image

class PantallaGestionSocio:
    
    def __init__(self):
        self.windows_gestion_socio = tk.Toplevel() 
        self.windows_properties()
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
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))                                        
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")          
        
        frame_4.pack()
        label_name_form.pack()
            