
import tkinter as tk
from tkinter import ttk, messagebox

from Controlador.controlador_ejemplar import ControladorEjemplar


class PantallaGestionEjemplar:

    def __init__(self, ventana_padre, codigo_libro=None):
        self.ventana = tk.Toplevel(ventana_padre)
        self.controlador = ControladorEjemplar()
        self.codigo_libro_inicial = codigo_libro

        self.windows_properties()
        self.windows_components()
        self.cargar_datos()

    def windows_properties(self):
        self.ventana.title("Proyecto DAO - Gestión de Ejemplares")
        self.ventana.geometry("1000x600")
        self.ventana.configure(bg="lightyellow")

    def windows_components(self):
        frame = tk.Frame(self.ventana, bg="lightyellow")
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(
            frame,
            text="Gestión de Ejemplares",
            fg="blue",
            bg="lightyellow",
            font=("Arial", 25)
        ).pack(pady=10)

        # Seleccionar el libro
        tk.Label(
            frame,
            text="Seleccionar libro:",
            bg="lightyellow",
            font=("Arial", 13)
        ).pack(pady=5)

        self.combo_libros = ttk.Combobox(
            frame,
            state="readonly",
            width=55
        )
        self.combo_libros.pack(pady=5)
        self.combo_libros.bind(
            "<<ComboboxSelected>>",
            lambda evento: self.actualizar_tabla()
        )

        # Tabla de ejemplares
        columnas = (
            "ID", "Codigo", "Libro",
            "Sede", "Estado", "EstadoFisico"
        )

        frame_tabla = tk.Frame(frame)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=15)

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings"
        )

        titulos = (
            "ID", "Código de inventario", "Libro",
            "Sede", "Estado", "Estado físico"
        )

        anchos = (60, 160, 220, 180, 140, 130)

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

        # Registrar nuevo ejemplar
        frame_registro = tk.LabelFrame(
            frame,
            text="Registrar nuevo ejemplar",
            bg="lightyellow",
            font=("Arial", 12, "bold")
        )
        frame_registro.pack(fill="x", pady=10)

        tk.Label(
            frame_registro,
            text="Código de inventario:",
            bg="lightyellow"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.entrada_codigo = tk.Entry(
            frame_registro,
            width=25
        )
        self.entrada_codigo.grid(
            row=0, column=1, padx=10, pady=10
        )

        tk.Label(
            frame_registro,
            text="Sede:",
            bg="lightyellow"
        ).grid(row=0, column=2, padx=10, pady=10)

        self.combo_sedes = ttk.Combobox(
            frame_registro,
            state="readonly",
            width=25
        )
        self.combo_sedes.grid(
            row=0, column=3, padx=10, pady=10
        )

        tk.Button(
            frame,
            text="Registrar ejemplar",
            bg="green",
            fg="white",
            font=("Arial", 13, "bold"),
            command=self.registrar_ejemplar
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Cerrar ventana",
            bg="red",
            fg="white",
            font=("Arial", 13, "bold"),
            command=self.ventana.destroy
        ).pack(pady=5)

    def cargar_datos(self):
        try:
            self.libros = self.controlador.listar_libros()
            self.sedes = self.controlador.listar_sedes_activas()

            self.combo_libros["values"] = [
                f"{codigo} - {titulo}"
                for codigo, titulo in self.libros
            ]

            self.combo_sedes["values"] = [
                f"{codigo} - {nombre}"
                for codigo, nombre in self.sedes
            ]

            # Seleccionar el libro indicado desde Gestión de Libros
            indice = 0

            if self.codigo_libro_inicial is not None:
                for i, libro in enumerate(self.libros):
                    if libro[0] == int(self.codigo_libro_inicial):
                        indice = i
                        break

            if self.libros:
                self.combo_libros.current(indice)
                self.actualizar_tabla()

            if self.sedes:
                self.combo_sedes.current(0)

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )

    def actualizar_tabla(self):
        # Vaciar la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        indice = self.combo_libros.current()

        if indice < 0:
            return

        codigo_libro = self.libros[indice][0]

        try:
            ejemplares = self.controlador.consultar_ejemplares(
                codigo_libro
            )

            for ejemplar in ejemplares:
                self.tabla.insert(
                    "",
                    tk.END,
                    values=ejemplar
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )

    def registrar_ejemplar(self):
        indice_libro = self.combo_libros.current()
        indice_sede = self.combo_sedes.current()

        if indice_libro < 0 or indice_sede < 0:
            messagebox.showwarning(
                "Datos incompletos",
                "Debe seleccionar un libro y una sede activa.",
                parent=self.ventana
            )
            return

        codigo_libro = self.libros[indice_libro][0]
        id_sede = self.sedes[indice_sede][0]
        codigo_inventario = self.entrada_codigo.get()

        try:
            self.controlador.registrar_ejemplar(
                codigo_libro,
                id_sede,
                codigo_inventario
            )

            messagebox.showinfo(
                "Éxito",
                "Ejemplar registrado correctamente.",
                parent=self.ventana
            )

            self.entrada_codigo.delete(0, tk.END)
            self.actualizar_tabla()

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )
