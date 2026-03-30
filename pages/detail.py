import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from stl import mesh
import numpy as np
from NFC.read_nfc import read_text

if "nfc_selected" not in st.session_state:
    st.session_state.nfc_selected = None


st.subheader("Selecteer via NFC")

if st.button("Lees NFC tag"):
    try:
        tag_value = read_text()
        if tag_value:
            st.session_state.nfc_selected = tag_value
            st.success(f"NFC tag gelezen: {tag_value}")
        else:
            st.warning("Geen geldige NFC data gevonden.")
    except Exception as e:
        st.error(f"Fout bij lezen NFC: {e}")


st.set_page_config(layout="wide")

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

st.html("""
<iframe  style="width:100%;max-width:800px;height:600px;border:none;"
src="https://www.webcreative.me/3d/view/p.php?m=soft_armchair&rot=1&g=grd_blue">
</iframe>
""")

# def load_clean_stl(path):
#     # Load STL
#     m = mesh.Mesh.from_file(path)

#     # Combine all vertices
#     vertices = np.vstack((m.v0, m.v1, m.v2))

#     # Remove duplicate vertices
#     unique_vertices, index = np.unique(vertices, axis=0, return_inverse=True)

#     # Rebuild triangle indices
#     i = index[:len(index)//3]
#     j = index[len(index)//3:2*len(index)//3]
#     k = index[2*len(index)//3:]

#     # Center the model
#     center = unique_vertices.mean(axis=0)
#     unique_vertices -= center

#     # Normalize scale
#     scale = np.max(np.abs(unique_vertices))
#     unique_vertices /= scale

#     return unique_vertices, i, j, k


# # Load + clean STL
# vertices, i, j, k = load_clean_stl("bridge.stl")

# # Build Plotly figure
# fig = go.Figure(
#     data=[
#         go.Mesh3d(
#             x=vertices[:, 0],
#             y=vertices[:, 1],
#             z=vertices[:, 2],
#             i=i, j=j, k=k,
#             color="lightblue",
#             opacity=0.9,
#             flatshading=False,  # smoother shading
#             lighting=dict(
#                 ambient=0.5,
#                 diffuse=0.8,
#                 specular=0.5,
#                 roughness=0.3,
#                 fresnel=0.2
#             ),
#             lightposition=dict(
#                 x=100,
#                 y=200,
#                 z=0
#             )
#         )
#     ]
# )

# fig.update_layout(
#     scene=dict(
#         xaxis=dict(visible=False),
#         yaxis=dict(visible=False),
#         zaxis=dict(visible=False),
#     ),
#     height=500,
#     margin=dict(l=0, r=0, t=0, b=0)
# )

# st.plotly_chart(fig, use_container_width=True)

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