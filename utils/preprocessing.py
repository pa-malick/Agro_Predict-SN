import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def preprocess_data(df):
    """Prépare les données pour l'entraînement : encodage des variables catégorielles."""
    # Features numériques et catégorielles
    numeric_cols = ['year', 'rainfall_mm', 'temp_avg_c', 'ndvi_avg']
    cat_cols = ['region', 'crop', 'soil_type']
    
    # Encodage OneHot
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_cat = encoder.fit_transform(df[cat_cols])
    encoded_df = pd.DataFrame(encoded_cat, columns=encoder.get_feature_names_out(cat_cols))
    
    # Concaténation
    X = pd.concat([df[numeric_cols].reset_index(drop=True), encoded_df], axis=1)
    y = df['yield_ton_ha']
    
    return X, y, encoder