from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
import os
from datetime import date, timedelta
from tkinter import messagebox
from PIL import ImageTk, Image

from Controlador.controlador_reporte import ControladorReporte, DIAS_PERIODO_POR_DEFECTO
from Entidades.excepciones import ReglaNegocioError
from Vistas.reportes.ventana_reporte import VentanaReporte

class PantallaReportesGenerales:
    
    def __init__(self):
        self.windows_reportes = tk.Toplevel()
        self.controlador_reportes = ControladorReporte()
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
        label_reportes_data = tk.Label(frame_5, text="Elegí un reporte y el período (fechas AAAA-MM-DD).\nSi dejás las fechas vacías, se usan los últimos 6 meses.")
        
        opciones_reporte = list(ControladorReporte.REPORTES)
                
        frame_derecho = tk.Frame(frame_5, bg="lightyellow")
        
        self.cmb_reporte = ttk.Combobox(frame_derecho, values=opciones_reporte, state="readonly", width=40)
        self.cmb_reporte.current(0)
        self.cmb_reporte.bind("<<ComboboxSelected>>", self.al_cambiar_reporte)

        # Período y Top N (este último solo para el reporte de libros)
        frame_filtros = tk.Frame(frame_derecho, bg="lightyellow")
        hoy = date.today()
        self.entry_desde = self.crear_campo(frame_filtros, "Desde:", 0, (hoy - timedelta(days=DIAS_PERIODO_POR_DEFECTO)).isoformat())
        self.entry_hasta = self.crear_campo(frame_filtros, "Hasta:", 1, hoy.isoformat())
        self.entry_limite = self.crear_campo(frame_filtros, "Top N:", 2, "10")
        self.al_cambiar_reporte()
        
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
        btn_generar_reporte.config(command=self.generar_reporte)
           
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
        
        self.cmb_reporte.pack(pady=15)
        frame_filtros.pack(pady=5)
        btn_generar_reporte.pack(pady=15)
        btn_salir.pack(pady=20)
        
    def crear_campo(self, frame, texto, fila, valor):
        tk.Label(frame, text=texto, bg="lightyellow", font=("Arial", 12)).grid(row=fila, column=0, sticky="e", pady=3)
        entry = tk.Entry(frame, font=("Arial", 12), width=14)
        entry.insert(0, valor)
        entry.grid(row=fila, column=1, padx=5, pady=3)
        return entry

    def al_cambiar_reporte(self, event=None):
        # El Top N solo tiene sentido para el ranking de libros
        es_ranking = self.cmb_reporte.get() == "Libros más pedidos entre sedes"
        self.entry_limite.config(state="normal" if es_ranking else "disabled")

    def generar_reporte(self):
        try:
            reporte = self.controlador_reportes.generar(self.cmb_reporte.get(), self.entry_desde.get().strip(),
                                                        self.entry_hasta.get().strip(),
                                                        limite=self.entry_limite.get().strip() or 10)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede generar el reporte", str(error), parent=self.windows_reportes)
            return
        VentanaReporte(reporte)

    # Metodo para el boton que cierra la ventana
    def cerrar_ventana(self):
        self.windows_reportes.destroy()
        
       