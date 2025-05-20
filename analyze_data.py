import pandas as pd
import random

def analyze_downtime_impact(data_path):
    df = pd.read_csv('data_nettoye.csv')

    mois = [
        'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
        'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'
    ]
    df['Mois'] = [random.choice(mois) for _ in range(len(df))]

    df = df[df['Cause_arret'].str.lower() != 'inconnu']

    overall_avg = df['Efficacite'].mean()

    avg_per_group = df.groupby(['Mois', 'Cause_arret'])['Efficacite'].mean()

    impact = overall_avg - avg_per_group

    summary = pd.DataFrame({
        'Efficacite_moyenne (%)': (avg_per_group * 100).round(2),
        'Impact_sur_efficacite (%)': (impact * 100).round(2)
    }).reset_index()

    summary = summary.sort_values(by=['Mois', 'Impact_sur_efficacite (%)'], ascending=[True, False])

    summary.to_csv('impact_cause_arret.csv', index=True)

    print("Impact de chaque cause d'arret sur l'efficacité de production (en pourcentage):")
    print(summary)

    return summary  


if __name__ == "__main__":
    cleaned_data_path = 'data nettoye.csv'  
    analyze_downtime_impact(cleaned_data_path)

