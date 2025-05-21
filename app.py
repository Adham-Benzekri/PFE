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
        cleaned_path = "data_nettoye.csv"
        df_cleaned.to_csv(cleaned_path, index=False)

        st.subheader("🧹 Aperçu des données nettoyées")
        st.dataframe(df_cleaned.head())

        # Analyse
        st.subheader("📊 Résultats de l'analyse")
        summary = analyze_downtime_impact(cleaned_path)

        if summary is not None:
            st.dataframe(summary)

            csv = summary.to_csv(index=False).encode('utf-8')
            result_filename = 'resultat_analyse.csv'

            st.download_button(
                label="📤 Télécharger les résultats pour Power BI",
                data=csv,
                file_name=result_filename,
                mime='text/csv'
            )

            if st.button("📋 Copier le chemin du fichier résultat"):
                abs_path = os.path.abspath(result_filename)
                st.markdown(f"Chemin absolu du fichier résultat : `{abs_path}`")

                st.markdown(
                    f"""
                    <script>
                    navigator.clipboard.writeText("{abs_path}").then(function() {{
                        alert('Chemin du fichier copié dans le presse-papier !');
                    }}, function(err) {{
                        alert('Échec de la copie : ' + err);
                    }});
                    </script>
                    """,
                    unsafe_allow_html=True
                )

            # Téléchargement du modèle Power BI
            if os.path.exists("powerbitamplate.pbit"):
                with open("powerbitamplate.pbit", "rb") as f:
                    st.download_button(
                        label="📥 Télécharger le modèle Power BI",
                        data=f,
                        file_name="powerbitamplate.pbit",
                        mime="application/octet-stream"
                    )
            else:
                st.warning("Modèle Power BI introuvable dans le répertoire de l'application.")

        else:
            st.warning("Aucun résultat à afficher.")

    except Exception as e:
        st.error(f"❌ Une erreur est survenue lors du traitement du fichier : {e}")
