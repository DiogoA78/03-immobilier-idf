"""
Téléchargement des données DVF (Demandes de Valeurs Foncières)
pour l'Île-de-France.

Source : data.gouv.fr — DGFiP
Fichiers géo-DVF par département et année.

Usage :
    python data/download_data.py
    python data/download_data.py --years 2022 2023
"""

import argparse
from pathlib import Path

import requests
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).parent
RAW_DIR = SCRIPT_DIR / "raw"
SAMPLE_DIR = SCRIPT_DIR / "sample"

# Départements Île-de-France
IDF_DEPS = ["75", "77", "78", "91", "92", "93", "94", "95"]

# Années disponibles
AVAILABLE_YEARS = list(range(2019, 2025))
DEFAULT_YEARS = [2022, 2023, 2024]

# URL pattern pour geo-dvf
BASE_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv"


def download_file(url: str, filepath: Path, retries: int = 3) -> bool:
    """Télécharge un fichier avec barre de progression."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, stream=True, timeout=120)
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            with open(filepath, "wb") as f:
                with tqdm(total=total, unit="B", unit_scale=True,
                          desc=f"    {filepath.name}", leave=True) as pbar:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)
                        pbar.update(len(chunk))
            return True
        except requests.RequestException as e:
            if attempt < retries:
                print(f"    ⚠️  Tentative {attempt}/{retries} échouée : {e}")
            else:
                print(f"    ❌ Échec : {e}")
                return False
    return False


def download_years(years: list[int]) -> dict:
    """Télécharge les fichiers DVF pour les années et départements IDF."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stats = {"success": 0, "failed": 0, "skipped": 0}

    for year in sorted(years):
        print(f"\n📅 Année {year}")
        for dep in IDF_DEPS:
            filename = f"dvf-{year}-{dep}.csv"
            filepath = RAW_DIR / filename

            if filepath.exists() and filepath.stat().st_size > 0:
                print(f"    ✓ {filename} — déjà présent")
                stats["skipped"] += 1
                continue

            # Essayer plusieurs patterns d'URL
            urls_to_try = [
                f"{BASE_URL}/{year}/departements/{dep}.csv.gz",
                f"{BASE_URL}/{year}/departements/{dep}.csv",
            ]

            downloaded = False
            for url in urls_to_try:
                if ".gz" in url:
                    import gzip
                    import tempfile
                    temp = filepath.with_suffix(".csv.gz")
                    if download_file(url, temp):
                        try:
                            with gzip.open(temp, "rb") as f_in:
                                with open(filepath, "wb") as f_out:
                                    f_out.write(f_in.read())
                            temp.unlink()
                            downloaded = True
                            break
                        except Exception:
                            temp.unlink(missing_ok=True)
                else:
                    if download_file(url, filepath):
                        downloaded = True
                        break

            if downloaded:
                stats["success"] += 1
            else:
                stats["failed"] += 1

    return stats


def create_sample(n_rows: int = 500) -> None:
    """Crée un échantillon."""
    import pandas as pd
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    sample_path = SAMPLE_DIR / f"sample_{n_rows}.csv"

    if sample_path.exists():
        print(f"\n✓ Échantillon déjà présent")
        return

    # Trouver le premier fichier disponible
    files = sorted(RAW_DIR.glob("dvf-*.csv"))
    if not files:
        print("\n⚠️  Pas de données pour l'échantillon")
        return

    print(f"\n📝 Échantillon depuis {files[0].name}...")
    for enc in ["utf-8", "latin-1"]:
        try:
            df = pd.read_csv(files[0], nrows=n_rows, encoding=enc)
            df.to_csv(sample_path, index=False)
            print(f"  ✓ {sample_path.name} créé")
            return
        except UnicodeDecodeError:
            continue


def main():
    parser = argparse.ArgumentParser(description="Télécharger DVF Île-de-France")
    parser.add_argument("--years", type=int, nargs="+", default=DEFAULT_YEARS,
                        help=f"Années (défaut: {DEFAULT_YEARS})")
    args = parser.parse_args()

    print("=" * 60)
    print("📥 Téléchargement DVF — Île-de-France")
    print(f"   Départements : {', '.join(IDF_DEPS)}")
    print(f"   Années : {args.years}")
    print("=" * 60)

    stats = download_years(args.years)
    create_sample()

    print("\n" + "=" * 60)
    print(f"📊 Bilan : ✓ {stats['success']} | → {stats['skipped']} déjà là | ✗ {stats['failed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
