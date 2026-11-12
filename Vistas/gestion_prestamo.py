from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import platform
from Controlador.controlador_prestamo import ControladorPrestamo
from Entidades.excepciones import ReglaNegocioError
from Vistas.devolucion_prestamos import DevolucionPrestamos
from Vistas.insercion_prestamos import InsercionPrestamos

class PantallaGestionPrestamo:

    def __init__(self):
        self.windows_gestion_prestamo = tk.Toplevel()
        self.windows_properties()

        self.controlador_prestamos = ControladorPrestamo()

        self.windows_components()
        # Al abrir, se inhabilita a los socios cuyos préstamos ya vencieron
        self.procesar_vencimientos()

    def windows_properties(self):
        self.windows_gestion_prestamo.title("Proyecto DAO")
        self.windows_gestion_prestamo.geometry("1300x700")
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
            btn_devolucion = tk.Button(frame_6, text="Registrar devolución", cursor="Hand2")
            btn_cerrar = tk.Button(frame_6, text="Cerrar ventana", cursor="Hand2")
        else:
            label_name_form.config(fg="blue", bg="lightyellow")
            btn_actualizar = tk.Button(frame_6, text="Actualizar tabla de préstamos")
            btn_nuevo_prestamo = tk.Button(frame_6, text="Nuevo préstamo")
            btn_devolucion = tk.Button(frame_6, text="Registrar devolución")
            btn_cerrar = tk.Button(frame_6, text="Cerrar ventana")

        columnas = ("Id", "Socio", "Sede_Origen", "Sede_Destino", "Tipo", "Fecha_Prestamo", "Fecha_Devolucion", "Estado", "Ejemplares")

        self.tabla = ttk.Treeview(frame_6, columns=columnas, show="headings")

        self.tabla.heading("Id", text="N° Préstamo")
        self.tabla.heading("Socio", text="Socio")
        self.tabla.heading("Sede_Origen", text="Sede Origen")
        self.tabla.heading("Sede_Destino", text="Sede Destino")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Fecha_Prestamo", text="Fecha Préstamo")
        self.tabla.heading("Fecha_Devolucion", text="Vencimiento")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Ejemplares", text="Libros")

        self.tabla.column("Id", width=80, anchor="center")
        self.tabla.column("Socio", width=200, anchor="w")
        self.tabla.column("Sede_Origen", width=130, anchor="center")
        self.tabla.column("Sede_Destino", width=130, anchor="center")
        self.tabla.column("Tipo", width=130, anchor="center")
        self.tabla.column("Fecha_Prestamo", width=110, anchor="center")
        self.tabla.column("Fecha_Devolucion", width=110, anchor="center")
        self.tabla.column("Estado", width=90, anchor="center")
        self.tabla.column("Ejemplares", width=260, anchor="w")

        # Traemos los datos de la base de datos
        self.actualizar_tabla()

        btn_actualizar.config(fg="white", bg="green", font=("Arial", 15, "bold"))
        btn_actualizar.config(command=self.actualizar_tabla)

        btn_nuevo_prestamo.config(fg="white", bg="blue", font=("Arial", 15, "bold"))
        btn_nuevo_prestamo.config(command=self.nuevo_prestamo)

        btn_devolucion.config(fg="white", bg="orange", font=("Arial", 15, "bold"))
        btn_devolucion.config(command=self.registrar_devolucion)

        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))
        btn_cerrar.config(command=self.cerrar_ventana)

        # Búsqueda: se elige un campo y se escribe el texto a buscar
        frame_busqueda = tk.Frame(frame_6, bg="lightyellow")
        tk.Label(frame_busqueda, text="Buscar por:", bg="lightyellow", font=("Arial", 13)).pack(side="left", padx=5)
        self.combo_campo = ttk.Combobox(frame_busqueda, state="readonly", width=22, font=("Arial", 12),
                                        values=list(ControladorPrestamo.CAMPOS_BUSQUEDA))
        self.combo_campo.current(0)
        self.combo_campo.pack(side="left", padx=5)
        self.textbox_buscar = tk.Entry(frame_busqueda, font=("Arial", 13), width=30)
        self.textbox_buscar.bind("<Return>", lambda evento: self.buscar_prestamos())
        self.textbox_buscar.pack(side="left", padx=5)
        tk.Button(frame_busqueda, text="Buscar", fg="white", bg="blue", font=("Arial", 12, "bold"),
                  command=self.buscar_prestamos).pack(side="left", padx=5)
        tk.Button(frame_busqueda, text="Limpiar", fg="white", bg="gray", font=("Arial", 12, "bold"),
                  command=self.limpiar_busqueda).pack(side="left", padx=5)

        frame_6.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack(pady=5)
        btn_actualizar.pack(pady=5)
        frame_busqueda.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=15)
        btn_nuevo_prestamo.pack(pady=5)
        btn_devolucion.pack(pady=5)
        btn_cerrar.pack()

    def procesar_vencimientos(self):
        inhabilitados = self.controlador_prestamos.procesar_vencimientos()
        if inhabilitados:
            messagebox.showinfo("Préstamos vencidos",
                                f"Se inhabilitaron {inhabilitados} socio(s) por tener préstamos vencidos.",
                                parent=self.windows_gestion_prestamo)

    def actualizar_tabla(self):
        self.mostrar_prestamos(self.controlador_prestamos.consultar_prestamos())

    def buscar_prestamos(self):
        try:
            resultados = self.controlador_prestamos.buscar_prestamos(self.combo_campo.get(), self.textbox_buscar.get())
        except ReglaNegocioError as error:
            messagebox.showerror("Búsqueda inválida", str(error), parent=self.windows_gestion_prestamo)
            return

        self.mostrar_prestamos(resultados)
        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron préstamos.", parent=self.windows_gestion_prestamo)

    def limpiar_busqueda(self):
        self.textbox_buscar.delete(0, tk.END)
        self.actualizar_tabla()

    def mostrar_prestamos(self, lista_resultados):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        for fila in lista_resultados:
            # Mostramos un guion en vez de "None" cuando todavía no hay fecha de devolución
            fila = ["-" if valor is None else valor for valor in fila]
            self.tabla.insert("", tk.END, values=fila)

    def nuevo_prestamo(self):
        # Le pasamos la función para que la tabla se refresque sola al registrar un préstamo
        InsercionPrestamos(self.actualizar_tabla)

    def registrar_devolucion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione un préstamo de la tabla.", parent=self.windows_gestion_prestamo)
            return

        id_prestamo = int(self.tabla.item(seleccion[0], "values")[0])
        try:
            DevolucionPrestamos(id_prestamo, self.actualizar_tabla)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede registrar la devolución", str(error), parent=self.windows_gestion_prestamo)

    def cerrar_ventana(self):
        self.windows_gestion_prestamo.destroy()
