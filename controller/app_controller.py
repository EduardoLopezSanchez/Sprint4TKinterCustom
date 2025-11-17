# controller/app_controller.py
from model.usuario_model import GestorUsuarios, Usuario
from view.main_view import MainView, AddUserView
from pathlib import Path
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk


class AppController:

    def __init__(self, master):
        self.master = master

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"

        self.avatar_images = {}

        self.modelo = GestorUsuarios()
        self.view = MainView(master)

        self.view.boton_añadir.configure(
            command=self.abrir_ventana_añadir
        )

        self.refrescar_lista_usuarios()


    def refrescar_lista_usuarios(self):
        usuarios = self.modelo.listar()
        self.view.actualizar_lista_usuarios(
            usuarios, self.seleccionar_usuario
        )


    def seleccionar_usuario(self, indice):
        usuario = self.modelo.obtener(indice)

        avatar_img = None

        if usuario.avatar:
            ruta = Path(usuario.avatar)
            if ruta.exists():
                if usuario.avatar not in self.avatar_images:
                    img = ctk.CTkImage(
                        light_image=Image.open(ruta),
                        dark_image=Image.open(ruta),
                        size=(150, 150)
                    )
                    self.avatar_images[usuario.avatar] = img

                avatar_img = self.avatar_images[usuario.avatar]

        self.view.mostrar_detalles_usuario(usuario, avatar_img)


    def abrir_ventana_añadir(self):
        add_view = AddUserView(self.master)

        add_view.guardar_button.configure(
            command=lambda: self.añadir_usuario(add_view)
        )


    def añadir_usuario(self, add_view):
        datos = add_view.get_data()

        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return

        try:
            edad = int(datos["edad"])
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        user = Usuario(
            nombre=datos["nombre"],
            edad=edad,
            genero=datos["genero"],
            avatar=datos["avatar"] or None
        )

        self.modelo._usuarios.append(user)

        self.refrescar_lista_usuarios()

        add_view.window.destroy()