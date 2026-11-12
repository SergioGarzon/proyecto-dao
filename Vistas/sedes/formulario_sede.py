"""Formulario compartido para crear y modificar sedes (Tkinter)."""
import tkinter as tk
from tkinter import messagebox

from Controlador.controlador_sede import ControladorSede
from Entidades.excepciones import ReglaNegocioError


class FormularioSede:
    CAMPOS = (
        ('nombre', 'Nombre de la sede *'),
        ('direccion', 'Dirección (calle y altura) *'),
        ('barrio', 'Barrio *'),
        ('localidad', 'Localidad *'),
        ('telefono', 'Teléfono'),
        ('email', 'Email'),
        ('hora_apertura', 'Hora de apertura (HH:MM) *'),
        ('hora_cierre', 'Hora de cierre (HH:MM) *'),
    )

    def __init__(self, padre, al_guardar, datos=None):
        self.padre = padre
        self.al_guardar = al_guardar
        self.datos = datos
        self.controlador_sedes = ControladorSede()
        self.ventana = tk.Toplevel(padre)
        self.ventana.title('Modificar sede' if datos else 'Crear sede')
        self.ventana.geometry('570x560')
        self.ventana.resizable(False, False)
        self.ventana.configure(bg='lightyellow')
        self.ventana.transient(padre)
        self.entradas = {}
        self.crear_componentes()
        self.ventana.grab_set()
        self.ventana.protocol('WM_DELETE_WINDOW', self.cerrar)

    def crear_componentes(self):
        marco = tk.Frame(self.ventana, bg='lightyellow')
        marco.pack(fill='both', expand=True, padx=22, pady=14)
        titulo = 'Modificar sede' if self.datos else 'Nueva sede'
        tk.Label(marco, text=titulo, font=('Arial', 23, 'bold'),
                 fg='blue', bg='lightyellow').grid(row=0, column=0, columnspan=2, pady=(0, 12))

        for fila, (clave, etiqueta) in enumerate(self.CAMPOS, start=1):
            tk.Label(marco, text=etiqueta, font=('Arial', 11),
                     bg='lightyellow').grid(row=fila, column=0, sticky='w', pady=8)
            entrada = tk.Entry(marco, font=('Arial', 12), width=30)
            entrada.grid(row=fila, column=1, padx=(12, 0), sticky='ew')
            self.entradas[clave] = entrada
            if self.datos:
                entrada.insert(0, self.datos.get(clave, ''))

        if not self.datos:
            self.entradas['hora_apertura'].insert(0, '08:00')
            self.entradas['hora_cierre'].insert(0, '20:00')

        tk.Label(marco, text='* Campos obligatorios', bg='lightyellow',
                 fg='#555555', font=('Arial', 10)).grid(row=9, column=0, columnspan=2, pady=8)

        botones = tk.Frame(marco, bg='lightyellow')
        botones.grid(row=10, column=0, columnspan=2, pady=13)
        tk.Button(botones, text='Guardar cambios' if self.datos else 'Crear sede',
                  bg='green', fg='white', font=('Arial', 12, 'bold'),
                  width=17, command=self.guardar).pack(side='left', padx=8)
        tk.Button(botones, text='Cancelar', bg='red', fg='white',
                  font=('Arial', 12, 'bold'), width=12,
                  command=self.cerrar).pack(side='left', padx=8)
        self.entradas['nombre'].focus_set()

    def guardar(self):
        valores = {clave: entrada.get() for clave, entrada in self.entradas.items()}
        try:
            argumentos = (valores['nombre'], valores['direccion'], valores['barrio'],
                          valores['localidad'], valores['telefono'], valores['email'],
                          valores['hora_apertura'], valores['hora_cierre'])
            if self.datos:
                self.controlador_sedes.modificar_sede(self.datos['id_sede'], *argumentos)
                mensaje = 'Sede modificada correctamente.'
            else:
                self.controlador_sedes.insertar_sede(*argumentos)
                mensaje = 'Sede creada correctamente.'
        except ReglaNegocioError as error:
            messagebox.showerror('Error de validación', str(error), parent=self.ventana)
            return
        except Exception as error:
            messagebox.showerror('Error', f'No se pudieron guardar los datos: {error}', parent=self.ventana)
            return
        messagebox.showinfo('Éxito', mensaje, parent=self.ventana)
        self.cerrar()
        self.al_guardar()

    def cerrar(self):
        self.ventana.grab_release()
        self.ventana.destroy()
