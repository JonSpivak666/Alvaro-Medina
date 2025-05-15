import streamlit as st
from chatbot.product_lookup import ProductLookup
from chatbot.quotation_engine import QuotationEngine
from chatbot.user_data_collector import UserDataCollector

# Inicialización
product_db = ProductLookup()
quotation_engine = QuotationEngine()
user_collector = UserDataCollector()

st.set_page_config(page_title="Chatbot Cotizador", layout="centered")
st.title("🤖 Cotizador Automatizado")

# 1. Selección de tipo de licencia
tipo_licencia = st.selectbox("¿Qué tipo de licencia te interesa?", ["Educativa", "Comercial", "Gobierno"])

# 2. Cargar productos disponibles según licencia
productos = product_db.list_products_by_license(tipo_licencia)
producto_seleccionado = st.selectbox("Selecciona un producto disponible:", productos)

# 3. Obtener precio
precio_unitario = product_db.get_product_price(producto_seleccionado, tipo_licencia)

if precio_unitario is None:
    st.error("Este producto no tiene un precio válido. Un ejecutivo te contactará.")
else:
    st.markdown(f"**Precio unitario:** ${precio_unitario:.2f} USD por licencia")

    # 4. Ingreso de cantidad
    cantidad = st.number_input("¿Cuántas licencias necesitas?", min_value=1, step=1)

    if cantidad:
        cotizacion = quotation_engine.generar_precotizacion(precio_unitario, cantidad)

        st.subheader("📄 Pre-Cotización (sin IVA)")
        st.write(f"Subtotal: ${cotizacion['subtotal']:.2f} USD")
        st.write(f"Total: ${cotizacion['total']:.2f} USD")

        # 5. Captura de datos del cliente
        st.markdown("---")
        st.subheader("📇 Datos de Contacto")
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo electrónico")
        telefono = st.text_input("Teléfono (opcional)")

        if st.button("Enviar cotización"):
            if not nombre or not correo:
                st.warning("Por favor, proporciona tu nombre y correo.")
            else:
                try:
                    user_collector.save_user_data(
                        nombre, correo, telefono,
                        f"{producto_seleccionado} - {tipo_licencia}", cantidad
                    )
                    st.success("Gracias, hemos guardado tu información. Un ejecutivo te contactará pronto.")
                except ValueError as e:
                    st.error(f"Error: {str(e)}")




