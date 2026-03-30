import streamlit as st
from NFC.read_nfc import write_text

st.set_page_config(layout="wide")
st.title("NFC Schrijfpagina")

st.write("Gebruik deze pagina om een 'Complex Code' naar een NFC tag te schrijven.")

# Input field
value_to_write = st.text_input("Voer de code in die je naar de tag wil schrijven", "")

# Button
if st.button("Schrijf naar NFC tag"):
    if not value_to_write:
        st.warning("Voer eerst een waarde in.")
    else:
        try:
            write_text(value_to_write)
            st.success(f"Succesvol geschreven naar NFC tag: {value_to_write}")
            st.session_state.last_written = value_to_write
        except Exception as e:
            st.error(f"Fout bij schrijven: {e}")

# Show last written value
if "last_written" in st.session_state:
    st.info(f"Laatst geschreven waarde: {st.session_state.last_written}")
