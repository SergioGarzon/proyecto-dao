import platform
import tkinter as tk
from tkinter import messagebox, ttk

from Controlador.controlador_ejemplar import ControladorEjemplar
from Controlador.controlador_prestamo import ControladorPrestamo
from Controlador.controlador_reserva import ControladorReserva
from Entidades.excepciones import ReglaNegocioError


class InsercionReserva:

    def __init__(self, al_registrar=None):
        self.ventana = tk.Toplevel()
        self.controlador_reservas = ControladorReserva()
        # Función que se llama después de crear la reserva (para refrescar la tabla de gestión)
        self.al_registrar = al_registrar

        self.windows_properties()
        self.windows_components()
        self.cargar_combos()

    def windows_properties(self):
        self.ventana.title("Proyecto DAO")
        self.ventana.geometry("700x520")
        self.ventana.configure(bg="lightyellow")
        self.ventana.resizable(False, False)

    def windows_components(self):
        es_windows = platform.system() == "Windows"
        fuente_titulo = ("Arial", 25) if es_windows else None
        fuente_texto = ("Arial", 15) if es_windows else None
        cursor = "hand2" if es_windows else ""

        frame = tk.Frame(self.ventana, bg="lightyellow")
        frame.pack(pady=10)

        tk.Label(frame, text="Nueva Reserva", fg="blue", bg="lightyellow", font=fuente_titulo).pack(pady=5)

        tk.Label(frame, text="Seleccione el socio:", bg="lightyellow", font=fuente_texto).pack()
        self.combo_socio = ttk.Combobox(frame, font=("Arial", 14), width=35, state="readonly")
        self.combo_socio.pack(pady=3)

        tk.Label(frame, text="Seleccione el libro:", bg="lightyellow", font=fuente_texto).pack()
        self.combo_libro = ttk.Combobox(frame, font=("Arial", 14), width=35, state="readonly")
        self.combo_libro.pack(pady=3)

        tk.Label(frame, text="Seleccione la sede de retiro:", bg="lightyellow", font=fuente_texto).pack()
        self.combo_sede = ttk.Combobox(frame, font=("Arial", 14), width=35, state="readonly")
        self.combo_sede.pack(pady=3)

        # Aviso de disponibilidad: se actualiza al elegir libro y sede
        self.label_disponibilidad = tk.Label(frame, text="", bg="lightyellow", font=fuente_texto)
        self.label_disponibilidad.pack(pady=10)

        self.combo_libro.bind("<<ComboboxSelected>>", self.mostrar_disponibilidad)
        self.combo_sede.bind("<<ComboboxSelected>>", self.mostrar_disponibilidad)

        tk.Button(frame, text="Confirmar reserva", fg="white", bg="green", font=("Arial", 15, "bold"),
                  cursor=cursor, command=self.confirmar_reserva).pack(pady=5)
        tk.Button(frame, text="Cerrar ventana", fg="white", bg="red", font=("Arial", 15, "bold"),
                  cursor=cursor, command=self.ventana.destroy).pack()

    def cargar_combos(self):
        self.socios = ControladorPrestamo().listar_socios_activos()
        self.combo_socio["values"] = [f"{legajo} - {apellido}, {nombre}" for legajo, nombre, apellido in self.socios]

        controlador_ejemplares = ControladorEjemplar()
        self.libros = controlador_ejemplares.listar_libros()
        self.combo_libro["values"] = [f"{codigo} - {titulo}" for codigo, titulo in self.libros]

        self.sedes = controlador_ejemplares.listar_sedes_activas()
        self.combo_sede["values"] = [f"{id_sede} - {nombre}" for id_sede, nombre in self.sedes]

    def mostrar_disponibilidad(self, event=None):
        if self.combo_libro.current() < 0 or self.combo_sede.current() < 0:
            return
        codigo_libro = self.libros[self.combo_libro.current()][0]
        id_sede = self.sedes[self.combo_sede.current()][0]
        cantidad = self.controlador_reservas.consultar_disponibilidad(codigo_libro, id_sede)
        if cantidad > 0:
            self.label_disponibilidad.config(
                text=f"{cantidad} ejemplar(es) disponible(s): la reserva se asigna en el momento.", fg="green")
        else:
            self.label_disponibilidad.config(
                text="No hay ejemplares disponibles: la reserva quedará pendiente.", fg="darkorange")

    def confirmar_reserva(self):
        if self.combo_socio.current() < 0 or self.combo_libro.current() < 0 or self.combo_sede.current() < 0:
            messagebox.showwarning("Datos incompletos", "Seleccione el socio, el libro y la sede.", parent=self.ventana)
            return

        legajo = self.socios[self.combo_socio.current()][0]
        codigo_libro = self.libros[self.combo_libro.current()][0]
        id_sede = self.sedes[self.combo_sede.current()][0]

        try:
            id_reserva, estado = self.controlador_reservas.crear_reserva(legajo, codigo_libro, id_sede)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede registrar la reserva", str(error), parent=self.ventana)
            return

        messagebox.showinfo("Reserva registrada", f"Se registró la reserva N° {id_reserva} en estado {estado}.",
                            parent=self.ventana)
        if self.al_registrar:
            self.al_registrar()
        self.mostrar_disponibilidad()
