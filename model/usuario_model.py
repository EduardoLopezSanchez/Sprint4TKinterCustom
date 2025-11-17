import csv
from pathlib import Path


class Usuario:
    def __init__(self, nombre, edad, genero, avatar=None):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar  # ruta relativa (string) o None

    def to_tuple(self):
        return (self.nombre, str(self.edad), self.genero, self.avatar or "")


class GestorUsuarios:
    def __init__(self):
        self._usuarios = []
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self):
        # Datos de ejemplo inicialmente
        self._usuarios.append(Usuario("Ana", 28, "Femenino"))
        self._usuarios.append(Usuario("Luis", 34, "Masculino"))
        self._usuarios.append(Usuario("Marta", 22, "Femenino"))

    def listar(self):
        return self._usuarios

    def obtener(self, indice):
        return self._usuarios[indice]

    def agregar(self, usuario):
        self._usuarios.append(usuario)

    def eliminar(self, indice):
        del self._usuarios[indice]

    def actualizar(self, indice, usuario):
        self._usuarios[indice] = usuario

    def guardar_csv(self, filepath):
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["nombre", "edad", "genero", "avatar"])
            for u in self._usuarios:
                escritor.writerow(u.to_tuple())

    def cargar_csv(self, filepath):
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(str(filepath))
        usuarios_nuevos = []
        with filepath.open("r", encoding="utf-8") as f:
            lector = csv.reader(f)
            try:
                header = next(lector)
            except StopIteration:
                return
            for i, fila in enumerate(lector, start=2):
                try:
                    if len(fila) < 3:
                        continue
                    nombre = fila[0].strip()
                    edad = int(fila[1].strip())
                    genero = fila[2].strip()
                    avatar = fila[3].strip() if len(fila) > 3 else ""
                    avatar = avatar if avatar else None
                    usuarios_nuevos.append(Usuario(nombre, edad, genero, avatar))
                except Exception as e:
                    print(f"Advertencia: fila {i} corrupta en CSV ({e}). Se omite.")
                    continue
        self._usuarios.clear()
        self._usuarios.extend(usuarios_nuevos)
