
import tkinter as tk
from tkinter import ttk, messagebox

from Controlador.controlador_libro import ControladorLibro
from Vistas.libros.formulario_libro import FormularioLibro
from Vistas.libros.gestion_ejemplar import PantallaGestionEjemplar
class PantallaGestionLibro:

    def __init__(self):
        self.windows_gestion_libro = tk.Toplevel()
        self.controlador_libros = ControladorLibro()

        self.windows_properties()
        self.windows_components()

    def windows_properties(self):
        self.windows_gestion_libro.title("Proyecto DAO - Gestión de Libros")
        self.windows_gestion_libro.geometry("1000x580")
        self.windows_gestion_libro.configure(bg="lightyellow")

    def windows_components(self):
        frame = tk.Frame(self.windows_gestion_libro, bg="lightyellow")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Titulo
        tk.Label(
            frame,
            text="Gestión de Libros",
            fg="blue",
            bg="lightyellow",
            font=("Arial", 25)
        ).pack(pady=10)

        # Buscador
        tk.Label(
            frame,
            text="Buscar por título, autor o ISBN:",
            bg="lightyellow",
            font=("Arial", 15)
        ).pack(pady=5)

        self.textbox_buscar = tk.Entry(
            frame, font=("Arial", 14), width=35
        )
        self.textbox_buscar.pack(pady=5)

        self.textbox_buscar.bind(
            "<Return>", lambda evento: self.buscar_libro()
        )

        tk.Button(
            frame,
            text="Buscar libro",
            fg="white",
            bg="blue",
            font=("Arial", 15, "bold"),
            command=self.buscar_libro
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Actualizar tabla de libros",
            fg="white",
            bg="green",
            font=("Arial", 15, "bold"),
            command=self.actualizar_tabla
        ).pack(pady=5)

        # Tabla de libros
        columnas = (
            "Codigo", "ISBN", "Titulo",
            "Autor", "Editorial", "Anio"
        )

        frame_tabla = tk.Frame(frame)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=15)

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings"
        )

        titulos = (
            "Código", "ISBN", "Título",
            "Autor", "Editorial", "Año"
        )

        anchos = (70, 150, 220, 180, 170, 80)

        for columna, titulo, ancho in zip(columnas, titulos, anchos):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(
                columna,
                width=ancho,
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill=tk.BOTH, expand=True)
        scroll.pack(side="right", fill="y")

        # Botones para crear y modificar libros
        frame_botones = tk.Frame(frame, bg="lightyellow")
        frame_botones.pack(pady=10)

        btn_crear_libro = tk.Button(
            frame_botones,
            text="Crear libro",
            fg="white",
            bg="green",
            font=("Arial", 15, "bold"),
            command=self.crear_libro
        )
        btn_crear_libro.pack(side="left", padx=10)

        btn_modificar_libro = tk.Button(
            frame_botones,
            text="Modificar libro",
            fg="white",
            bg="blue",
            font=("Arial", 15, "bold"),
            command=self.modificar_libro
        )
        btn_modificar_libro.pack(side="left", padx=10)
        btn_gestion_ejemplares = tk.Button(
            frame_botones,
            text="Gestionar ejemplares",
            fg="white",
            bg="orange",
            font=("Arial", 15, "bold"),
            command=self.gestionar_ejemplares
        )
        btn_gestion_ejemplares.pack(side="left", padx=10)

        btn_disponibilidad = tk.Button(
            frame_botones,
            text="Revisar disponibilidad",
            fg="white",
            bg="purple",
            font=("Arial", 15, "bold"),
            command=self.revisar_disponibilidad
        )
        btn_disponibilidad.pack(side="left", padx=10)

        # Cerrar ventana
        tk.Button(
            frame,
            text="Cerrar ventana",
            fg="white",
            bg="red",
            font=("Arial", 15, "bold"),
            command=self.cerrar_ventana
        ).pack(pady=10)

        # Cargar los libros al abrir la ventana
        self.actualizar_tabla()

    # Mostrar datos en la tabla
    def mostrar_libros(self, libros):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for libro in libros:
            self.tabla.insert("", tk.END, values=libro)

    # Consultar todos los libros
    def actualizar_tabla(self):
        try:
            libros = self.controlador_libros.consultar_libros()
            self.mostrar_libros(libros)
        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.windows_gestion_libro
            )

    # Buscar libros
    def buscar_libro(self):
        texto = self.textbox_buscar.get().strip()

        try:
            libros = self.controlador_libros.buscar_libros(texto)
            self.mostrar_libros(libros)

            if not libros:
                messagebox.showinfo(
                    "Sin resultados",
                    "No se encontraron libros.",
                    parent=self.windows_gestion_libro
                )
        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.windows_gestion_libro
            )

    
    def crear_libro(self):
        # Abrir el formulario vacío para registrar un libro
        FormularioLibro(
            self.windows_gestion_libro,
            self.actualizar_tabla
        )

    def modificar_libro(self):
        # Obtener el libro seleccionado en la tabla
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccionar libro",
                "Primero seleccioná un libro de la tabla.",
                parent=self.windows_gestion_libro
            )
            return

        # Obtener el código del libro seleccionado
        codigo = self.tabla.item(seleccion[0], "values")[0]

        try:
            # Buscar los datos del libro en la base
            datos = self.controlador_libros.obtener_libro(codigo)

            # Abrir el formulario con los datos existentes
            FormularioLibro(
                self.windows_gestion_libro,
                self.actualizar_tabla,
                datos=datos
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.windows_gestion_libro
            )


    def revisar_disponibilidad(self):
        # Obtener el libro seleccionado en la tabla
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccionar libro",
                "Primero seleccioná un libro de la tabla.",
                parent=self.windows_gestion_libro
            )
            return

        valores = self.tabla.item(seleccion[0], "values")
        codigo, titulo = valores[0], valores[2]

        try:
            filas = self.controlador_libros.consultar_disponibilidad(codigo)
        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.windows_gestion_libro
            )
            return

        if not filas:
            messagebox.showinfo(
                "Disponibilidad",
                f"\"{titulo}\" no tiene ejemplares en sedes activas.",
                parent=self.windows_gestion_libro
            )
            return

        # Ventana con una fila por sede
        ventana = tk.Toplevel(self.windows_gestion_libro)
        ventana.title("Disponibilidad por sede")
        ventana.configure(bg="lightyellow")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text=titulo,
            fg="blue",
            bg="lightyellow",
            font=("Arial", 16, "bold")
        ).pack(padx=15, pady=10)

        columnas = ("Sede", "Disponibles", "Total")
        tabla = ttk.Treeview(
            ventana,
            columns=columnas,
            show="headings",
            height=min(len(filas), 10)
        )

        for columna, ancho in zip(columnas, (200, 100, 80)):
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=ancho, anchor="center")

        for fila in filas:
            tabla.insert("", tk.END, values=fila)

        tabla.pack(padx=15)

        disponibles = sum(fila[1] for fila in filas)
        total = sum(fila[2] for fila in filas)

        tk.Label(
            ventana,
            text=f"{disponibles} disponibles de {total} ejemplares",
            bg="lightyellow",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Cerrar",
            fg="white",
            bg="red",
            font=("Arial", 12, "bold"),
            command=ventana.destroy
        ).pack(pady=(0, 10))

    # Cerrar
    def cerrar_ventana(self):
        self.windows_gestion_libro.destroy()

    def gestionar_ejemplares(self):
        seleccion = self.tabla.selection()
        codigo_libro = None

        if seleccion:
            codigo_libro = self.tabla.item(
                seleccion[0], "values"
            )[0]

        PantallaGestionEjemplar(
            self.windows_gestion_libro,
            codigo_libro=codigo_libro
        )