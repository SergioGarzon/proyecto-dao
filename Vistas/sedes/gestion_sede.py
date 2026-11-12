import tkinter as tk
from tkinter import ttk
import platform
import os
from tkinter import messagebox
from Controlador.controlador_sede import ControladorSede
from Vistas.sedes.formulario_sede import FormularioSede

class PantallaGestionSede:
    
    def __init__(self):
        self.windows_gestion_sede = tk.Toplevel() 
        self.controlador_sedes = ControladorSede()
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
            btn_eliminar_sede = tk.Button(frame_3, text="Dar de baja sede", cursor="Hand2")
            btn_modificar_sede = tk.Button(frame_3, text="Modificar sede", cursor="Hand2")
            btn_reactivar_sede = tk.Button(frame_3, text="Reactivar sede", cursor="Hand2")
            btn_cerrar = tk.Button(frame_3, text="Cerrar ventana", cursor="Hand2")                                      
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")       
            label_nombre_sede_buscar.config(fg="black", bg="lightyellow")  
            btn_actualizar_sede = tk.Button(frame_3, text="Actualizar tabla de sedes")
            btn_buscar_sede = tk.Button(frame_3, text="Buscar sede")
            btn_insertar_datos_sedes = tk.Button(frame_3, text="Crear sedes") 
            btn_eliminar_sede = tk.Button(frame_3, text="Dar de baja sede")
            btn_modificar_sede = tk.Button(frame_3, text="Modificar sede")
            btn_reactivar_sede = tk.Button(frame_3, text="Reactivar sede")
            btn_cerrar = tk.Button(frame_3, text="Cerrar ventana")  
        
        btn_buscar_sede.config(fg="white", bg="blue", font=("Arial", 15, "bold"))  
        btn_buscar_sede.config(command=self.buscar_sede) 
        
        btn_actualizar_sede.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        btn_actualizar_sede.config(command=self.actualizar_tabla)
        
        btn_insertar_datos_sedes.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        btn_insertar_datos_sedes.config(command=self.crear_sede) 
        
        btn_eliminar_sede.config(fg="white", bg="orange", font=("Arial", 15, "bold"))  
        btn_eliminar_sede.config(command=self.dar_baja_sede)  
        
        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))  
        btn_cerrar.config(command=self.cerrar_ventana)  
        
        btn_modificar_sede.config(fg="white", bg="blue", font=("Arial", 15, "bold"), command=self.modificar_sede)
        btn_reactivar_sede.config(fg="white", bg="green", font=("Arial", 15, "bold"), command=self.reactivar_sede)

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

        # Mostrar los componentes que ya fueron creados.
        frame_3.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack()
        label_nombre_sede_buscar.pack(pady=5)
        self.textbox_nombre_sede.pack(pady=5)
        btn_buscar_sede.pack(pady=5)
        btn_actualizar_sede.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=15)

        btn_eliminar_sede.pack(pady=10, padx=4, side="right")
        btn_insertar_datos_sedes.pack(pady=10, padx=4, side="right")
        btn_modificar_sede.pack(pady=10, padx=4, side="right")
        btn_reactivar_sede.pack(pady=10, padx=4, side="right")
        btn_cerrar.pack(pady=10, side="left")

        # Mostrar los registros existentes al abrir la ventana.
        self.actualizar_tabla()

                
        


    # --- FUNCIONES AGREGADAS: Gestión de Sedes ---

    def mostrar_sedes(self, sedes):
        """Carga en la tabla las filas que devuelve el controlador."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for sede in sedes:
            self.tabla.insert("", tk.END, values=sede)

    def actualizar_tabla(self):
        try:
            sedes = self.controlador_sedes.consultar_sedes()
            self.mostrar_sedes(sedes)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron consultar las sedes: {error}",
                                 parent=self.windows_gestion_sede)

    def buscar_sede(self):
        nombre = self.textbox_nombre_sede.get().strip()
        try:
            sedes = self.controlador_sedes.buscar_sede(nombre)
            self.mostrar_sedes(sedes)
            if not sedes:
                messagebox.showinfo("Sin resultados", "No se encontraron sedes.",
                                    parent=self.windows_gestion_sede)
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self.windows_gestion_sede)

    def crear_sede(self):
        FormularioSede(self.windows_gestion_sede, self.actualizar_tabla)

    def sede_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar sede", "Primero seleccioná una sede de la tabla.",
                                   parent=self.windows_gestion_sede)
            return None
        return int(self.tabla.item(seleccion[0], "values")[0])

    def modificar_sede(self):
        id_sede = self.sede_seleccionada()
        if id_sede is None:
            return
        try:
            datos = self.controlador_sedes.obtener_sede(id_sede)
            FormularioSede(self.windows_gestion_sede, self.actualizar_tabla, datos=datos)
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self.windows_gestion_sede)

    def dar_baja_sede(self):
        id_sede = self.sede_seleccionada()
        if id_sede is None:
            return
        confirmar = messagebox.askyesno("Confirmar baja",
                                       "¿Dar de baja esta sede? Se conservará su historial.",
                                       parent=self.windows_gestion_sede)
        if not confirmar:
            return
        try:
            self.controlador_sedes.dar_baja_sede(id_sede)
            self.actualizar_tabla()
            messagebox.showinfo("Sede dada de baja", "La sede fue dada de baja correctamente.",
                                parent=self.windows_gestion_sede)
        except Exception as error:
            messagebox.showerror("No se pudo dar de baja", str(error),
                                 parent=self.windows_gestion_sede)

    def reactivar_sede(self):
        id_sede = self.sede_seleccionada()
        if id_sede is None:
            return
        try:
            self.controlador_sedes.reactivar_sede(id_sede)
            self.actualizar_tabla()
            messagebox.showinfo("Sede reactivada", "La sede volvió a estar activa.",
                                parent=self.windows_gestion_sede)
        except Exception as error:
            messagebox.showerror("No se pudo reactivar", str(error),
                                 parent=self.windows_gestion_sede)

    def cerrar_ventana(self):
        self.windows_gestion_sede.destroy()