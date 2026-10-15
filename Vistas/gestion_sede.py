import tkinter as tk
import platform
import os
from tkinter import messagebox

# Instalar PILLOW 'pip install pillow'
from PIL import ImageTk, Image

class PantallaGestionSede:
    
    def __init__(self):
        self.windows_gestion_sede = tk.Toplevel() 
        self.windows_properties()
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_gestion_sede.title("Proyecto DAO")
        self.windows_gestion_sede.geometry("800x650")
        self.windows_gestion_sede.configure(bg="lightyellow")
        self.windows_gestion_sede.resizable(False, False)
        
    def windows_components(self):
        frame_3 = tk.Frame(self.windows_gestion_sede)   
        frame_3.configure(bg="lightyellow") 
        
        label_name_form = tk.Label(frame_3, text="Gestión de Sedes")
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))                                        
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")          
        
        frame_3.pack()
        label_name_form.pack()
            