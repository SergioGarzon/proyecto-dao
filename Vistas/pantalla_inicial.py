import tkinter as tk
import platform

class PantallaInicial:
    
    def __init__(self):
        self.windows_inicial = tk.Tk()
        self.windows_properties()
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_inicial.title("Proyecto DAO")
        self.windows_inicial.geometry("850x650")
        self.windows_inicial.configure(bg="lightyellow")
        self.windows_inicial.resizable(False, False)
        
    def windows_components(self):
        frame_2 = tk.Frame(self.windows_inicial)   
        frame_2.configure(bg="lightyellow") 
            
        label_name_subject = tk.Label(frame_2, text="Biblioteca de Prestamos a Socios")                     
            
        if str(platform.system()) == "Windows":
            label_name_subject.config(fg="black", bg="lightyellow", font=("Arial", 25))                    
        else:    
            label_name_subject.config(fg="black", bg="lightyellow")                             
                  
        frame_2.pack()
        label_name_subject.pack()