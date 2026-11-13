import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

COLORES = ("#2a9d8f", "#e9c46a", "#e76f51", "#264653", "#8ab17d")


class VentanaReporte:
    """Muestra cualquier reporte de ControladorReporte: resumen, tabla y gráfico."""

    def __init__(self, reporte):
        self.reporte = reporte
        self.ventana = tk.Toplevel()
        self.ventana.title(f"Proyecto DAO - {reporte['titulo']}")
        self.ventana.geometry("1200x800")
        self.ventana.configure(bg="lightyellow")

        self.crear_encabezado()
        self.crear_tabla()
        self.crear_grafico()
        tk.Button(self.ventana, text="Cerrar", fg="white", bg="red", font=("Arial", 12, "bold"),
                  command=self.cerrar).pack(pady=5)

    def crear_encabezado(self):
        tk.Label(self.ventana, text=self.reporte["titulo"], fg="blue", bg="lightyellow",
                 font=("Arial", 20)).pack(pady=(10, 5))
        for linea in self.reporte["resumen"]:
            tk.Label(self.ventana, text=linea, bg="lightyellow", font=("Arial", 11),
                     wraplength=1100, justify="left").pack(anchor="w", padx=20)

    def crear_tabla(self):
        frame = tk.Frame(self.ventana, bg="lightyellow")
        frame.pack(fill="x", padx=20, pady=10)
        columnas = self.reporte["columnas"]
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=min(max(len(self.reporte["filas"]), 1), 8))
        ancho = max(80, 1100 // len(columnas))
        for columna in columnas:
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=ancho, anchor="center")
        for fila in self.reporte["filas"]:
            tabla.insert("", tk.END, values=fila)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="x", expand=True)
        scroll.pack(side="right", fill="y")

    def crear_grafico(self):
        grafico = self.reporte["grafico"]
        figura = Figure(figsize=(11, 4.2), dpi=90)
        ejes = figura.add_subplot(111)

        if not grafico["etiquetas"]:
            ejes.text(0.5, 0.5, "No hay datos para el período elegido", ha="center", va="center", fontsize=14)
            ejes.set_axis_off()
        elif grafico["tipo"] == "barras_horizontales":
            self._dibujar_barras_horizontales(ejes, grafico)
        elif grafico["tipo"] == "barras_apiladas":
            self._dibujar_barras_apiladas(ejes, grafico)
        else:
            self._dibujar_lineas(ejes, grafico)

        ejes.set_title(grafico["titulo"])
        figura.tight_layout()
        self.canvas = FigureCanvasTkAgg(figura, master=self.ventana)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20)

    def _dibujar_barras_horizontales(self, ejes, grafico):
        nombre, valores = next(iter(grafico["series"].items()))
        # Se invierte para que el primero del ranking quede arriba
        etiquetas, valores = grafico["etiquetas"][::-1], valores[::-1]
        barras = ejes.barh(etiquetas, valores, color=COLORES[0], label=nombre)
        anotaciones = grafico.get("anotaciones")
        if anotaciones:
            ejes.bar_label(barras, labels=anotaciones[::-1], padding=4)
        else:
            ejes.bar_label(barras, padding=4)
        ejes.set_xlabel(grafico.get("eje_x", ""))
        ejes.margins(x=0.15)

    def _dibujar_barras_apiladas(self, ejes, grafico):
        base = [0] * len(grafico["etiquetas"])
        for color, (nombre, valores) in zip(COLORES, grafico["series"].items()):
            ejes.bar(grafico["etiquetas"], valores, bottom=base, color=color, label=nombre)
            base = [acumulado + valor for acumulado, valor in zip(base, valores)]
        ejes.set_ylabel(grafico.get("eje_y", ""))
        ejes.set_ylim(0, 100)
        ejes.legend(loc="lower right")

    def _dibujar_lineas(self, ejes, grafico):
        for color, (nombre, valores) in zip(COLORES, grafico["series"].items()):
            ejes.plot(grafico["etiquetas"], valores, marker="o", color=color, label=nombre)
        ejes.set_ylabel(grafico.get("eje_y", ""))
        ejes.grid(axis="y", alpha=0.3)
        ejes.legend()

    def cerrar(self):
        self.ventana.destroy()
