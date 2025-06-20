import pandas as pd

def clean_data(df):
    df['Cause_arret'] = df['Cause_arret'].str.lower()
    df = df.drop_duplicates()

    df['Cause_arret'] = df['Cause_arret'].str.strip().str.lower()
    df['Quart_de_travail'] = df['Quart_de_travail'].str.strip().str.lower()

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

    for col in colonnes_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in colonnes_numeriques:
        if col in df.columns:
            median = df[col].median()
            df[col] = df[col].fillna(median)

    for col_cat in ['Cause_arret', 'Quart_de_travail']:
        if col_cat in df.columns:
            df[col_cat] = df[col_cat].fillna('inconnu')

    if 'mois' in df.columns:
        mois_order = [
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
        mois_order_desc = mois_order[::-1] 
        df['mois'] = df['mois'].str.strip().str.lower()
        df['mois'] = pd.Categorical(df['mois'], categories=mois_order_desc, ordered=True)
        df = df.sort_values('mois', ascending=True)

    df = df.reset_index(drop=True)
    return df
