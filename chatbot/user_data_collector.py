import csv
from pathlib import Path

class UserDataCollector:
    def __init__(self, storage_path: str = "database/clientes.csv"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            with open(self.storage_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["nombre", "correo", "telefono", "producto", "cantidad"])
                writer.writeheader()

    def save_user_data(self, nombre: str, correo: str, telefono: str, producto: str, cantidad: int) -> None:
        if not self._is_valid_email(correo):
            raise ValueError("Correo electrónico inválido.")
        if self._email_exists(correo):
            print(f"El correo {correo} ya está registrado. No se guardará duplicado.")
            return
        with open(self.storage_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "correo", "telefono", "producto", "cantidad"])
            writer.writerow({
                "nombre": nombre.strip(),
                "correo": correo.strip().lower(),
                "telefono": telefono.strip(),
                "producto": producto.strip(),
                "cantidad": cantidad
            })

    def _email_exists(self, correo: str) -> bool:
        correo = correo.strip().lower()
        if not self.storage_path.exists():
            return False
        with open(self.storage_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return any(row["correo"].strip().lower() == correo for row in reader)

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]
