import platform
import tkinter as tk
from tkinter import messagebox, ttk

from Controlador.controlador_multa import ControladorMulta
from Entidades.excepciones import ReglaNegocioError


def formatear_monto(monto):
    # $5300.0 -> "$5.300,00"
    return "$" + f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class PantallaGestionMulta:

    def __init__(self, legajo=None):
        self.ventana = tk.Toplevel()
        self.controlador_multas = ControladorMulta()

        self.windows_properties()
        self.windows_components()
        if legajo is not None:
            self.entry_legajo.insert(0, str(legajo))
        self.actualizar_tabla()

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

        tk.Label(frame, text="Gestión de Multas", fg="blue", bg="lightyellow", font=fuente_titulo).pack(pady=5)

        # Filtros
        frame_filtros = tk.Frame(frame, bg="lightyellow")
        frame_filtros.pack(pady=5)
        tk.Label(frame_filtros, text="Estado:", bg="lightyellow", font=fuente_texto).pack(side="left")
        self.combo_estado = ttk.Combobox(frame_filtros, state="readonly", width=12, font=("Arial", 12),
                                         values=ControladorMulta.ESTADOS)
        self.combo_estado.set("Pendientes")
        self.combo_estado.pack(side="left", padx=5)
        tk.Label(frame_filtros, text="Legajo:", bg="lightyellow", font=fuente_texto).pack(side="left", padx=(15, 0))
        self.entry_legajo = tk.Entry(frame_filtros, font=("Arial", 12), width=14)
        self.entry_legajo.bind("<Return>", lambda evento: self.actualizar_tabla())
        self.entry_legajo.pack(side="left", padx=5)
        self.crear_boton(frame_filtros, "Filtrar", "blue", self.actualizar_tabla).pack(side="left", padx=5)
        self.crear_boton(frame_filtros, "Limpiar", "gray", self.limpiar_filtros).pack(side="left", padx=5)

        # Deuda del socio filtrado
        self.label_resumen = tk.Label(frame, text="", bg="lightyellow", font=("Arial", 13, "bold"))
        self.label_resumen.pack(pady=5)

        # Tabla (se pueden seleccionar varias filas con Ctrl o Shift)
        columnas = (("id", "N°", 50), ("socio", "Socio", 200), ("motivo", "Motivo", 80),
                    ("libro", "Libro", 200), ("prestamo", "Préstamo", 80), ("monto", "Monto", 100),
                    ("generada", "Generada", 100), ("pagada", "Pagada", 100), ("estado", "Estado", 90))
        frame_tabla = tk.Frame(frame, bg="lightyellow")
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tabla = ttk.Treeview(frame_tabla, columns=[c[0] for c in columnas], show="headings",
                                  selectmode="extended", height=14)
        for clave, titulo, ancho in columnas:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, anchor="w" if clave in ("socio", "libro") else "center")
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill=tk.BOTH, expand=True)
        scroll.pack(side="right", fill="y")

        # Acciones
        frame_botones = tk.Frame(frame, bg="lightyellow")
        frame_botones.pack(pady=5)
        self.crear_boton(frame_botones, "Pagar seleccionadas", "green", self.pagar_seleccionadas).pack(side="left", padx=5)
        self.crear_boton(frame_botones, "Pagar todas del socio", "teal", self.pagar_todas).pack(side="left", padx=5)
        self.crear_boton(frame_botones, "Cerrar ventana", "red", self.ventana.destroy).pack(side="left", padx=5)

    def crear_boton(self, padre, texto, color, comando):
        return tk.Button(padre, text=texto, fg="white", bg=color, font=("Arial", 13, "bold"),
                         cursor=self.cursor, command=comando)

    def actualizar_tabla(self):
        legajo = self.entry_legajo.get().strip() or None
        try:
            filas = self.controlador_multas.consultar_multas(self.combo_estado.get(), legajo)
            resumen = self.controlador_multas.consultar_deuda(legajo) if legajo else None
        except ReglaNegocioError as error:
            messagebox.showerror("Filtro inválido", str(error), parent=self.ventana)
            return

        self.tabla.delete(*self.tabla.get_children())
        self.montos = {}
        for fila in filas:
            self.montos[str(fila[0])] = (fila[1], fila[5], fila[8])
            valores = list(fila)
            valores[5] = formatear_monto(fila[5])
            self.tabla.insert("", tk.END, iid=str(fila[0]), values=valores)

        if resumen:
            nombre, cantidad, total = resumen
            texto = f"{nombre}: {cantidad} multa(s) pendiente(s) por {formatear_monto(total)}" if cantidad \
                else f"{nombre}: no tiene multas pendientes"
            self.label_resumen.config(text=texto, fg="darkred" if cantidad else "darkgreen")
        else:
            self.label_resumen.config(text="")

    def limpiar_filtros(self):
        self.entry_legajo.delete(0, tk.END)
        self.combo_estado.set("Pendientes")
        self.actualizar_tabla()

    def pagar_seleccionadas(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione una o más multas de la tabla.", parent=self.ventana)
            return

        total = sum(self.montos[iid][1] for iid in seleccion if self.montos[iid][2] == "Pendiente")
        if not messagebox.askyesno("Confirmar pago",
                                   f"¿Registrar el pago de {len(seleccion)} multa(s) por {formatear_monto(total)}?",
                                   parent=self.ventana):
            return
        try:
            pagado = self.controlador_multas.pagar_multas([int(iid) for iid in seleccion])
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede registrar el pago", str(error), parent=self.ventana)
            return
        messagebox.showinfo("Pago registrado", f"Se registró un pago de {formatear_monto(pagado)}.",
                            parent=self.ventana)
        self.actualizar_tabla()

    def pagar_todas(self):
        legajo = self.entry_legajo.get().strip()
        if not legajo:
            # Sin filtro, se toma el socio de la fila seleccionada ("legajo - Apellido, Nombre")
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showwarning("Sin socio", "Filtre por legajo o seleccione una multa del socio.",
                                       parent=self.ventana)
                return
            legajo = self.montos[seleccion[0]][0].split(" - ")[0]

        try:
            nombre, cantidad, total = self.controlador_multas.consultar_deuda(legajo)
            if cantidad and not messagebox.askyesno(
                    "Confirmar pago", f"¿Registrar el pago de las {cantidad} multa(s) pendiente(s) de {nombre} "
                                      f"por {formatear_monto(total)}?", parent=self.ventana):
                return
            cantidad, total = self.controlador_multas.pagar_todas_del_socio(legajo)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede registrar el pago", str(error), parent=self.ventana)
            return
        messagebox.showinfo("Pago registrado",
                            f"Se pagaron {cantidad} multa(s) de {nombre} por {formatear_monto(total)}.",
                            parent=self.ventana)
        self.actualizar_tabla()
