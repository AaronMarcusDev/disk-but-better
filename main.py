import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from NFC.read_nfc import write_text, read_text # Local module, see NFC/read_nfc.py

use_real_data = False # Change this to false in order to demo!

st.set_page_config(layout="wide")

st.title("DISK - Kunstwerken Dashboard (Prototype)")

# Make some dummy data
np.random.seed(42)

n = 30

if (use_real_data):
    # Load dataframe from Excel
    df = pd.read_excel(
        './data/dataframe.xlsx',
        skiprows=1, # Skip the "Vertrouwelijkheid: RWS Informatie" Row
        usecols=
            [
                "Complex_Code", 
                "Complex_Naam", 
                "Complex_Omschrijving", 
                "KW_Soort", 
                "Ecologie Passeerbaarheid", 
                "Provincie 1", 
                "Gemeente 1",
            ]
            ).head(1000)

else:
    df = pd.DataFrame({
        "Complex_Code": [f"KUNST-{i:03}" for i in range(n)],
        "Complex_Naam": "DEMO MODE",
        "Bouwjaar": np.random.randint(1950, 2020, n),
        "Risico": np.random.choice(["Laag", "Middel", "Hoog"], n, p=[0.4, 0.4, 0.2]),
        "Inspectie": np.random.choice(["NI", "PI", "OK"], n),
        "Onderhoudskosten (€)": np.random.randint(10000, 200000, n),
        "Vervangingskosten (€)": np.random.randint(300000, 2000000, n),
        "Monument": np.random.choice(["Ja", "Nee"], n, p=[0.2, 0.8])
    })
    
    # ^
    # Random component presence (for demo mode)
    df["Has_Pump"] = np.random.choice([True, False], n)
    df["Has_Motor"] = np.random.choice([True, False], n)
    df["Has_Road"] = np.random.choice([True, False], n)
    #Pandas dataframe I filled temporarily with some random data
    #  ^-- love this stuff


# --- minimal additions to make dashboard work ---
n = len(df)
df["DISK_ID"] = df["Complex_Code"]
df["Risico"] = np.random.choice(["Laag", "Middel", "Hoog"], n, p=[0.4, 0.4, 0.2])
df["Inspectie"] = np.random.choice(["NI", "PI", "OK"], n)
df["Onderhoudskosten (€)"] = np.random.randint(10000, 200000, n)
df["Vervangingskosten (€)"] = np.random.randint(300000, 2000000, n)

print("[INFO] DataFrame loaded successfully!")
print("-"*90)
print(df.head())  # Display first few rows
print("-"*90)

# Sidebar filter options
st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect(
    "Risiconiveau", # Risk level
    df["Risico"].unique(),
    default=df["Risico"].unique()
)

inspection_filter = st.sidebar.multiselect(
    "Inspectiestatus", # Inspection status
    df["Inspectie"].unique(),
    default=df["Inspectie"].unique()
)

filtered = df[
    df["Risico"].isin(risk_filter)
    & df["Inspectie"].isin(inspection_filter)
]

# KPI (Key Performance Indicator)
col1, col2, col3 = st.columns(3)

col1.metric("Aantal kunstwerken", len(filtered))
col2.metric(
    "Hoog risico",
    len(filtered[filtered["Risico"] == "Hoog"])
)
col3.metric(
    "Geen inspectie (NI)",
    len(filtered[filtered["Inspectie"] == "NI"])
)

st.divider()

# Table view of the 'artworks'
st.subheader("Overzicht kunstwerken") # MAIN PART!!

def highlight_risk(row):
    if row.Risico == "Hoog":
        return ["background-color: #f52c11"] * len(row)
    if row.Risico == "Middel":
        return ["background-color: #f58e11"] * len(row)
    return [""] * len(row)

st.dataframe(filtered.style.apply(highlight_risk, axis=1), use_container_width=True)

st.divider()

st.info("""**NI** = Zero inspection done before,

 **PI** = Programmed Inspection (planned),
 
  **BO** = Beheer Object""")

# Visualisation of costs
st.subheader("Beslisvisualisatie: onderhoud vs vervanging")

selected = st.selectbox(
    "Selecteer kunstwerk",
    filtered["DISK_ID"]
)

asset = filtered[filtered["DISK_ID"] == selected].iloc[0]

cost_df = pd.DataFrame({
    "Type": ["Onderhoud", "Vervanging"],
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
    color="Type"
)

st.plotly_chart(fig, use_container_width=True)

# Risks
st.subheader("Risicoverdeling")

risk_fig = px.pie(
    filtered,
    names="Risico",
    title="Verdeling risiconiveaus",
    color="Risico",
    color_discrete_map={
        "Laag": "#2596be",     # Blue
        "Middel": "#f58e12",   # Orange
        "Hoog": "#f52c11"      # Red
    }
)


st.plotly_chart(risk_fig, use_container_width=True)

if (not use_real_data):
    st.info("Prototype — geen echte DISK data")
    
try:
    st.info(read_text()) # NFC!
except:
    print("-"*20)
    print("[ERROR] Could not read NFC tag!!")
    print("-"*20)

# For passing data to other pages
st.session_state["df"] = df