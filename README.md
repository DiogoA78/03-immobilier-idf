🇫🇷 [Version française](README_FR.md)

# 🏠 Real Estate Prices in Île-de-France — Geospatial Analysis & Prediction

> From data.gouv.fr to a prediction model: combining geospatial analysis and Machine Learning to estimate prices per m².

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Context

DVF data (Demandes de Valeurs Foncières) makes all real estate transactions in France publicly available. This project leverages this data for a dual analysis: first understanding price dynamics in the Île-de-France region, then building a predictive model capable of estimating a property's price based on its characteristics.

## 🎯 Objectives

- Map median prices per m² by municipality in Île-de-France
- Identify micro-markets and price drivers
- Build an ML price prediction model (XGBoost)
- Deploy an interactive Streamlit app: map + predictor

## 🔧 Tech Stack

| Tool | Usage |
|------|-------|
| **Python 3.10+** | Main language |
| **Pandas / GeoPandas** | Data manipulation and geospatial data |
| **Scikit-learn / XGBoost** | Predictive modeling |
| **Plotly / Folium** | Visualizations and maps |
| **Streamlit** | Interactive app |

## 📁 Project Structure

```
03-immobilier-idf/
├── README.md                          ← This file
├── README_FR.md                       ← French version
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
├── models/                            ← Gitignored
├── assets/
└── scripts/
    └── security_check.sh
```

## 🚀 Quick Start

```bash
git clone https://github.com/DiogoA78/03-immobilier-idf.git
cd 03-immobilier-idf
pip install -r requirements.txt
python data/download_data.py
jupyter notebook notebooks/01_eda_geospatiale.ipynb
```

### Launch the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

## 📊 Live Demo

> [🔗 View the app on Streamlit Cloud](https://diogoa78-07-demonstrateur-hsrfdt8xqoiobofkvqmaqd.streamlit.app/)

## 📄 Data Source

- **DVF — Demandes de Valeurs Foncières** (Property Value Requests)
- Publisher: DGFiP (French Directorate General of Public Finances)
- License: Open Licence
- URL: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)

## 📜 License

MIT — see [LICENSE](LICENSE).
