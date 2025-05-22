import streamlit as st
import pandas as pd
import os
from data_cleaning import clean_data
from analyze_data import analyze_downtime_impact

st.title("Analyse de l'efficacité de production de sucre")

st.markdown("Chargez un fichier CSV contenant les données de production pour analyser l'impact des arrêts sur l'efficacité.")

uploaded_file = st.file_uploader("📁 Choisissez un fichier CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Nettoyage
        df_cleaned = clean_data(df)

        st.subheader("🧹 Aperçu des données nettoyées")
        st.dataframe(df_cleaned.head())

        # Analyse
        st.subheader("📊 Résultats de l'analyse")
        summary = analyze_downtime_impact(df_cleaned)

        if summary is not None:
            st.dataframe(summary)

            # Télécharger les données nettoyées
            cleaned_csv = df_cleaned.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données nettoyées",
                data=cleaned_csv,
                file_name="data_nettoye.csv",
                mime="text/csv"
            )

            # Télécharger les résultats d'analyse
            analysis_csv = summary.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📤 Télécharger les résultats pour Power BI",
                data=analysis_csv,
                file_name="resultat_analyse.csv",
                mime='text/csv'
            )

        else:
            st.warning("Aucun résultat à afficher.")

        # Téléchargement du modèle Power BI
        if os.path.exists("template.pbit"):
            with open("template.pbit", "rb") as f:
                st.download_button(
                    label="📥 Télécharger le modèle Power BI",
                    data=f,
                    file_name="template.pbit",
                    mime="application/octet-stream"
                )
        else:
            st.warning("Modèle Power BI introuvable dans le répertoire de l'application.")

    except Exception as e:
        st.error(f"❌ Une erreur est survenue lors du traitement du fichier : {e}")
