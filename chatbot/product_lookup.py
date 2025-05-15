import pandas as pd
from pathlib import Path

class ProductLookup:
    def __init__(self):
        # Mapear tipo de licencia a su archivo correspondiente
        self.files = {
            "educativa": Path("data/Lista Academico.xlsx"),
            "comercial": Path("data/Lista Comercial.xlsx"),
            "gobierno": Path("data/Lista Gobierno.xlsx")
        }

    def _load_dataframe(self, tipo_licencia: str) -> pd.DataFrame:
        tipo = tipo_licencia.strip().lower()
        if tipo not in self.files:
            raise ValueError(f"Tipo de licencia no válido: {tipo_licencia}")

        file_path = self.files[tipo]
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df.rename(columns={"producto": "producto", "precio unitario (usd)": "precio"}, inplace=True)
        df["producto"] = df["producto"].astype(str).str.strip().str.lower()
        df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
        df = df.dropna(subset=["producto", "precio"])
        return df

    def list_products_by_license(self, tipo_licencia: str) -> list:
        df = self._load_dataframe(tipo_licencia)
        return sorted(df["producto"].unique().tolist())

    def get_product_price(self, product_name: str, tipo_licencia: str) -> float:
        df = self._load_dataframe(tipo_licencia)
        product_name = product_name.strip().lower()
        match = df[df["producto"] == product_name]

        if match.empty:
            return None

        # Tomamos el primer precio válido si hay varios rangos
        return match.iloc[0]["precio"]
