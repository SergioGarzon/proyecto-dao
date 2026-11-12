from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import platform
from Controlador.controlador_socio import ControladorSocio
from Entidades.excepciones import ReglaNegocioError
from Vistas.multas.gestion_multa import PantallaGestionMulta
from Vistas.socios.insercion_socios import InsercionSocios

class PantallaGestionSocio:
    
    def __init__(self):
        self.windows_gestion_socio = tk.Toplevel() 
        self.windows_properties()
        
        self.controlador_socios = ControladorSocio()
        
        self.windows_components()    
    
    def windows_properties(self):
        self.windows_gestion_socio.title("Proyecto DAO")
        self.windows_gestion_socio.geometry("1150x650")
        self.windows_gestion_socio.configure(bg="lightyellow")
        self.windows_gestion_socio.resizable(False, False)
        
    def windows_components(self):
        frame_4 = tk.Frame(self.windows_gestion_socio)   
        frame_4.configure(bg="lightyellow") 
        
        label_name_form = tk.Label(frame_4, text="Gestión de Socios")
        label_socio_legajo_buscar = tk.Label(frame_4, text="Ingrese el legajo del Socio:")
        self.textbox_legajo_socio = tk.Entry(frame_4, font=("Arial", 14), width=30)
        
        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))     
            label_socio_legajo_buscar.config(fg="black", bg="lightyellow", font=("Arial", 15))  
            btn_buscar_socio = tk.Button(frame_4, text="Buscar socio", cursor="Hand2")                                      
            btn_actualizar = tk.Button(frame_4, text="Actualizar tabla de socios", cursor="Hand2")
            btn_insertar_datos_socios = tk.Button(frame_4, text="Crear socios", cursor="Hand2") 
            btn_eliminar_socio = tk.Button(frame_4, text="Dar de baja", cursor="Hand2")
            btn_cerrar = tk.Button(frame_4, text="Cerrar ventana", cursor="Hand2") 
        else:    
            label_name_form.config(fg="blue", bg="lightyellow")
            label_socio_legajo_buscar.config(fg="black", bg="lightyellow") 
            btn_buscar_socio = tk.Button(frame_4, text="Buscar socio") 
            btn_actualizar = tk.Button(frame_4, text="Actualizar tabla de socios")  
            btn_insertar_datos_socios = tk.Button(frame_4, text="Crear socios") 
            btn_eliminar_socio = tk.Button(frame_4, text="Dar de baja")
            btn_cerrar = tk.Button(frame_4, text="Cerrar ventana")          
        
        btn_buscar_socio.config(fg="white", bg="blue", font=("Arial", 15, "bold"))  
        btn_buscar_socio.config(command=self.mostrar_datos_tabla_filtrada_nro_socio)  
        
        btn_eliminar_socio.config(fg="white", bg="orange", font=("Arial", 15, "bold"))  
        btn_eliminar_socio.config(command=self.eliminar_socio)  
        
        columnas = ("Legajo", "Nombre", "Apellido", "Fecha_Inscripcion", "Domicilio", "Barrio", "Localidad", "Estado")
        
        self.tabla = ttk.Treeview(frame_4, columns=columnas, show="headings")
        
        self.tabla.heading("Legajo", text="Legajo Socio")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Fecha_Inscripcion", text="Fecha de Inscripcion")
        self.tabla.heading("Domicilio", text="Domicilio")
        self.tabla.heading("Barrio", text="Barrio")
        self.tabla.heading("Localidad", text="Localidad")
        self.tabla.heading("Estado", text="Estado")
        
        self.tabla.column("Legajo", width=60, anchor="center")
        self.tabla.column("Nombre", width=120, anchor="w")
        self.tabla.column("Apellido", width=120, anchor="center")
        self.tabla.column("Fecha_Inscripcion", width=120, anchor="center")
        self.tabla.column("Domicilio", width=100, anchor="center")
        self.tabla.column("Barrio", width=100, anchor="center")
        self.tabla.column("Localidad", width=100, anchor="center")
        self.tabla.column("Estado", width=80, anchor="center")
        
        # Traemos los datos de la base de datos
        self.actualizar_tabla()
        
        btn_actualizar.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        btn_actualizar.config(command=self.actualizar_tabla)  
        
        btn_insertar_datos_socios.config(fg="white", bg="green", font=("Arial", 15, "bold"))  
        btn_insertar_datos_socios.config(command=self.insertar_informacion)          
        
        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))  
        btn_cerrar.config(command=self.cerrar_ventana)  

        # Botones que actúan sobre el socio seleccionado en la tabla
        cursor = "hand2" if str(platform.system()) == "Windows" else ""
        btn_modificar_socio = tk.Button(frame_4, text="Modificar socio", fg="white", bg="blue",
                                        font=("Arial", 15, "bold"), cursor=cursor, command=self.modificar_socio)
        # Habilitar e inhabilitar no son botones: el sistema lo hace solo según multas y préstamos vencidos
        btn_dar_alta_socio = tk.Button(frame_4, text="Dar de alta", fg="white", bg="teal",
                                       font=("Arial", 15, "bold"), cursor=cursor, command=self.dar_alta_socio)
        btn_ver_multas = tk.Button(frame_4, text="Ver multas", fg="white", bg="darkred",
                                   font=("Arial", 15, "bold"), cursor=cursor, command=self.ver_multas)
                
        frame_4.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack(pady=5)
        label_socio_legajo_buscar.pack(pady=5)
        self.textbox_legajo_socio.pack(pady=5)
        btn_buscar_socio.pack(pady=5) 
        btn_actualizar.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=15)
        btn_ver_multas.pack(pady=10, padx=4, side="right")
        btn_eliminar_socio.pack(pady=10, padx=4, side="right")
        btn_dar_alta_socio.pack(pady=10, padx=4, side="right")
        btn_modificar_socio.pack(pady=10, padx=4, side="right")
        btn_insertar_datos_socios.pack(pady=10, padx=4, side="right")
        btn_cerrar.pack(side="left")
                
    #  Metodo para consultar datos
    def consultar_datos(self):
        return self.controlador_socios.consultar_socios()
    
       
    # Metodo del boton para actualizar la lista
    def actualizar_tabla(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)
            
        lista_resultados = self.consultar_datos()
        
        for fila in lista_resultados:
            self.tabla.insert("", tk.END, values=fila)
            
        self.textbox_legajo_socio.delete(0, tk.END)
        
    # Metodo para el boton de insertar nuevo socio, nos va a derivar al nuevo formulario
    def insertar_informacion(self):
        InsercionSocios(al_guardar=self.actualizar_tabla)
        
    # Metodo para el boton que busca socio por medio de un legajo ingresado    
    def mostrar_datos_tabla_filtrada_nro_socio(self):        
        if str(self.textbox_legajo_socio.get()) == "":
            messagebox.showerror("Error", "No se ha insertado el legajo del socio a buscar!", parent=self.windows_gestion_socio)
            return
                    
        try:
            lista_resultados = self.controlador_socios.buscar_socio(self.textbox_legajo_socio.get())
        except ReglaNegocioError as error:
            messagebox.showerror("Error", str(error), parent=self.windows_gestion_socio)
            return

        if len(lista_resultados) == 0:
            messagebox.showwarning("Advertencia", "No se han encontrado socios con dicho legajo", parent=self.windows_gestion_socio)
        else:
            for elemento in self.tabla.get_children():
                        self.tabla.delete(elemento)
                        
            for fila in lista_resultados:
                self.tabla.insert("", tk.END, values=fila)     
    
    def legajo_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una fila de la tabla.",
                                   parent=self.windows_gestion_socio)
            return None
        return self.tabla.item(seleccion[0], "values")[0]

    # Metodo para ver y pagar las multas del socio seleccionado
    def ver_multas(self):
        legajo = self.legajo_seleccionado()
        if legajo is not None:
            PantallaGestionMulta(legajo=legajo)

    # Metodo para modificar los datos del socio seleccionado
    def modificar_socio(self):
        legajo = self.legajo_seleccionado()
        if legajo is None:
            return
        try:
            datos = self.controlador_socios.obtener_socio(legajo)
        except ReglaNegocioError as error:
            messagebox.showerror("Error", str(error), parent=self.windows_gestion_socio)
            return
        InsercionSocios(al_guardar=self.actualizar_tabla, datos=datos)

    # Metodos para dar de alta y de baja: comparten la confirmación y el manejo de errores
    def dar_alta_socio(self):
        self.cambiar_estado(self.controlador_socios.dar_alta_socio, "dar de alta", "dado de alta")

    def eliminar_socio(self):
        self.cambiar_estado(self.controlador_socios.eliminar_socio, "dar de baja", "dado de baja")

    def cambiar_estado(self, operacion, accion, resultado):
        legajo = self.legajo_seleccionado()
        if legajo is None:
            return
        if not messagebox.askyesno("Confirme", f"¿Estás seguro que deseas {accion} al socio con legajo {legajo}?",
                                   parent=self.windows_gestion_socio):
            return
        try:
            operacion(legajo)
        except ReglaNegocioError as error:
            messagebox.showerror("Error", str(error), parent=self.windows_gestion_socio)
            return
        messagebox.showinfo("Éxito", f"Socio {resultado} correctamente.", parent=self.windows_gestion_socio)
        self.actualizar_tabla()

    # Metodo para el boton que cierra la ventana
    def cerrar_ventana(self):
        self.windows_gestion_socio.destroy()
        
       
