import tkinter as tk
import platform

# Instalar PILLOW 'pip install pillow'
from PIL import ImageTk, Image

class PantallaInicioPrograma():

    def __init__(self):
        self.windows_main = tk.Tk()
        self.windows_properties()
        self.windows_components()    

    def windows_properties(self):
        self.windows_main.title("Proyecto DAO")
        self.windows_main.geometry("700x450+250+100")
        self.windows_main.configure(bg="white")
        self.windows_main.resizable(False, False)
    
    def windows_components(self):
        frame1 = tk.Frame(self.windows_main)   
        frame1.configure(bg="white") 
        
        label_name_subject = tk.Label(frame1, text="Desarrollo de Aplicaciones con Objetos")  
                     
        name_personas = tk.Label(frame1, text="\nIntegrantes")
        name_person_1 = tk.Label(frame1, text="\n\n* Dario Lopez")    
        name_person_2 = tk.Label(frame1, text="* Federico Wedemeyer")  
        name_person_3 = tk.Label(frame1, text="* Rosario Evelyn Mendoza")  
        name_person_4 = tk.Label(frame1, text="* Sergio Gabriel Garzon") 
        name_person_5 = tk.Label(frame1, text="* Tomas Reyna Mariano")  
        name_person_6 = tk.Label(frame1, text="\n\n")          
        
        if str(platform.system()) == "Windows":
            label_name_subject.config(fg="black", bg="white", font=("Arial", 25))
            name_personas.config(fg="black", bg="white", font=("Arial", 20))
            name_person_1.config(fg="black", bg="white", font=("Arial", 15))
            name_person_2.config(fg="black", bg="white", font=("Arial", 15))  
            name_person_3.config(fg="black", bg="white", font=("Arial", 15))  
            name_person_4.config(fg="black", bg="white", font=("Arial", 15))  
            name_person_5.config(fg="black", bg="white", font=("Arial", 15))
            name_person_6.config(fg="black", bg="white", font=("Arial", 15)) 
            btn_quit = tk.Button(self.windows_main, text="Continuar", cursor="Hand2")             
        else:    
            label_name_subject.config(fg="black", bg="white")
            name_personas.config(fg="black", bg="white")
            name_person_1.config(fg="black", bg="white")
            name_person_2.config(fg="black", bg="white")  
            name_person_3.config(fg="black", bg="white")  
            name_person_4.config(fg="black", bg="white")  
            name_person_5.config(fg="black", bg="white")
            name_person_6.config(fg="black", bg="white")
            btn_quit = tk.Button(self.windows_main, text="Continuar")
                            
        btn_quit.config(fg="white", bg="blue", font=("Arial", 15, "bold"))  
        #btn_quit.config(command=self.quitar_ventana)  
                       
        image_open = Image.open("./logo_utn.png")
        image_open = ImageTk.PhotoImage(image_open)
        
        image_label = tk.Label(frame1, image=image_open)
        image_label.image = image_open 
        
        frame1.pack()
        label_name_subject.pack()
        name_personas.pack()
        name_person_1.pack()
        name_person_2.pack()
        name_person_3.pack()
        name_person_4.pack()
        name_person_5.pack()
        name_person_6.pack()
        btn_quit.pack()


if __name__ == "__main__":
    app_inicial = PantallaInicioPrograma()
    app_inicial.windows_main.mainloop()