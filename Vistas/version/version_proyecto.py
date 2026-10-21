# python --version
# python -m venv .venv
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1
# python -m pip install --upgrade "flet[all]"
# flet doctor

import flet as ft

class SaludoApp:
    
    def __init__(self):       
         
        self.saludo_sistema = ft.Text("Muchas gracias por utilizar nuestro sistema", size=50, data=0)
        self.grupo = ft.Text("Nuestro grupo estuvo compuesto por:", size=20, data=0)
        self.integrante_1 = ft.Text("* Dario Lopez", size=15, data=0)
        self.integrante_2 = ft.Text("* Federico Wedemeyer", size=15, data=0)
        self.integrante_3 = ft.Text("* Rosario Evelyn Mendoza", size=15, data=0)
        self.integrante_4 = ft.Text("* Sergio Gabriel Garzon", size=15, data=0)
        self.integrante_5 = ft.Text("* Tomas Reyna Mariano", size=15, data=0)
        self.datos_profesores = ft.Text("\nProfesores de la materia:", size=20, data=0)
        self.profe_1 = ft.Text("* Martín Gustavo Casatti", size=15, data=0)
        self.profe_2 = ft.Text("* Fernando Mario Sanabria", size=15, data=0)
        
        # Esta forma de hacer el boton la extrajimos de la documentacion de flet
        # Link: https://flet.dev/docs/controls/button/        
        self.button_salir =  ft.Button(
                        content="Salir del Sistema",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.HOVERED: ft.Colors.ORANGE_400,
                                ft.ControlState.FOCUSED: ft.Colors.BLUE_400,
                                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                            },
                            bgcolor={
                                ft.ControlState.FOCUSED: ft.Colors.PINK_200,
                                ft.ControlState.DEFAULT: ft.Colors.RED_600,
                            },
                            padding={ft.ControlState.HOVERED: 20},
                            overlay_color=ft.Colors.TRANSPARENT,
                            elevation={
                                ft.ControlState.DEFAULT: 0,
                                ft.ControlState.HOVERED: 5,
                                ft.ControlState.PRESSED: 10,
                            },
                            animation_duration=500,
                            side={
                                ft.ControlState.DEFAULT: ft.BorderSide(
                                    1, color=ft.Colors.BLUE_100
                                ),
                                ft.ControlState.HOVERED: ft.BorderSide(
                                    3, color=ft.Colors.BLUE_400
                                ),
                                ft.ControlState.PRESSED: ft.BorderSide(
                                    6, color=ft.Colors.BLUE_600
                                ),
                            },
                            shape={
                                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(
                                    radius=20
                                ),
                                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                    radius=2
                                ),
                            },
                        ), )
    
    
    def build(self):
        return ft.Column(controls=[
            self.saludo_sistema,
            self.grupo,
            self.integrante_1,
            self.integrante_2,
            self.integrante_3,
            self.integrante_4,
            self.integrante_5,
            self.datos_profesores,
            self.profe_1,
            self.profe_2,  
            self.button_salir         
        ], spacing=12, scroll=ft.ScrollMode.AUTO)
    
    def salir_programa(self):        
        pass
        
    
def main(page: ft.Page):
    app = SaludoApp()
    page.title = "Informacion: Ventana de fin"
    page.window.width = 1200
    page.window.height = 650    
    page.add(app.build())
    
    
if __name__ == "__main__":
    ft.run(main)
    
