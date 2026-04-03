import pandas as pd
import os

def load_data():
    """
    Charge les données agricoles depuis le fichier CSV.
    Retourne un DataFrame pandas.
    """
    path = "data/raw/sample_yield_data.csv"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"""
        Le fichier de données n'existe pas : {path}
        
        Veuillez créer le dossier 'data/raw/' et y placer le fichier 'sample_yield_data.csv'.
        """)
    
    try:
        df = pd.read_csv(path)
        print(f"✅ Données chargées avec succès ! {len(df)} lignes trouvées.")
        return df
    except Exception as e:
        raise Exception(f"Erreur lors du chargement du fichier CSV : {e}")