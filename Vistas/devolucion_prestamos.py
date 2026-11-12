from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import platform
from Controlador.controlador_prestamo import ControladorPrestamo
from Entidades.enums import EstadoFisico
from Entidades.excepciones import ReglaNegocioError

class DevolucionPrestamos:

    def __init__(self, id_prestamo, al_registrar=None):
        self.id_prestamo = id_prestamo
        # Función que se llama después de registrar una devolución (para refrescar la tabla de gestión)
        self.al_registrar = al_registrar
        self.controlador_prestamos = ControladorPrestamo()

        # Se consulta antes de crear la ventana: si el préstamo no está activo, no queda abierta y vacía
        self.pendientes = self.controlador_prestamos.consultar_pendientes(id_prestamo)

        self.windows_devolucion = tk.Toplevel()
        self.windows_properties()
        self.windows_components()
        self.mostrar_pendientes()

    def windows_properties(self):
        self.windows_devolucion.title("Proyecto DAO")
        self.windows_devolucion.geometry("800x650")
        self.windows_devolucion.configure(bg="lightyellow")
        self.windows_devolucion.resizable(False, False)

    def windows_components(self):
        frame_8 = tk.Frame(self.windows_devolucion)
        frame_8.configure(bg="lightyellow")

        encabezado = self.controlador_prestamos.consultar_encabezado(self.id_prestamo)
        label_name_form = tk.Label(frame_8, text=f"Devolución del préstamo {encabezado}")

        label_ejemplares = tk.Label(frame_8, text="Seleccione los ejemplares (clic para marcar o desmarcar):")
        self.lista_ejemplares = tk.Listbox(frame_8, font=("Arial", 14), width=50, height=6, selectmode=tk.MULTIPLE)

        # Solo informa: los ejemplares ya devueltos no se pueden seleccionar
        label_devueltos = tk.Label(frame_8, text="Ya devueltos (no se pueden seleccionar):")
        self.lista_devueltos = tk.Listbox(frame_8, font=("Arial", 14), width=50, height=4, state="disabled",
                                          disabledforeground="gray")

        label_fisico = tk.Label(frame_8, text="Seleccione el estado físico:")
        self.combo_fisico = ttk.Combobox(frame_8, font=("Arial", 14), width=30, state="readonly",
                                         values=[estado.value for estado in EstadoFisico])
        self.combo_fisico.current(0)

        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))
            label_ejemplares.config(fg="black", bg="lightyellow", font=("Arial", 15))
            label_devueltos.config(fg="black", bg="lightyellow", font=("Arial", 15))
            label_fisico.config(fg="black", bg="lightyellow", font=("Arial", 15))
            btn_confirmar = tk.Button(frame_8, text="Confirmar devolución", cursor="Hand2")
            btn_cerrar = tk.Button(frame_8, text="Cerrar ventana", cursor="Hand2")
        else:
            label_name_form.config(fg="blue", bg="lightyellow")
            label_ejemplares.config(fg="black", bg="lightyellow")
            label_devueltos.config(fg="black", bg="lightyellow")
            label_fisico.config(fg="black", bg="lightyellow")
            btn_confirmar = tk.Button(frame_8, text="Confirmar devolución")
            btn_cerrar = tk.Button(frame_8, text="Cerrar ventana")

        btn_confirmar.config(fg="white", bg="green", font=("Arial", 15, "bold"))
        btn_confirmar.config(command=self.confirmar_devolucion)

        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))
        btn_cerrar.config(command=self.cerrar_ventana)

        frame_8.pack()
        label_name_form.pack()
        label_ejemplares.pack()
        self.lista_ejemplares.pack()
        label_devueltos.pack()
        self.lista_devueltos.pack()
        label_fisico.pack()
        self.combo_fisico.pack()
        btn_confirmar.pack(pady=5)
        btn_cerrar.pack()

    def mostrar_pendientes(self):
        self.lista_ejemplares.delete(0, tk.END)
        for _, _, codigo_inventario, titulo, fisico_salida in self.pendientes:
            self.lista_ejemplares.insert(tk.END, f"{codigo_inventario} - {titulo} (salió {fisico_salida})")

        # Un Listbox deshabilitado no acepta cambios: se habilita solo para cargarlo
        self.lista_devueltos.config(state="normal")
        self.lista_devueltos.delete(0, tk.END)
        for codigo_inventario, titulo, fecha, fisico in self.controlador_prestamos.consultar_devueltos(self.id_prestamo):
            self.lista_devueltos.insert(tk.END, f"{codigo_inventario} - {titulo} ({fecha}, {fisico})")
        self.lista_devueltos.config(state="disabled")

    def confirmar_devolucion(self):
        ids_detalle = [self.pendientes[i][0] for i in self.lista_ejemplares.curselection()]

        try:
            total_multas = self.controlador_prestamos.registrar_devolucion(
                self.id_prestamo, ids_detalle, self.combo_fisico.get())
        except ReglaNegocioError as error:
            messagebox.showerror("No se puede registrar la devolución", str(error), parent=self.windows_devolucion)
            return
        except Exception as error:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {error}", parent=self.windows_devolucion)
            return

        mensaje = f"Se generaron multas por ${total_multas:.2f}." if total_multas else "No se generaron multas."
        messagebox.showinfo("Devolución registrada", mensaje, parent=self.windows_devolucion)

        if self.al_registrar:
            self.al_registrar()

        self.pendientes = [fila for fila in self.pendientes if fila[0] not in ids_detalle]
        if self.pendientes:
            self.mostrar_pendientes()
        else:
            self.cerrar_ventana()

    def cerrar_ventana(self):
        self.windows_devolucion.destroy()
