import streamlit as st
from chatbot.product_lookup import ProductLookup
from chatbot.quotation_engine import QuotationEngine
from chatbot.user_data_collector import UserDataCollector

# Inicialización de componentes
product_db = ProductLookup()
quotation_engine = QuotationEngine()
user_collector = UserDataCollector()

st.set_page_config(page_title="Cotizador Conversacional", layout="centered")
st.title("🧑‍💼 Chatbot - Álvaro Medina")

# Inicialización del estado
if "step" not in st.session_state:
    st.session_state.step = "inicio"
    st.session_state.tipo_licencia = None
    st.session_state.producto = None
    st.session_state.cantidad = None
    st.session_state.nombre = None
    st.session_state.correo = None
    st.session_state.telefono = None

# Manejador de pasos
def responder_usuario(mensaje_usuario):
    if st.session_state.step == "inicio":
        st.session_state.step = "licencia"
        return "¡Hola! Soy Álvaro Medina, tu asesor de confianza. 😊\n\n¿En qué tipo de licencia estás interesado? (Educativa, Comercial, Gobierno)"

    elif st.session_state.step == "licencia":
        tipo = mensaje_usuario.strip().lower()
        if tipo not in ["educativa", "comercial", "gobierno"]:
            return "🙋‍♂️ Por favor, indícame una opción válida: Educativa, Comercial o Gobierno."
        st.session_state.tipo_licencia = tipo
        st.session_state.step = "producto"
        productos = product_db.list_products_by_license(tipo)
        st.session_state.productos_disponibles = productos
        lista = "\n".join(f"- {p}" for p in productos)
        return f"¡Perfecto! 😊 Estos son los productos disponibles para licencias *{tipo.capitalize()}*:\n\n{lista}\n\nEscríbeme cuál te interesa."

    elif st.session_state.step == "producto":
        producto = mensaje_usuario.strip().lower()
        if producto not in [p.lower() for p in st.session_state.productos_disponibles]:
            return "🛑 Ese producto no está en la lista. Por favor, copia y pega el nombre tal cual aparece."
        st.session_state.producto = producto
        st.session_state.step = "cantidad"
        return f"👌 Excelente elección. ¿Cuántas licencias de '{producto}' te interesan?"

    elif st.session_state.step == "cantidad":
        try:
            cantidad = int(mensaje_usuario)
            if cantidad <= 0:
                raise ValueError
            st.session_state.cantidad = cantidad
            st.session_state.step = "contacto"
            precio = product_db.get_product_price(st.session_state.producto, st.session_state.tipo_licencia)
            total = precio * cantidad
            st.session_state.total = total
            return (
                f"💰 El precio por licencia es de **${precio:.2f} USD**.\n"
                f"🧾 *Total sin IVA*: **${total:.2f} USD**.\n\n"
                "Para continuar, ¿podrías decirme tu **nombre completo**?"
            )
        except ValueError:
            return "😅 Ups... Necesito que me indiques un número entero válido mayor a 0."

    elif st.session_state.step == "contacto":
        st.session_state.nombre = mensaje_usuario.strip()
        st.session_state.step = "correo"
        return f"Gracias, {st.session_state.nombre}. Ahora, ¿podrías compartirme tu **correo electrónico** para enviarte la cotización?"

    elif st.session_state.step == "correo":
        correo = mensaje_usuario.strip()
        if "@" not in correo or "." not in correo.split("@")[-1]:
            return "📧 El formato del correo no parece válido. Intenta nuevamente, por favor."
        st.session_state.correo = correo
        st.session_state.step = "telefono"
        return "¡Listo! Si gustas, también puedes proporcionarme tu **número de teléfono** para seguimiento (opcional)."

    elif st.session_state.step == "telefono":
        st.session_state.telefono = mensaje_usuario.strip()
        user_collector.save_user_data(
            st.session_state.nombre,
            st.session_state.correo,
            st.session_state.telefono,
            f"{st.session_state.producto} - {st.session_state.tipo_licencia}",
            st.session_state.cantidad
        )
        st.session_state.step = "final"
        nombre = st.session_state.nombre
        return (
            f"✅ ¡Perfecto, {nombre}!\n\n"
            "Tu solicitud ha sido registrada con éxito. 📌\n\n"
            "📬 Muy pronto, uno de nuestros ejecutivos te contactará para enviarte la cotización final y resolver cualquier duda.\n\n"
            "Si deseas cotizar otro producto, solo escribe: **reiniciar** 🔄"
        )

    elif st.session_state.step == "final":
        if mensaje_usuario.strip().lower() == "reiniciar":
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
        else:
            return "¿Deseas iniciar una nueva cotización? Solo escribe: **reiniciar** 🔁"

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escríbele a Álvaro Medina..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = responder_usuario(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

