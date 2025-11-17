import shutil
import uuid
from pathlib import Path
from PIL import Image
import customtkinter as ctk
import tkinter.messagebox as messagebox

from model.usuario_model import GestorUsuarios, Usuario
from view.main_view import MainView, AddUserView


class AppController:
    def __init__(self, master):
        self.master = master

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.ASSETS_PATH.mkdir(parents=True, exist_ok=True)

        self.modelo = GestorUsuarios()
        self.view = MainView(master)

        self.avatar_images = {}
        self.view.menu_archivo.add_command(label="Cargar", command=self.cargar_usuarios)
        self.view.menu_archivo.add_command(label="Guardar", command=self.guardar_usuarios)
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(label="Salir", command=self.master.quit)

        self.view.add_user_btn.configure(command=self.abrir_ventana_añadir)

        self.usuarios_csv = self.BASE_DIR / "usuarios.csv"

        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        usuarios = self.modelo.listar()
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice):
        usuario = self.modelo.obtener(indice)
        img = None
        if usuario.avatar:
            ruta_avatar = (self.ASSETS_PATH / usuario.avatar)
            if ruta_avatar.exists():
                img = self._cargar_ctkimage(ruta_avatar, size=(150, 150))
        self.view.mostrar_detalles_usuario(usuario, img)

    def abrir_ventana_añadir(self):
        add_view = AddUserView(self.master)
        add_view.guardar_button.configure(command=lambda: self.añadir_usuario(add_view))

    def añadir_usuario(self, add_view):
        data = add_view.get_data()
        nombre = data.get("nombre", "")
        edad_txt = data.get("edad", "")
        genero = data.get("genero", "")
        avatar_path = data.get("avatar_path", None)

        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        try:
            edad = int(edad_txt)
            if edad < 0:
                raise ValueError("Edad negativa")
        except Exception:
            messagebox.showerror("Error", "Introduce una edad válida (entero).")
            return

        avatar_filename = None
        if avatar_path:
            try:
                ext = Path(avatar_path).suffix
                avatar_filename = f"avatar_{uuid.uuid4().hex}{ext}"
                destino = self.ASSETS_PATH / avatar_filename
                shutil.copy(avatar_path, destino)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar la imagen del avatar: {e}")
                return

        nuevo = Usuario(nombre=nombre, edad=edad, genero=genero, avatar=avatar_filename)
        self.modelo.agregar(nuevo)

        self.refrescar_lista_usuarios()
        add_view.window.destroy()
        messagebox.showinfo("OK", "Usuario añadido correctamente.")

    def guardar_usuarios(self):
        try:
            self.modelo.guardar_csv(self.usuarios_csv)
            messagebox.showinfo("Guardado", f"Usuarios guardados en:\n{self.usuarios_csv}")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def cargar_usuarios(self):
        try:
            self.modelo.cargar_csv(self.usuarios_csv)
            self.avatar_images.clear()
            self.refrescar_lista_usuarios()
            messagebox.showinfo("Cargado", f"Usuarios cargados desde:\n{self.usuarios_csv}")
        except FileNotFoundError:
            print(f"Archivo {self.usuarios_csv} no existe — nada que cargar.")
        except Exception as e:
            messagebox.showerror("Error al cargar CSV", str(e))

    def _cargar_ctkimage(self, ruta: Path, size=(100, 100)):
        key = str(ruta.resolve())
        if key in self.avatar_images:
            return self.avatar_images[key]
        try:
            pil_img = Image.open(ruta)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
            self.avatar_images[key] = ctk_img
            return ctk_img
        except Exception as e:
            print(f"Error cargando imagen {ruta}: {e}")
            return None