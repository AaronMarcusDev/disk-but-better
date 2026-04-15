from time import sleep

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from stl import mesh
import numpy as np
from streamlit_stl import stl_from_file
import requests
# Custom Libraries (local)
from NFC.read_nfc import read_text

# st.set_page_config(layout="wide")

# For the ESP connection
def send_code(code):
    response = requests.get(f"http://192.168.4.1/code?code={code}")
    print(response.text)

if "nfc_selected" not in st.session_state:
    st.session_state.nfc_selected = None

st.subheader("Selecteer via NFC")

if st.button("Lees NFC tag"):
    try:
        tag_value = read_text()
        if tag_value:
            st.session_state.nfc_selected = tag_value
            st.success(f"NFC tag gelezen: {tag_value}")
            
            sleep(1)
            try: 
                send_code(tag_value)
                print("Sent the code: " + tag_value)
            except:
                st.error("Problem with the connection to the Physical System, try again in a few seconds.")
        else:
            st.warning("Geen geldige NFC data gevonden.")
    except Exception as e:
        st.error(f"Fout bij lezen NFC: {e}")


st.title("Detailpagina Kunstwerk")

# Load the dataframe from session_state (set in main.py)
df = st.session_state.get("df", None)
use_real_data = st.session_state.get("use_real_data", False)

if df is None:
    st.error("Geen data beschikbaar. Open eerst de hoofdpagina.")
    st.stop()

# Select artwork
manual_selection = st.selectbox(
    "Selecteer kunstwerk handmatig",
    df["DISK_ID"].unique(),
    key="manual_select"
)

# NFC overrides manual selection
selected = st.session_state.nfc_selected or manual_selection


st.info("This will be replaced by the NFC reader")

asset = df[df["DISK_ID"] == selected].iloc[0]


st.subheader("3D Voorbeeld")
st.set_page_config(layout="wide")
stl_from_file(file_path="stl/intersec.stl", color="#ff2b2b", key="test")

# --- Layout ---
col1, col2 = st.columns([1, 2])

# LEFT COLUMN: Metadata
with col1:
    basis_df = pd.DataFrame({
    "Eigenschap": ["DISK ID", "Naam", "Bouwjaar", "Risico", "Inspectiestatus", "Monument"],
    "Waarde": [
        str(asset["DISK_ID"]),
        str(asset.get("Naam", "—")),
        str(asset.get("Bouwjaar", "—")),
        str(asset["Risico"]),
        str(asset["Inspectie"]),
        str(asset.get("Monument", "—"))
    ]
})

    st.subheader("Basisinformatie")
    st.table(basis_df)
    
    st.info("""**NI** = Zero inspection done before,
 **PI** = Programmed Inspection (planned),
  **BO** = Beheer Object""")


    kosten_df = pd.DataFrame({
        "Type": ["Onderhoudskosten", "Vervangingskosten"],
        "Bedrag (€)": [
            asset["Onderhoudskosten (€)"],
            asset["Vervangingskosten (€)"]
            ]
        })

    st.subheader("Kosten")
    st.table(kosten_df)
    
if not use_real_data:
    
    st.subheader("Componenten")

    components_df = pd.DataFrame({
        "Component": ["Waterpomp", "Motor", "Wegdek"],
        "Aanwezig": [
            "Ja" if asset["Has_Pump"] else "Nee",
            "Ja" if asset["Has_Motor"] else "Nee",
            "Ja" if asset["Has_Road"] else "Nee"
        ]
    })

    st.table(components_df)


# RIGHT COLUMN: Visualizations
with col2:
    st.subheader("Kosten van Onderhoud vs Vervanging")

    cost_df = pd.DataFrame({
        "Type": ["Onderhoud (€)", "Vervanging (€)"],
        "Kosten": [
            asset["Onderhoudskosten (€)"],
            asset["Vervangingskosten (€)"]
        ]
    })

    fig = px.bar(
        cost_df,
        x="Type",
        y="Kosten",
        text="Kosten",
        color="Type",
        color_discrete_map={
            "Onderhoud": "#2596be",
            "Vervanging": "#f52c11"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

st.info("Prototype — geen echte DISK data")