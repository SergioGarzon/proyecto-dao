
import tkinter as tk
from tkinter import messagebox

from Controlador.controlador_libro import ControladorLibro


class FormularioLibro:

    def __init__(self, ventana_padre, actualizar_tabla, datos=None):
        self.ventana = tk.Toplevel(ventana_padre)
        self.controlador = ControladorLibro()
        self.actualizar_tabla = actualizar_tabla
        self.datos = datos

        self.ventana.title("Formulario de Libros")
        self.ventana.geometry("500x400")
        self.ventana.configure(bg="lightyellow")
        self.ventana.resizable(False, False)

        self.crear_formulario()

        # Mantiene el formulario asociado a su ventana principal
        self.ventana.transient(ventana_padre)
        self.ventana.grab_set()

    def crear_formulario(self):

        titulo = "Modificar libro" if self.datos else "Crear libro"

        tk.Label(
            self.ventana,
            text=titulo,
            font=("Arial", 22),
            fg="blue",
            bg="lightyellow"
        ).pack(pady=15)

        frame = tk.Frame(self.ventana, bg="lightyellow")
        frame.pack(pady=10)

        campos = [
            ("ISBN", "isbn"),
            ("Título", "titulo"),
            ("Autor", "autor"),
            ("Editorial", "editorial"),
            ("Año de publicación", "anio")
        ]

        self.entradas = {}

        for fila, (etiqueta, campo) in enumerate(campos):

            tk.Label(
                frame,
                text=etiqueta + ":",
                font=("Arial", 12),
                bg="lightyellow"
            ).grid(row=fila, column=0, padx=10, pady=8, sticky="e")

            entrada = tk.Entry(frame, font=("Arial", 12), width=25)
            entrada.grid(row=fila, column=1, padx=10, pady=8)

            self.entradas[campo] = entrada

        # Si estamos modificando, cargamos los datos existentes
        if self.datos:
            valores = {
                "isbn": self.datos[1],
                "titulo": self.datos[2],
                "autor": self.datos[3],
                "editorial": self.datos[4],
                "anio": self.datos[5]
            }

            for campo, valor in valores.items():
                self.entradas[campo].insert(0, str(valor))

        tk.Button(
            self.ventana,
            text="Guardar libro",
            bg="green",
            fg="white",
            font=("Arial", 13, "bold"),
            command=self.guardar_libro
        ).pack(pady=15)

    def guardar_libro(self):

        isbn = self.entradas["isbn"].get()
        titulo = self.entradas["titulo"].get()
        autor = self.entradas["autor"].get()
        editorial = self.entradas["editorial"].get()
        anio = self.entradas["anio"].get()

        try:
            if self.datos:
                # Modificar un libro existente
                codigo = self.datos[0]

                self.controlador.modificar_libro(
                    codigo, isbn, titulo, autor, editorial, anio
                )
                mensaje = "Libro modificado correctamente."
            else:
                # Crear un libro nuevo
                self.controlador.insertar_libro(
                    isbn, titulo, autor, editorial, anio
                )
                mensaje = "Libro registrado correctamente."

            messagebox.showinfo(
                "Éxito",
                mensaje,
                parent=self.ventana
            )

            self.ventana.destroy()
            self.actualizar_tabla()

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )
