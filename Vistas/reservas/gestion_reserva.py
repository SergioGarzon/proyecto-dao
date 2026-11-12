import platform
import tkinter as tk
from tkinter import messagebox, ttk

from Controlador.controlador_reserva import ControladorReserva
from Entidades.enums import EstadoReserva
from Entidades.excepciones import ReglaNegocioError
from Vistas.reservas.insercion_reserva import InsercionReserva

TODOS = "Todos"


class PantallaGestionReserva:

    def __init__(self):
        self.ventana = tk.Toplevel()
        self.controlador_reservas = ControladorReserva()

        self.windows_properties()
        self.windows_components()
        # Al abrir, se ponen al día los vencimientos y las asignaciones pendientes
        self.procesar_reservas(silencioso=True)

    def windows_properties(self):
        self.ventana.title("Proyecto DAO")
        self.ventana.geometry("1150x650")
        self.ventana.configure(bg="lightyellow")
        self.ventana.resizable(False, False)

    def windows_components(self):
        es_windows = platform.system() == "Windows"
        fuente_titulo = ("Arial", 25) if es_windows else None
        fuente_texto = ("Arial", 13) if es_windows else None
        self.cursor = "hand2" if es_windows else ""

        frame = tk.Frame(self.ventana, bg="lightyellow")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Gestión de Reservas", fg="blue", bg="lightyellow", font=fuente_titulo).pack(pady=5)

        # Filtros
        frame_filtros = tk.Frame(frame, bg="lightyellow")
        frame_filtros.pack(pady=5)
        tk.Label(frame_filtros, text="Estado:", bg="lightyellow", font=fuente_texto).pack(side="left")
        self.combo_estado = ttk.Combobox(frame_filtros, state="readonly", width=15, font=("Arial", 12),
                                         values=[TODOS] + [estado.value for estado in EstadoReserva])
        self.combo_estado.current(0)
        self.combo_estado.pack(side="left", padx=5)
        tk.Label(frame_filtros, text="Legajo:", bg="lightyellow", font=fuente_texto).pack(side="left", padx=(15, 0))
        self.entry_legajo = tk.Entry(frame_filtros, font=("Arial", 12), width=14)
        self.entry_legajo.pack(side="left", padx=5)
        self.crear_boton(frame_filtros, "Filtrar", "blue", self.actualizar_tabla).pack(side="left", padx=5)

        # Tabla
        columnas = (("id", "N°", 50), ("legajo", "Legajo", 80), ("socio", "Socio", 160), ("libro", "Libro", 190),
                    ("sede", "Sede de retiro", 120), ("fecha", "Fecha reserva", 100), ("ejemplar", "Ejemplar", 90),
                    ("expira", "Retirar hasta", 100), ("estado", "Estado", 90))
        frame_tabla = tk.Frame(frame, bg="lightyellow")
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tabla = ttk.Treeview(frame_tabla, columns=[c[0] for c in columnas], show="headings", height=15)
        for clave, titulo, ancho in columnas:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, anchor="center")
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill=tk.BOTH, expand=True)
        scroll.pack(side="right", fill="y")

        # Acciones
        frame_botones = tk.Frame(frame, bg="lightyellow")
        frame_botones.pack(pady=5)
        self.crear_boton(frame_botones, "Nueva reserva", "green", self.nueva_reserva).pack(side="left", padx=5)
        self.crear_boton(frame_botones, "Registrar retiro", "teal", self.cumplir_reserva).pack(side="left", padx=5)
        self.crear_boton(frame_botones, "Cancelar reserva", "orange", self.cancelar_reserva).pack(side="left", padx=5)
        self.crear_boton(frame_botones, "Procesar vencimientos", "purple",
                         self.procesar_reservas).pack(side="left", padx=5)
        self.crear_boton(frame_botones, "Cerrar ventana", "red", self.ventana.destroy).pack(side="left", padx=5)

    def crear_boton(self, padre, texto, color, comando):
        return tk.Button(padre, text=texto, fg="white", bg=color, font=("Arial", 13, "bold"),
                         cursor=self.cursor, command=comando)

    def actualizar_tabla(self):
        estado = self.combo_estado.get()
        try:
            filas = self.controlador_reservas.consultar_reservas(
                estado=None if estado == TODOS else estado, legajo=self.entry_legajo.get().strip() or None)
        except ReglaNegocioError as error:
            messagebox.showerror("Filtro inválido", str(error), parent=self.ventana)
            return

        self.tabla.delete(*self.tabla.get_children())
        for fila in filas:
            self.tabla.insert("", tk.END, values=fila)

    def reserva_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione una reserva de la tabla.", parent=self.ventana)
            return None
        return int(self.tabla.item(seleccion[0], "values")[0])

    def nueva_reserva(self):
        InsercionReserva(self.actualizar_tabla)

    def cumplir_reserva(self):
        id_reserva = self.reserva_seleccionada()
        if id_reserva is None:
            return
        try:
            id_prestamo = self.controlador_reservas.cumplir_reserva(id_reserva)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede registrar el retiro", str(error), parent=self.ventana)
        else:
            messagebox.showinfo("Retiro registrado",
                                f"La reserva {id_reserva} se cumplió y se registró el préstamo N° {id_prestamo}.",
                                parent=self.ventana)
        self.actualizar_tabla()

    def cancelar_reserva(self):
        id_reserva = self.reserva_seleccionada()
        if id_reserva is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Cancelar la reserva {id_reserva}?", parent=self.ventana):
            return
        try:
            self.controlador_reservas.cancelar_reserva(id_reserva)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede cancelar", str(error), parent=self.ventana)
        else:
            messagebox.showinfo("Reserva cancelada", f"Se canceló la reserva {id_reserva}.", parent=self.ventana)
        self.actualizar_tabla()

    def procesar_reservas(self, silencioso=False):
        vencidas, asignadas = self.controlador_reservas.procesar_reservas()
        self.actualizar_tabla()
        if not silencioso or vencidas or asignadas:
            messagebox.showinfo("Reservas al día",
                                f"Reservas vencidas: {vencidas}\nReservas que recibieron un ejemplar: {asignadas}",
                                parent=self.ventana)
