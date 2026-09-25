# 🏠 Prix immobiliers en Île-de-France — Analyse géospatiale & prédiction

> Du data.gouv.fr au modèle de prédiction : combiner analyse géospatiale et Machine Learning pour estimer les prix au m².

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Contexte

Les données DVF (Demandes de Valeurs Foncières) rendent publiques toutes les transactions immobilières en France. Ce projet exploite ces données pour mener une double analyse : d'abord comprendre les dynamiques de prix en Île-de-France, puis construire un modèle prédictif capable d'estimer le prix d'un bien à partir de ses caractéristiques.

## 🎯 Objectifs

- Cartographier les prix médians au m² par commune en Île-de-France
- Identifier les micro-marchés et les facteurs de prix
- Construire un modèle ML de prédiction de prix (XGBoost)
- Déployer une app Streamlit interactive : carte + prédicteur

## 🔧 Stack technique

| Outil | Usage |
|-------|-------|
| **Python 3.10+** | Langage principal |
| **Pandas / GeoPandas** | Manipulation et données géospatiales |
| **Scikit-learn / XGBoost** | Modélisation prédictive |
| **Plotly / Folium** | Visualisations et cartes |
| **Streamlit** | App interactive |

## 📁 Structure du projet

```
03-immobilier-idf/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── README.md
│   ├── download_data.py
│   ├── raw/
│   ├── processed/
│   └── sample/
├── notebooks/
│   ├── 01_eda_geospatiale.ipynb
│   └── 02_modelisation.ipynb
├── app/
│   └── streamlit_app.py
├── models/                     ← Gitignored
├── assets/
└── scripts/
    └── security_check.sh
```

## 🚀 Démarrage rapide

```bash
git clone https://github.com/DiogoA78/03-immobilier-idf.git
cd 03-immobilier-idf
pip install -r requirements.txt
python data/download_data.py
jupyter notebook notebooks/01_eda_geospatiale.ipynb
```

### Lancer l'app Streamlit

```bash
streamlit run app/streamlit_app.py
```

## 📊 Démo live

> [🔗 Voir l'app sur Streamlit Cloud](https://diogoa78-07-demonstrateur-hsrfdt8xqoiobofkvqmaqd.streamlit.app/)

## 📄 Source des données

- **DVF — Demandes de Valeurs Foncières**
- Éditeur : DGFiP (Direction Générale des Finances Publiques)
- Licence : Licence Ouverte
- URL : [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)

## 📜 Licence

MIT — voir [LICENSE](LICENSE).
