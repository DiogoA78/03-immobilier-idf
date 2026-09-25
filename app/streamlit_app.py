"""
🏠 Prix immobiliers IDF — App Streamlit
Carte interactive + prédicteur de prix

Usage : streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
from pathlib import Path

# ── Config ──
st.set_page_config(
    page_title="Prix immobiliers IDF",
    page_icon="🏠",
    layout="wide",
)

# ── Paths ──
ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "processed"
MODELS = ROOT / "models"

# ── Chargement données & modèle ──
@st.cache_data
def load_data():
    """Charge les données nettoyées."""
    path = DATA / "dvf_clean.csv"
    if not path.exists():
        st.error("❌ Fichier dvf_clean.csv non trouvé. Lance d'abord le notebook 1.")
        st.stop()
    df = pd.read_csv(path)
    return df


@st.cache_resource
def load_model():
    """Charge le modèle entraîné."""
    model_path = MODELS / "best_model.pkl"
    features_path = MODELS / "features_list.pkl"
    encoder_path = MODELS / "label_encoder_dep.pkl"

    if not model_path.exists():
        return None, None, None

    model = joblib.load(model_path)
    features = joblib.load(features_path)
    encoder = joblib.load(encoder_path)
    return model, features, encoder


# ── Données ──
df = load_data()
model, features, le_dep = load_model()

# ── Sidebar ──
st.sidebar.title("🏠 Navigation")
page = st.sidebar.radio("Page", ["🗺️ Carte des prix", "🔮 Prédicteur de prix", "📊 Statistiques"], label_visibility="hidden")

DEP_NAMES = {
    "75": "Paris", "77": "Seine-et-Marne", "78": "Yvelines",
    "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne", "95": "Val-d'Oise",
}

# ════════════════════════════════════════════
# PAGE 1 : CARTE
# ════════════════════════════════════════════
if page == "🗺️ Carte des prix":
    st.title("🗺️ Carte des prix au m² — Île-de-France")

    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        dep_filter = st.multiselect(
            "Département",
            options=sorted(df["departement"].unique()),
            format_func=lambda x: f"{x} — {DEP_NAMES.get(x, x)}",
            default=sorted(df["departement"].unique()),
        )
    with col2:
        type_filter = st.multiselect(
            "Type de bien",
            options=df["type_local"].unique(),
            default=df["type_local"].unique(),
        )
    with col3:
        prix_range = st.slider(
            "Prix au m² (€)",
            min_value=int(df["prix_m2"].quantile(0.01)),
            max_value=int(df["prix_m2"].quantile(0.99)),
            value=(1000, 15000),
        )

    # Filtrer
    mask = (
        df["departement"].isin(dep_filter) &
        df["type_local"].isin(type_filter) &
        df["prix_m2"].between(prix_range[0], prix_range[1])
    )
    df_filtered = df[mask]

    st.caption(f"{len(df_filtered):,} transactions affichées")

    # Prix médian par commune
    commune_agg = (
        df_filtered.groupby(["nom_commune", "departement"])
        .agg(
            prix_m2_median=("prix_m2", "median"),
            nb_transactions=("prix", "count"),
            lat=("lat", "median"),
            lon=("lon", "median"),
        )
        .reset_index()
        .query("nb_transactions >= 10")
    )

    fig = px.scatter_map(
        commune_agg,
        lat="lat", lon="lon",
        size="nb_transactions",
        color="prix_m2_median",
        hover_name="nom_commune",
        hover_data={"prix_m2_median": ":.0f", "nb_transactions": True},
        color_continuous_scale="RdYlGn_r",
        range_color=[2000, 12000],
        zoom=9,
        center={"lat": 48.86, "lon": 2.35},
        map_style="carto-positron",
        title="Prix médian au m² par commune",
        height=600,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, width="stretch")


# ════════════════════════════════════════════
# PAGE 2 : PRÉDICTEUR
# ════════════════════════════════════════════
elif page == "🔮 Prédicteur de prix":
    st.title("🔮 Estimez le prix de votre bien")

    if model is None:
        st.warning("⚠️ Modèle non trouvé. Lance d'abord le notebook 2 (modélisation).")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Caractéristiques du bien")
        surface = st.number_input("Surface (m²)", min_value=9, max_value=500, value=50)
        nb_pieces = st.number_input("Nombre de pièces", min_value=1, max_value=10, value=2)
        type_bien = st.selectbox("Type de bien", ["Appartement", "Maison"])
        departement = st.selectbox(
            "Département",
            options=sorted(DEP_NAMES.keys()),
            format_func=lambda x: f"{x} — {DEP_NAMES[x]}",
            index=0,
        )

    with col2:
        st.subheader("Localisation")
        # Coordonnées par défaut selon le département
        default_coords = {
            "75": (48.8566, 2.3522), "92": (48.8283, 2.2183),
            "93": (48.9134, 2.4831), "94": (48.7904, 2.4679),
            "77": (48.5333, 2.6667), "78": (48.8048, 2.1203),
            "91": (48.6321, 2.4408), "95": (49.0333, 2.0667),
        }
        lat_default, lon_default = default_coords.get(departement, (48.86, 2.35))
        lat = st.number_input("Latitude", value=lat_default, format="%.4f")
        lon = st.number_input("Longitude", value=lon_default, format="%.4f")

    if st.button("💰 Estimer le prix", type="primary", use_container_width=True):

        # Construire le vecteur de features
        PARIS_LAT, PARIS_LON = 48.8566, 2.3522
        dist_paris = np.sqrt(
            ((lat - PARIS_LAT) * 111) ** 2 +
            ((lon - PARIS_LON) * 111 * np.cos(np.radians(48.85))) ** 2
        )

        # Encoder le département
        try:
            dep_encoded = le_dep.transform([departement])[0]
        except ValueError:
            dep_encoded = 0

        input_data = pd.DataFrame([{
            "surface": surface,
            "nb_pieces": nb_pieces,
            "log_surface": np.log1p(surface),
            "pieces_par_surface": nb_pieces / surface,
            "est_paris": 1 if departement == "75" else 0,
            "dist_paris_km": dist_paris,
            "dep_encoded": dep_encoded,
            "est_appartement": 1 if type_bien == "Appartement" else 0,
            "lat": lat,
            "lon": lon,
            "annee_num": 2024,
            "mois_num": 6,
        }])

        # S'assurer que les colonnes sont dans le bon ordre
        input_data = input_data[features]

        # Prédiction
        prix_predit = model.predict(input_data)[0]
        prix_m2_predit = prix_predit / surface

        # Affichage
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Prix estimé", f"{prix_predit:,.0f} €")
        c2.metric("📐 Prix au m²", f"{prix_m2_predit:,.0f} €/m²")
        c3.metric("📍 Distance Paris", f"{dist_paris:.1f} km")

        # Comparaison avec le marché
        median_dep = df[df["departement"] == departement]["prix_m2"].median()
        diff_pct = ((prix_m2_predit - median_dep) / median_dep) * 100

        if diff_pct > 0:
            st.info(f"📊 Ce bien est estimé **{diff_pct:.0f}% au-dessus** de la médiane "
                    f"du département ({median_dep:,.0f} €/m²)")
        else:
            st.info(f"📊 Ce bien est estimé **{abs(diff_pct):.0f}% en-dessous** de la médiane "
                    f"du département ({median_dep:,.0f} €/m²)")


# ════════════════════════════════════════════
# PAGE 3 : STATS
# ════════════════════════════════════════════
elif page == "📊 Statistiques":
    st.title("📊 Statistiques du marché immobilier IDF")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transactions", f"{len(df):,}")
    c2.metric("Prix médian", f"{df['prix'].median():,.0f} €")
    c3.metric("Prix/m² médian", f"{df['prix_m2'].median():,.0f} €")
    c4.metric("Surface médiane", f"{df['surface'].median():.0f} m²")

    # Prix par département
    dep_stats = (
        df.groupby("departement")
        .agg(prix_m2_median=("prix_m2", "median"), nb=("prix", "count"))
        .reset_index()
        .sort_values("prix_m2_median", ascending=False)
    )
    dep_stats["nom"] = dep_stats["departement"].map(DEP_NAMES)

    fig = px.bar(
        dep_stats, x="nom", y="prix_m2_median",
        color="prix_m2_median", color_continuous_scale="RdYlGn_r",
        title="Prix médian au m² par département",
        labels={"nom": "", "prix_m2_median": "€/m²"},
        template="plotly_white",
    )
    st.plotly_chart(fig, width="stretch")

    # Distribution
    fig = px.histogram(
        df, x="prix_m2", nbins=80,
        title="Distribution du prix au m²",
        labels={"prix_m2": "Prix au m² (€)"},
        template="plotly_white",
    )
    st.plotly_chart(fig, width="stretch")
