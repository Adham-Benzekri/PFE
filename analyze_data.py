import pandas as pd
import random

def analyze_downtime_impact(data_path):
    # Load cleaned data
    df = pd.read_csv('data_nettoye.csv')

    # Add 'Mois' column with random months (no accents)
    mois = [
        'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
        'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'
    ]
    df['Mois'] = [random.choice(mois) for _ in range(len(df))]

    # Exclude 'inconnu' downtime cause if present
    df = df[df['Cause_arret'].str.lower() != 'inconnu']

    # Calculate overall average efficiency (over all data)
    overall_avg = df['Efficacite'].mean()

    # Calculate average efficiency by month and downtime cause
    avg_per_group = df.groupby(['Mois', 'Cause_arret'])['Efficacite'].mean()

    # Calculate impact = overall average - average per month & cause
    impact = overall_avg - avg_per_group

    # Prepare a summary DataFrame
    summary = pd.DataFrame({
        'Efficacite_moyenne (%)': (avg_per_group * 100).round(2),
        'Impact_sur_efficacite (%)': (impact * 100).round(2)
    }).reset_index()

    # Sort by month then by impact descending
    summary = summary.sort_values(by=['Mois', 'Impact_sur_efficacite (%)'], ascending=[True, False])

        # Save to CSV (optional)
    summary.to_csv('impact_cause_arret.csv', index=True)

    # Print summary
    print("Impact de chaque cause d'arret sur l'efficacité de production (en pourcentage):")
    print(summary)

    return summary  # ✅ Add this line


if __name__ == "__main__":
    cleaned_data_path = 'data nettoye.csv'  # Change if needed
    analyze_downtime_impact(cleaned_data_path)

