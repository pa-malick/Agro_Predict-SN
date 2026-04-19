import plotly.express as px
import folium


def plot_yield_distribution(df):
    """Graphique des rendements par culture et region."""
    fig = px.box(
        df,
        x='crop',
        y='yield_ton_ha',
        color='region',
        title="Distribution des rendements par culture et par region",
        labels={"yield_ton_ha": "Rendement (tonnes/ha)"}
    )
    return fig


def create_senegal_map(example_preds):
    """Cree une carte interactive simple du Senegal."""
    m = folium.Map(location=[14.5, -14.5], zoom_start=6, tiles="CartoDB positron")

    regions_coords = {
        "Thies":       [14.79, -16.92],
        "Fatick":      [14.35, -16.41],
        "Kaolack":     [14.15, -15.91],
        "Saint-Louis": [16.02, -16.49],
        "Kaffrine":    [14.10, -15.55],
        "Tambacounda": [13.77, -13.67],
        "Sedhiou":     [12.82, -15.55],
    }

    for reg, coord in regions_coords.items():
        pred = example_preds.get(reg, "N/D")
        folium.Marker(
            location=coord,
            popup=f"<b>{reg}</b><br>Rendement prevu : {pred} t/ha",
            tooltip=reg,
            icon=folium.Icon(color="green", icon="leaf"),
        ).add_to(m)

    return m
