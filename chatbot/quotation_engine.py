class QuotationEngine:
    def __init__(self):
        pass  # No se necesita configuración adicional al no usar IVA

    def generar_precotizacion(self, precio_unitario: float, cantidad: int) -> dict:
        # Validaciones
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")
        if precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo.")

        # Cálculo sin IVA
        subtotal = precio_unitario * cantidad
        total = subtotal

        # Resultado estructurado
        return {
            "precio_unitario": round(precio_unitario, 2),
            "cantidad": cantidad,
            "subtotal": round(subtotal, 2),
            "iva": 0.0,  # Por si en el futuro se requiere mostrarlo igual en la interfaz
            "total": round(total, 2),
        }

