# data_cleaning.py

import pandas as pd

def clean_data(df):
    """
    Nettoyage des données : 
    - mise en minuscules, suppression des doublons,
    - correction des fautes dans colonnes catégorielles,
    - conversion colonnes numériques,
    - gestion des valeurs manquantes,
    - réinitialisation de l'index.
    
    Paramètre:
    df : pandas.DataFrame
        Le DataFrame brut à nettoyer.
        
    Retour:
    pandas.DataFrame
        Le DataFrame nettoyé.
    """

    # Mettre toutes les valeurs de la colonne "Cause_arret" en minuscules
    df['Cause_arret'] = df['Cause_arret'].str.lower()

    # Vérifier et supprimer les doublons
    df = df.drop_duplicates()

    # Nettoyer les espaces et harmoniser la casse dans les colonnes catégorielles
    df['Cause_arret'] = df['Cause_arret'].str.strip().str.lower()
    df['Quart_de_travail'] = df['Quart_de_travail'].str.strip().str.lower()

    # Correction manuelle des fautes courantes ou incohérences
    df['Cause_arret'] = df['Cause_arret'].replace({
        'maintenence': 'maintenance',
        'panne equipement': 'panne equipement',
        'panne electrique': 'panne electrique',
        'retard matiere premiere': 'retard matiere premiere',
        'aucun': 'aucun'
    })

    df['Quart_de_travail'] = df['Quart_de_travail'].replace({
        'matin': 'matin',
        'apres-midi': 'apres-midi',
        'apres midi': 'apres-midi'
    })

    colonnes_numeriques = [
        'Quantite_betteraves_tonnes', 'Teneur_sucre_pct', 'Teneur_eau_pct',
        'Impuretes_pct', 'Debit_tonnes_par_heure', 'Temperature_ebullition_C',
        'Niveau_pH', 'Nombre_ouvriers', 'Duree_arret_minutes',
        'Quantite_sucre_produit_tonnes', 'Efficacite', 'Consommation_energie_kWh',
        'Utilisation_produits_chimiques_kg', 'Pourcentage_sucre_rejete',
        'Temperature_C', 'Humidite_pct'
    ]

    # Conversion des colonnes numériques en nombres
    for col in colonnes_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Gestion des valeurs manquantes
    for col in colonnes_numeriques:
        if col in df.columns:
            median = df[col].median()
            df[col] = df[col].fillna(median)

    for col_cat in ['Cause_arret', 'Quart_de_travail']:
        if col_cat in df.columns:
            df[col_cat] = df[col_cat].fillna('inconnu')

    # Réinitialisation de l’index
    df = df.reset_index(drop=True)

    return df
