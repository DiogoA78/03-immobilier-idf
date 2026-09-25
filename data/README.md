# 📊 Données — DVF Île-de-France

## Source

- **Éditeur :** DGFiP (Direction Générale des Finances Publiques)
- **Licence :** Licence Ouverte
- **URL :** [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)
- **Fichiers geo-DVF :** [files.data.gouv.fr/geo-dvf](https://files.data.gouv.fr/geo-dvf/latest/csv/)

## Téléchargement

```bash
python data/download_data.py
python data/download_data.py --years 2022 2023 2024
```

## Départements Île-de-France

| Code | Département |
|------|-------------|
| 75 | Paris |
| 77 | Seine-et-Marne |
| 78 | Yvelines |
| 91 | Essonne |
| 92 | Hauts-de-Seine |
| 93 | Seine-Saint-Denis |
| 94 | Val-de-Marne |
| 95 | Val-d'Oise |

## Variables clés

| Variable | Description |
|----------|-------------|
| `date_mutation` | Date de la transaction |
| `valeur_fonciere` | Prix de la transaction (€) |
| `type_local` | Appartement / Maison / etc. |
| `surface_reelle_bati` | Surface en m² |
| `nombre_pieces_principales` | Nombre de pièces |
| `code_departement` | Code département |
| `nom_commune` | Nom de la commune |
| `code_postal` | Code postal |
| `latitude`, `longitude` | Coordonnées GPS |

## Structure attendue

```
data/
├── raw/                         ← Gitignored
│   ├── dvf-2022-75.csv
│   ├── dvf-2022-77.csv
│   └── ...
├── processed/                   ← Gitignored
│   ├── dvf_clean.parquet
│   └── dvf_looker.csv
└── sample/
    └── sample_500.csv
```
