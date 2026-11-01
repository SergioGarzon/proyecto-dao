from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
from Controlador.controlador_prestamo import ControladorPrestamo
from Vistas.insercion_prestamos import InsercionPrestamos

class PantallaGestionPrestamo:

    def __init__(self):
        self.windows_gestion_prestamo = tk.Toplevel()
        self.windows_properties()

        self.controlador_prestamos = ControladorPrestamo()

        self.windows_components()

    def windows_properties(self):
        self.windows_gestion_prestamo.title("Proyecto DAO")
        self.windows_gestion_prestamo.geometry("1000x650")
        self.windows_gestion_prestamo.configure(bg="lightyellow")
        self.windows_gestion_prestamo.resizable(False, False)

    def windows_components(self):
        frame_6 = tk.Frame(self.windows_gestion_prestamo)
        frame_6.configure(bg="lightyellow")

        label_name_form = tk.Label(frame_6, text="Gestión de Préstamos")

        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))
            btn_actualizar = tk.Button(frame_6, text="Actualizar tabla de préstamos", cursor="Hand2")
            btn_nuevo_prestamo = tk.Button(frame_6, text="Nuevo préstamo", cursor="Hand2")
            btn_cerrar = tk.Button(frame_6, text="Cerrar ventana", cursor="Hand2")
        else:
            label_name_form.config(fg="blue", bg="lightyellow")
            btn_actualizar = tk.Button(frame_6, text="Actualizar tabla de préstamos")
            btn_nuevo_prestamo = tk.Button(frame_6, text="Nuevo préstamo")
            btn_cerrar = tk.Button(frame_6, text="Cerrar ventana")

        columnas = ("Id", "Socio", "Sede_Origen", "Sede_Destino", "Tipo", "Fecha_Prestamo", "Fecha_Devolucion", "Estado", "Ejemplares")

        self.tabla = ttk.Treeview(frame_6, columns=columnas, show="headings")

        self.tabla.heading("Id", text="N° Préstamo")
        self.tabla.heading("Socio", text="Legajo Socio")
        self.tabla.heading("Sede_Origen", text="Sede Origen")
        self.tabla.heading("Sede_Destino", text="Sede Destino")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Fecha_Prestamo", text="Fecha Préstamo")
        self.tabla.heading("Fecha_Devolucion", text="Fecha Devolución")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Ejemplares", text="Ejemplares")

        self.tabla.column("Id", width=80, anchor="center")
        self.tabla.column("Socio", width=90, anchor="center")
        self.tabla.column("Sede_Origen", width=90, anchor="center")
        self.tabla.column("Sede_Destino", width=90, anchor="center")
        self.tabla.column("Tipo", width=130, anchor="center")
        self.tabla.column("Fecha_Prestamo", width=110, anchor="center")
        self.tabla.column("Fecha_Devolucion", width=110, anchor="center")
        self.tabla.column("Estado", width=90, anchor="center")
        self.tabla.column("Ejemplares", width=150, anchor="center")

        # Traemos los datos de la base de datos
        self.actualizar_tabla()

        btn_actualizar.config(fg="white", bg="green", font=("Arial", 15, "bold"))
        btn_actualizar.config(command=self.actualizar_tabla)

        btn_nuevo_prestamo.config(fg="white", bg="blue", font=("Arial", 15, "bold"))
        btn_nuevo_prestamo.config(command=self.nuevo_prestamo)

        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))
        btn_cerrar.config(command=self.cerrar_ventana)

        frame_6.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack(pady=5)
        btn_actualizar.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=15)
        btn_nuevo_prestamo.pack(pady=10)
        btn_cerrar.pack()

    def actualizar_tabla(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        lista_resultados = self.controlador_prestamos.consultar_prestamos()

        for fila in lista_resultados:
            # Mostramos un guion en vez de "None" cuando todavía no hay fecha de devolución
            fila = ["-" if valor is None else valor for valor in fila]
            self.tabla.insert("", tk.END, values=fila)

    def nuevo_prestamo(self):
        # Le pasamos la función para que la tabla se refresque sola al registrar un préstamo
        InsercionPrestamos(self.actualizar_tabla)

    def cerrar_ventana(self):
        self.windows_gestion_prestamo.destroy()
