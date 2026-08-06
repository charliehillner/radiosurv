# Dataset

## Selected Dataset

The initial dataset selected for this project is the NSCLC-Radiomics collection
provided by The Cancer Imaging Archive (TCIA).

The collection contains data from 422 patients with non-small cell lung cancer.
For these patients, the dataset provides:

- pre-treatment computed tomography scans;
- manually delineated three-dimensional gross tumor volumes;
- clinical outcome information.

The collection is also known as the Lung1 dataset and was used in a published
radiomics study.

## Rationale for Selection

The dataset is suitable for this project because it combines all three major
components required by the planned workflow:

1. medical imaging data;
2. expert tumour segmentations;
3. clinical outcome data.

Existing segmentations allow the initial project to focus on radiomic feature
extraction and survival modeling rather than first requiring the development
of a segmentation model.

The cohort size is also large enough for an exploratory comparison of survival
models, although careful feature reduction and validation will still be
required because the number of candidate radiomic features may be large
relative to the number of patients and observed events.

## Data Modalities

### CT Imaging

The imaging component consists of pre-treatment CT scans. The precise imaging
parameters, voxel dimensions and acquisition protocols will be inspected after
download.

Relevant metadata may include:

- slice thickness;
- pixel spacing;
- reconstruction settings;
- scanner manufacturer;
- image dimensions;
- voxel spacing.

These characteristics matter because radiomic features can be sensitive to
image acquisition and reconstruction differences.

### Tumour Segmentations

The dataset includes manually delineated three-dimensional gross tumor
volumes produced by a radiation oncologist.

The segmentation masks define the regions of interest from which radiomic
features will be extracted.

Before feature extraction, the following checks will be performed:

- the segmentation can be matched uniquely to the corresponding CT scan;
- the mask and image use compatible coordinate systems;
- the mask contains a non-empty tumour region;
- the mask lies within the image dimensions;
- voxel spacing and orientation are interpreted correctly.

### Clinical and Survival Data

The clinical metadata contain outcome information suitable for survival
analysis.

The following variables must be identified and verified before modeling:

- patient identifier;
- survival or follow-up time;
- event or censoring indicator;
- available demographic variables;
- tumour stage;
- treatment-related variables;
- other relevant clinical covariates.

The coding and units of all survival variables must be verified from the
dataset documentation rather than inferred from column names alone.

## Unit of Analysis

The intended unit of analysis is one patient.

Each patient should contribute:

- one baseline CT examination;
- one associated tumor segmentation;
- one survival outcome;
- one row in the final modeling table.

If multiple scans or segmentations exist for a patient, explicit selection
rules will be defined before analysis.

## Planned Data Representation

Raw imaging data will be stored separately from the modeling dataset.

The processed modeling table will have a structure similar to:

| patient_id | survival_time | event | clinical_feature_1 | radiomic_feature_1 | ... |
|------------|---------------|-------|--------------------|---------------------|-----|

The final feature matrix must contain no direct identifiers.

## Data Directory Structure

```text
data/
├── raw/
│   ├── images/
│   ├── segmentations/
│   └── clinical/
├── interim/
│   ├── image_metadata/
│   └── extracted_features/
└── processed/
    └── modelling_dataset.parquet