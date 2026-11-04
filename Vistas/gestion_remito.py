import platform
import tkinter as tk
from tkinter import messagebox, ttk

from Controlador.controlador_remito import ControladorRemito
from Entidades.estado_remito import ESTADOS_REMITO
from Entidades.excepciones import ReglaNegocioError

ETIQUETAS_ESTADO = {"EnTransito": "En tránsito", "Danado": "Dañado"}


def etiqueta(estado):
    return ETIQUETAS_ESTADO.get(estado, estado)


class PantallaGestionRemito:

    def __init__(self):
        self.windows_gestion_remito = tk.Toplevel()
        self.windows_properties()

        self.controlador_remitos = ControladorRemito()

        self.windows_components()

    def windows_properties(self):
        self.windows_gestion_remito.title("Proyecto DAO")
        self.windows_gestion_remito.geometry("1250x650")
        self.windows_gestion_remito.configure(bg="lightyellow")
        self.windows_gestion_remito.resizable(False, False)

    def crear_boton(self, frame, texto, color, comando):
        boton = tk.Button(frame, text=texto, fg="white", bg=color, font=("Arial", 11, "bold"), command=comando)
        if str(platform.system()) == "Windows":
            boton.config(cursor="Hand2")
        return boton

    def windows_components(self):
        frame_7 = tk.Frame(self.windows_gestion_remito)
        frame_7.configure(bg="lightyellow")

        label_name_form = tk.Label(frame_7, text="Gestión de Remitos y Envíos")

        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))
        else:
            label_name_form.config(fg="blue", bg="lightyellow")

        # Filtro por estado del remito
        frame_filtro = tk.Frame(frame_7, bg="lightyellow")
        label_filtro = tk.Label(frame_filtro, text="Filtrar por estado:", bg="lightyellow", font=("Arial", 12))
        self.combo_estado = ttk.Combobox(frame_filtro, state="readonly", width=15, font=("Arial", 12),
                                         values=["Todos"] + [etiqueta(estado) for estado in ESTADOS_REMITO])
        self.combo_estado.set("Todos")
        self.combo_estado.bind("<<ComboboxSelected>>", lambda evento: self.actualizar_tabla())
        label_filtro.pack(side="left", padx=5)
        self.combo_estado.pack(side="left")

        columnas = ("Numero", "Tipo", "Prestamo", "Sede_Origen", "Sede_Destino", "Fecha_Emision", "Estado", "Ejemplares")

        self.tabla = ttk.Treeview(frame_7, columns=columnas, show="headings", selectmode="browse")

        self.tabla.heading("Numero", text="N° Remito")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Prestamo", text="N° Préstamo")
        self.tabla.heading("Sede_Origen", text="Sede Origen")
        self.tabla.heading("Sede_Destino", text="Sede Destino")
        self.tabla.heading("Fecha_Emision", text="Fecha Emisión")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Ejemplares", text="Ejemplares")

        self.tabla.column("Numero", width=110, anchor="center")
        self.tabla.column("Tipo", width=70, anchor="center")
        self.tabla.column("Prestamo", width=90, anchor="center")
        self.tabla.column("Sede_Origen", width=220, anchor="center")
        self.tabla.column("Sede_Destino", width=220, anchor="center")
        self.tabla.column("Fecha_Emision", width=110, anchor="center")
        self.tabla.column("Estado", width=110, anchor="center")
        self.tabla.column("Ejemplares", width=160, anchor="center")

        # Traemos los datos de la base de datos
        self.actualizar_tabla()

        # Observación opcional que se guarda en el historial del remito
        frame_observacion = tk.Frame(frame_7, bg="lightyellow")
        label_observacion = tk.Label(frame_observacion, text="Observación (opcional):", bg="lightyellow", font=("Arial", 12))
        self.entry_observacion = tk.Entry(frame_observacion, width=70, font=("Arial", 12))
        label_observacion.pack(side="left", padx=5)
        self.entry_observacion.pack(side="left")

        frame_botones = tk.Frame(frame_7, bg="lightyellow")
        botones = [("Despachado", "blue", self.despachar),
                   ("En tránsito", "orange", self.iniciar_transito),
                   ("Recibido", "green", self.recibir),
                   ("Reportar daño", "purple", self.reportar_danio),
                   ("Reportar extravío", "brown", self.reportar_extravio),
                   ("Ver historial", "gray", self.ver_historial)]
        for texto, color, comando in botones:
            self.crear_boton(frame_botones, texto, color, comando).pack(side="left", padx=5)

        btn_actualizar = self.crear_boton(frame_7, "Actualizar tabla de remitos", "green", self.actualizar_tabla)
        btn_cerrar = self.crear_boton(frame_7, "Cerrar ventana", "red", self.cerrar_ventana)

        frame_7.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        label_name_form.pack(pady=5)
        frame_filtro.pack(pady=5)
        btn_actualizar.pack(pady=5)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)
        frame_observacion.pack(pady=5)
        frame_botones.pack(pady=5)
        btn_cerrar.pack(pady=10)

    def actualizar_tabla(self):
        # Guardamos la fila elegida para dejarla seleccionada después de recargar
        seleccion_previa = self.tabla.selection()
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        seleccionado = self.combo_estado.get()
        estado = None
        for nombre in ESTADOS_REMITO:
            if etiqueta(nombre) == seleccionado:
                estado = nombre

        for fila in self.controlador_remitos.consultar_remitos(estado):
            valores = list(fila[1:])
            valores[6] = etiqueta(valores[6])
            self.tabla.insert("", tk.END, iid=str(fila[0]), values=valores)

        if seleccion_previa and seleccion_previa[0] in self.tabla.get_children():
            self.tabla.selection_set(seleccion_previa[0])

    def _remito_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione un remito de la tabla.", parent=self.windows_gestion_remito)
            return None
        return int(seleccion[0])

    def _ejecutar(self, operacion, estado_nuevo):
        id_remito = self._remito_seleccionado()
        if id_remito is None:
            return
        numero = self.tabla.item(str(id_remito), "values")[0]

        observacion = self.entry_observacion.get()
        try:
            operacion(id_remito, observacion)
            self.entry_observacion.delete(0, tk.END)
            messagebox.showinfo("Estado actualizado", f"El remito {numero} pasó a estado: {estado_nuevo}.",
                                parent=self.windows_gestion_remito)
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede realizar la operación", str(error), parent=self.windows_gestion_remito)
        self.actualizar_tabla()

    def despachar(self):
        self._ejecutar(self.controlador_remitos.despachar, "Despachado")

    def iniciar_transito(self):
        self._ejecutar(self.controlador_remitos.iniciar_transito, "En tránsito")

    def recibir(self):
        self._ejecutar(self.controlador_remitos.recibir, "Recibido")

    def reportar_danio(self):
        self._ejecutar(self.controlador_remitos.reportar_danio, "Dañado")

    def reportar_extravio(self):
        self._ejecutar(self.controlador_remitos.reportar_extravio, "Extraviado")

    def ver_historial(self):
        id_remito = self._remito_seleccionado()
        if id_remito is None:
            return

        ventana = tk.Toplevel(self.windows_gestion_remito)
        ventana.title("Trazabilidad del remito")
        ventana.geometry("800x300")
        ventana.configure(bg="lightyellow")

        tabla = ttk.Treeview(ventana, columns=("Fecha", "Desde", "Hacia", "Observacion"), show="headings")
        for columna, titulo, ancho in (("Fecha", "Fecha y hora", 160), ("Desde", "Estado anterior", 120),
                                       ("Hacia", "Estado nuevo", 120), ("Observacion", "Observación", 350)):
            tabla.heading(columna, text=titulo)
            tabla.column(columna, width=ancho, anchor="center")

        for fecha, desde, hacia, observacion in self.controlador_remitos.consultar_historial(id_remito):
            tabla.insert("", tk.END, values=(fecha.strftime("%d/%m/%Y %H:%M"), etiqueta(desde), etiqueta(hacia), observacion))

        tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cerrar_ventana(self):
        self.windows_gestion_remito.destroy()


if __name__ == "__main__":
    # Para probar la pantalla sola:  python -m Vistas.gestion_remito
    from Persistencia.conexion import ConexionBD
    ConexionBD().crear_tablas()
    raiz = tk.Tk()
    raiz.withdraw()
    pantalla = PantallaGestionRemito()
    pantalla.windows_gestion_remito.bind(
        "<Destroy>", lambda evento: raiz.quit() if evento.widget is pantalla.windows_gestion_remito else None)
    raiz.mainloop()