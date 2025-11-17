# view/main_view.py
import customtkinter as ctk
import tkinter
from tkinter import filedialog


class MainView:
    def __init__(self, master):
        self.master = master

        # ---- BARRA DE MENÚ ----
        self.menubar = tkinter.Menu(master)
        master.config(menu=self.menubar)
        self.menu_archivo = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        # ---- LAYOUT ----
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=3)

        # Panel izquierdo
        self.lista_frame = ctk.CTkScrollableFrame(master)
        self.lista_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Panel derecho
        self.detalles_frame = ctk.CTkFrame(master)
        self.detalles_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.label_nombre = ctk.CTkLabel(self.detalles_frame, text="Nombre:")
        self.label_nombre.pack(anchor="w", pady=5)

        self.label_edad = ctk.CTkLabel(self.detalles_frame, text="Edad:")
        self.label_edad.pack(anchor="w", pady=5)

        self.label_genero = ctk.CTkLabel(self.detalles_frame, text="Género:")
        self.label_genero.pack(anchor="w", pady=5)

        self.avatar_label = ctk.CTkLabel(self.detalles_frame, text="")
        self.avatar_label.pack(pady=10)

        # Botón Añadir Usuario
        self.boton_añadir = ctk.CTkButton(
            master, text="Añadir Usuario (+)"
        )
        self.boton_añadir.grid(row=1, column=0, columnspan=2, pady=10)


    # -------- LISTA DE USUARIOS --------
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


    # -------- DETALLES --------
    def mostrar_detalles_usuario(self, usuario, avatar_img=None):
        self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.label_edad.configure(text=f"Edad: {usuario.edad}")
        self.label_genero.configure(text=f"Género: {usuario.genero}")

        if avatar_img:
            self.avatar_label.configure(image=avatar_img)
        else:
            self.avatar_label.configure(image="")


# ============================================================
#                 VENTANA MODAL (AddUserView)
# ============================================================

class AddUserView:
    def __init__(self, master):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Usuario")
        self.window.geometry("350x400")
        self.window.grab_set()

        # Nombre
        ctk.CTkLabel(self.window, text="Nombre").pack(pady=5)
        self.nombre_entry = ctk.CTkEntry(self.window)
        self.nombre_entry.pack(pady=5)

        # Edad
        ctk.CTkLabel(self.window, text="Edad").pack(pady=5)
        self.edad_entry = ctk.CTkEntry(self.window)
        self.edad_entry.pack(pady=5)

        # Género
        ctk.CTkLabel(self.window, text="Género").pack(pady=5)
        self.genero_entry = ctk.CTkEntry(self.window)
        self.genero_entry.pack(pady=5)

        # Avatar
        ctk.CTkLabel(self.window, text="Avatar (opcional)").pack(pady=5)
        self.avatar_path = ctk.CTkEntry(self.window, width=220)
        self.avatar_path.pack(pady=5)

        self.boton_avatar = ctk.CTkButton(
            self.window,
            text="Seleccionar Imagen",
            command=self.seleccionar_imagen
        )
        self.boton_avatar.pack(pady=5)

        # Botón guardar
        self.guardar_button = ctk.CTkButton(self.window, text="Guardar")
        self.guardar_button.pack(pady=20)


    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.webp")]
        )
        if ruta:
            self.avatar_path.delete(0, "end")
            self.avatar_path.insert(0, ruta)


    def get_data(self):
        return {
            "nombre": self.nombre_entry.get(),
            "edad": self.edad_entry.get(),
            "genero": self.genero_entry.get(),
            "avatar": self.avatar_path.get()
        }
