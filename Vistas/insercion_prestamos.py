from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import platform
from Controlador.controlador_prestamo import ControladorPrestamo

class InsercionPrestamos:

    def __init__(self, al_registrar=None):
        self.windows_insercion_prestamo = tk.Toplevel()
        self.windows_properties()

        self.controlador_prestamos = ControladorPrestamo()
        # Función que se llama después de registrar un préstamo (para refrescar la tabla de gestión)
        self.al_registrar = al_registrar

        self.windows_components()
        self.cargar_combos()
        self.al_cambiar_tipo()

    def windows_properties(self):
        self.windows_insercion_prestamo.title("Proyecto DAO")
        self.windows_insercion_prestamo.geometry("800x650")
        self.windows_insercion_prestamo.configure(bg="lightyellow")
        self.windows_insercion_prestamo.resizable(False, False)

    def windows_components(self):
        frame_7 = tk.Frame(self.windows_insercion_prestamo)
        frame_7.configure(bg="lightyellow")

        label_name_form = tk.Label(frame_7, text="Registro de Préstamos")

        label_socio = tk.Label(frame_7, text="Seleccione el socio:")
        self.combo_socio = ttk.Combobox(frame_7, font=("Arial", 14), width=30, state="readonly")

        label_tipo = tk.Label(frame_7, text="Seleccione el tipo de préstamo:")
        self.combo_tipo = ttk.Combobox(frame_7, font=("Arial", 14), width=30, state="readonly",
                                       values=["Local", "Interbibliotecario"])
        self.combo_tipo.current(0)

        label_sede_origen = tk.Label(frame_7, text="Seleccione la sede de origen:")
        self.combo_sede_origen = ttk.Combobox(frame_7, font=("Arial", 14), width=30, state="readonly")

        label_sede_destino = tk.Label(frame_7, text="Seleccione la sede de destino:")
        self.combo_sede_destino = ttk.Combobox(frame_7, font=("Arial", 14), width=30, state="readonly")

        label_ejemplares = tk.Label(frame_7, text="Seleccione los ejemplares (clic para marcar o desmarcar):")
        self.lista_ejemplares = tk.Listbox(frame_7, font=("Arial", 14), width=32, height=6, selectmode=tk.MULTIPLE)

        if str(platform.system()) == "Windows":
            label_name_form.config(fg="blue", bg="lightyellow", font=("Arial", 25))
            label_socio.config(fg="black", bg="lightyellow", font=("Arial", 15))
            label_tipo.config(fg="black", bg="lightyellow", font=("Arial", 15))
            label_sede_origen.config(fg="black", bg="lightyellow", font=("Arial", 15))
            label_sede_destino.config(fg="black", bg="lightyellow", font=("Arial", 15))
            label_ejemplares.config(fg="black", bg="lightyellow", font=("Arial", 15))
            btn_insertar_datos = tk.Button(frame_7, text="Confirmar préstamo", cursor="Hand2")
            btn_cerrar = tk.Button(frame_7, text="Cerrar ventana", cursor="Hand2")
        else:
            label_name_form.config(fg="blue", bg="lightyellow")
            label_socio.config(fg="black", bg="lightyellow")
            label_tipo.config(fg="black", bg="lightyellow")
            label_sede_origen.config(fg="black", bg="lightyellow")
            label_sede_destino.config(fg="black", bg="lightyellow")
            label_ejemplares.config(fg="black", bg="lightyellow")
            btn_insertar_datos = tk.Button(frame_7, text="Confirmar préstamo")
            btn_cerrar = tk.Button(frame_7, text="Cerrar ventana")

        # Cuando cambia el tipo o la sede de origen, se actualizan los combos que dependen de ellos
        self.combo_tipo.bind("<<ComboboxSelected>>", self.al_cambiar_tipo)
        self.combo_sede_origen.bind("<<ComboboxSelected>>", self.al_cambiar_sede_origen)

        btn_cerrar.config(fg="white", bg="red", font=("Arial", 15, "bold"))
        btn_cerrar.config(command=self.cerrar_ventana)

        btn_insertar_datos.config(fg="white", bg="green", font=("Arial", 15, "bold"))
        btn_insertar_datos.config(command=self.insertar_prestamo)

        frame_7.pack()
        label_name_form.pack()
        label_socio.pack()
        self.combo_socio.pack()
        label_tipo.pack()
        self.combo_tipo.pack()
        label_sede_origen.pack()
        self.combo_sede_origen.pack()
        label_sede_destino.pack()
        self.combo_sede_destino.pack()
        label_ejemplares.pack()
        self.lista_ejemplares.pack()
        btn_insertar_datos.pack(pady=5)
        btn_cerrar.pack()

    def cargar_combos(self):
        # Socios: se muestra "legajo - Apellido, Nombre" y se guarda el legajo para usarlo después
        self.socios = self.controlador_prestamos.listar_socios_activos()
        self.combo_socio["values"] = [f"{legajo} - {apellido}, {nombre}" for legajo, nombre, apellido in self.socios]

        sedes = [str(fila[0]) for fila in self.controlador_prestamos.listar_sedes_activas()]
        self.combo_sede_origen["values"] = sedes
        self.combo_sede_destino["values"] = sedes

        self.ejemplares_disponibles = []

    def al_cambiar_tipo(self, event=None):
        # En un préstamo local la sede de destino es siempre la de origen
        if self.combo_tipo.get() == "Local":
            self.combo_sede_destino.set(self.combo_sede_origen.get())
            self.combo_sede_destino.config(state="disabled")
        else:
            self.combo_sede_destino.config(state="readonly")
            self.combo_sede_destino.set("")

    def al_cambiar_sede_origen(self, event=None):
        if self.combo_tipo.get() == "Local":
            self.combo_sede_destino.set(self.combo_sede_origen.get())

        # Solo se muestran los ejemplares disponibles de la sede de origen elegida
        self.lista_ejemplares.delete(0, tk.END)
        self.ejemplares_disponibles = self.controlador_prestamos.listar_ejemplares_disponibles(int(self.combo_sede_origen.get()))
        for id_ejemplar, codigo_libro in self.ejemplares_disponibles:
            self.lista_ejemplares.insert(tk.END, f"Ejemplar {id_ejemplar} (libro {codigo_libro})")

    def cerrar_ventana(self):
        self.windows_insercion_prestamo.destroy()

    def insertar_prestamo(self):
        if not self.combo_socio.get() or not self.combo_sede_origen.get() or not self.combo_sede_destino.get():
            messagebox.showwarning("Datos incompletos", "Complete el socio y las sedes.", parent=self.windows_insercion_prestamo)
            return

        legajo = self.socios[self.combo_socio.current()][0]
        id_sede_origen = int(self.combo_sede_origen.get())
        id_sede_destino = int(self.combo_sede_destino.get())
        tipo = self.combo_tipo.get()
        ids_ejemplares = [self.ejemplares_disponibles[i][0] for i in self.lista_ejemplares.curselection()]

        try:
            prestamo = self.controlador_prestamos.registrar_prestamo(
                legajo, id_sede_origen, id_sede_destino, tipo, None, ids_ejemplares)
        except ValueError as error:
            # Validaciones de negocio que no se cumplieron (socio inactivo, sede de baja, etc.)
            messagebox.showerror("No se puede registrar el préstamo", str(error), parent=self.windows_insercion_prestamo)
            return
        except Exception as error:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {error}", parent=self.windows_insercion_prestamo)
            return

        messagebox.showinfo("Préstamo registrado", f"Se registró el préstamo N° {prestamo.id_prestamo}.", parent=self.windows_insercion_prestamo)

        if self.al_registrar:
            self.al_registrar()

        # Los ejemplares prestados ya no están disponibles, así que recargamos la lista
        self.al_cambiar_sede_origen()
