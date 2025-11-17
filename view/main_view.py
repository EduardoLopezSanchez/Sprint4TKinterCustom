# view/main_view.py
import customtkinter as ctk
import tkinter
from tkinter import filedialog


class MainView:
    def __init__(self, master):
        self.master = master

        self.menubar = tkinter.Menu(master)
        master.config(menu=self.menubar)
        self.menu_archivo = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=3)

        self.lista_frame = ctk.CTkScrollableFrame(master)
        self.lista_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.add_user_btn = ctk.CTkButton(master, text="+ Añadir usuario")
        self.add_user_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.detalles_frame = ctk.CTkFrame(master)
        self.detalles_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.label_nombre = ctk.CTkLabel(self.detalles_frame, text="Nombre: ")
        self.label_nombre.pack(anchor="w", pady=5)

        self.label_edad = ctk.CTkLabel(self.detalles_frame, text="Edad: ")
        self.label_edad.pack(anchor="w", pady=5)

        self.label_genero = ctk.CTkLabel(self.detalles_frame, text="Género: ")
        self.label_genero.pack(anchor="w", pady=5)

        self.avatar_label = ctk.CTkLabel(self.detalles_frame, text="")
        self.avatar_label.pack(anchor="center", pady=10)

    def actualizar_lista_usuarios(self, usuarios, on_seleccionar_callback):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        for i, usuario in enumerate(usuarios):
            boton = ctk.CTkButton(
                self.lista_frame,
                text=usuario.nombre,
                command=lambda idx=i: on_seleccionar_callback(idx)
            )
            boton.pack(fill="x", padx=5, pady=4)

    def mostrar_detalles_usuario(self, usuario, ctkimage=None):
        self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.label_edad.configure(text=f"Edad: {usuario.edad}")
        self.label_genero.configure(text=f"Género: {usuario.genero}")
        if ctkimage:
            self.avatar_label.configure(image=ctkimage, text="")
        else:
            self.avatar_label.configure(image="", text="(sin avatar)")

class AddUserView:
    def __init__(self, master):
        # crea ventana modal
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Nuevo Usuario")
        self.window.geometry("350x350")
        self.window.grab_set()

        self.avatar_path = None

        ctk.CTkLabel(self.window, text="Nombre:").pack(anchor="w", padx=10, pady=(10, 0))
        self.nombre_entry = ctk.CTkEntry(self.window)
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.window, text="Edad:").pack(anchor="w", padx=10, pady=(10, 0))
        self.edad_entry = ctk.CTkEntry(self.window)
        self.edad_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.window, text="Género:").pack(anchor="w", padx=10, pady=(10, 0))
        self.genero_option = ctk.CTkOptionMenu(self.window, values=["Femenino", "Masculino", "Otro"])
        self.genero_option.set("Femenino")
        self.genero_option.pack(fill="x", padx=10, pady=5)

        self.avatar_label = ctk.CTkLabel(self.window, text="(sin avatar seleccionado)")
        self.avatar_label.pack(pady=(10, 5))

        self.seleccionar_avatar_btn = ctk.CTkButton(self.window, text="Seleccionar avatar...", command=self._seleccionar_avatar)
        self.seleccionar_avatar_btn.pack(padx=10, pady=5)

        self.guardar_button = ctk.CTkButton(self.window, text="Guardar")
        self.guardar_button.pack(side="left", padx=(30,10), pady=15)

        self.cancelar_button = ctk.CTkButton(self.window, text="Cancelar", command=self.window.destroy)
        self.cancelar_button.pack(side="right", padx=(10,30), pady=15)

    def _seleccionar_avatar(self):
        filepath = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"), ("Todos los archivos", "*.*")]
        )
        if filepath:
            self.avatar_path = filepath
            self.avatar_label.configure(text=f"Avatar: {filepath.split('/')[-1]}")

    def get_data(self):
        return {
            "nombre": self.nombre_entry.get().strip(),
            "edad": self.edad_entry.get().strip(),
            "genero": self.genero_option.get(),
            "avatar_path": self.avatar_path  # puede ser None
        }
