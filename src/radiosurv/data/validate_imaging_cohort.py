from pathlib import Path

import pandas as pd
import pydicom

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "images"
    / "NSCLC-Radiomics"
)

def read_modality(dicom_path: Path) -> str | None:
    """Read the DICOM modality without loading pixel data."""
    try:
        ds = pydicom.dcmread(dicom_path, stop_before_pixels=True)
        return getattr(ds, "Modality", None)
    except Exception:
        return None

def inspect_patient(patient_dir: Path) -> dict:
    modality_counts = {}

    for dicom_path in patient_dir.rglob("*.dcm"):
        modality = read_modality(dicom_path)

        if modality is None:
            continue

        modality_counts[modality] = modality_counts.get(modality, 0) + 1

    return {
        "PatientID": patient_dir.name,
        "CT_present": modality_counts.get("CT", 0) > 0,
        "SEG_present": modality_counts.get("SEG", 0) > 0,
        "RTSTRUCT_present": modality_counts.get("RTSTRUCT", 0) > 0,
        "n_CT_files": modality_counts.get("CT", 0),
        "n_SEG_files": modality_counts.get("SEG", 0),
        "n_RTSTRUCT_files": modality_counts.get("RTSTRUCT", 0),
    }

def inspect_cohort(data_dir: Path) -> pd.DataFrame:
    patient_dirs = sorted(
        path
        for path in data_dir.iterdir()
        if path.is_dir() and path.name.startswith("LUNG1-")
    )

    records = [
        inspect_patient(patient_dir)
        for patient_dir in patient_dirs
    ]

    return pd.DataFrame(records)

if __name__ == "__main__":
    qc = inspect_cohort(DATA_DIR)

    OUTPUT_DIR = PROJECT_ROOT / "data" / "interim"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    qc.to_csv(
        OUTPUT_DIR / "imaging_qc.csv",
        index=False
    )

    print(qc.head())
    print()
    print(f"Patients found: {len(qc)}")
    print(
        qc[
            ["CT_present", "SEG_present", "RTSTRUCT_present"]
        ].sum()
    )
    print()
    print(qc["n_CT_files"].describe())
    print()
    print(
        qc["n_CT_files"]
        .value_counts()
        .sort_index()
    )
    print()
    missing_modalities = qc.loc[
        ~qc["CT_present"]
        | ~qc["SEG_present"]
        | ~qc["RTSTRUCT_present"]
        ]

    print(missing_modalities)