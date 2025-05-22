import pandas as pd

def analyze_downtime_impact(data_path):
    if isinstance(data_path, str):
        df = pd.read_csv(data_path)
    else:
        df = data_path.copy()

    if 'Mois' not in df.columns and 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Mois'] = df['Date'].dt.month.map({
            1: 'janvier', 2: 'fevrier', 3: 'mars', 4: 'avril',
            5: 'mai', 6: 'juin', 7: 'juillet', 8: 'aout',
            9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'decembre'
        })

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
