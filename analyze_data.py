import pandas as pd

def analyze_downtime_impact(df):
    df = df[df['Cause_arret'].str.lower() != 'inconnu']

    overall_avg = df['Efficacite'].mean()

    avg_per_group = df.groupby(['Mois', 'Cause_arret'])['Efficacite'].mean()

    impact = overall_avg - avg_per_group

    summary = pd.DataFrame({
        'Efficacite_moyenne (%)': (avg_per_group * 100).round(2),
        'Impact_sur_efficacite (%)': (impact * 100).round(2)
    }).reset_index()

    summary = summary.sort_values(by=['Mois', 'Impact_sur_efficacite (%)'], ascending=[True, False])

    return summary
