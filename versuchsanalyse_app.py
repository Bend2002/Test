# versuchsanalyse_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App-Titel
st.set_page_config(page_title="Versuchsanalyse: Gewichtsstatistik", layout="wide")
st.title("🧪 Versuchsdaten eingeben & analysieren")

st.markdown("Gib mindestens 15 Messwerte pro Versuch ein (Abtropfgewicht und Trockengewicht).")

# Session-State: initialisieren
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=["Abtropfgewicht", "Trockengewicht"])

# Eingabeformular
with st.expander("📋 Versuchsdaten manuell eingeben"):
    with st.form("eingabe_formular"):
        cols = st.columns(2)
        abtropf = cols[0].number_input("Abtropfgewicht (g)", min_value=0.0, step=0.01, format="%.2f")
        trocken = cols[1].number_input("Trockengewicht (g)", min_value=0.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("➕ Hinzufügen")
        if submitted:
            new_row = pd.DataFrame([[abtropf, trocken]], columns=["Abtropfgewicht", "Trockengewicht"])
            st.session_state['data'] = pd.concat([st.session_state['data'], new_row], ignore_index=True)

# Tabelle anzeigen
st.subheader("📊 Aktuelle Versuchsdaten")
st.dataframe(st.session_state['data'], use_container_width=True)

data = st.session_state['data']

if len(data) >= 15:
    st.success("✅ Genug Daten für Analyse vorhanden (≥ 15 Messungen)")

    # Statistische Analyse
    st.subheader("📈 Statistische Kennwerte")

    def berechne_stats(df):
        stats = {}
        for col in df.columns:
            arr = df[col].values
            stats[col] = {
                "Mittelwert": np.mean(arr),
                "Median": np.median(arr),
                "Standardabweichung": np.std(arr, ddof=1),
                "Varianz": np.var(arr, ddof=1),
                "Min": np.min(arr),
                "Max": np.max(arr),
                "Spannweite": np.max(arr) - np.min(arr),
                "Index of Dispersion": np.var(arr, ddof=1) / np.mean(arr) if np.mean(arr) != 0 else np.nan
            }
        return stats

    stats = berechne_stats(data)

    # Ausgabe der Statistik
    for gewicht in stats:
        st.markdown(f"**🔹 {gewicht}**")
        for key, value in stats[gewicht].items():
            st.markdown(f"- {key}: `{value:.3f}`")

    # Visualisierungen
    st.subheader("🖼️ Visualisierung")

    # Histogramme
    fig1, ax1 = plt.subplots()
    ax1.hist(data["Abtropfgewicht"], bins=10, alpha=0.7, label="Abtropfgewicht")
    ax1.hist(data["Trockengewicht"], bins=10, alpha=0.7, label="Trockengewicht")
    ax1.set_title("Histogramm der Gewichte")
    ax1.set_xlabel("Gewicht (g)")
    ax1.set_ylabel("Häufigkeit")
    ax1.legend()
    st.pyplot(fig1)

    # Scatterplot
    fig2, ax2 = plt.subplots()
    ax2.scatter(data["Abtropfgewicht"], data["Trockengewicht"], c='blue')
    ax2.set_title("Abtropfgewicht vs. Trockengewicht")
    ax2.set_xlabel("Abtropfgewicht (g)")
    ax2.set_ylabel("Trockengewicht (g)")
    st.pyplot(fig2)

    # Boxplots
    fig3, ax3 = plt.subplots()
    ax3.boxplot([data["Abtropfgewicht"], data["Trockengewicht"]], labels=["Abtropf", "Trocken"])
    ax3.set_title("Boxplot der Gewichte")
    st.pyplot(fig3)

    # Export
    st.subheader("💾 Datenexport")
    export_col1, export_col2 = st.columns(2)
    export_col1.download_button("📥 CSV herunterladen", data=data.to_csv(index=False), file_name="versuchsdaten.csv")
    export_col2.download_button("📥 Excel herunterladen", data=data.to_excel(index=False, engine='openpyxl'), file_name="versuchsdaten.xlsx")

else:
    st.warning("Bitte mindestens 15 Werte eingeben, um Analyse & Visualisierung zu aktivieren.")

