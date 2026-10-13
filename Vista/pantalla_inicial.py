import tkinter as tk
import platform

class PantallaInicioPrograma():

    def __init__(self):
        self.windows_main = tk.Tk()
        self.windows_properties()
        self.windows_components()    

    def windows_properties(self):
        self.windows_main.title("Proyecto DAO")
        self.windows_main.geometry("500x500+250+100")
        self.windows_main.configure(bg="white")
        self.windows_main.resizable(False, False)
    
    def windows_components(self):
        frame1 = tk.Frame(self.windows_main)   
        frame1.configure(bg="lightblue") 
        
        label_name = tk.Label(frame1, text="Desarrollo de Aplicaciones con Objetos")    
        
        if str(platform.system()) == "Windows":
            label_name.config(fg="black", bg="white", font=("Arial", 20))    
        else:    
             label_name.config(fg="black", bg="white")  
        
        frame1.pack()
        label_name.pack()


if __name__ == "__main__":
    app_inicial = PantallaInicioPrograma()
    app_inicial.windows_main.mainloop()