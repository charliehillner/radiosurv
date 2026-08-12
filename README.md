# RadioSurv

**Radiomics and survival analysis from medical imaging data**

RadioSurv is a scientific data analysis project exploring whether quantitative features extracted from medical CT images can provide prognostic information for survival outcomes.

The project combines **medical image analysis, radiomics, survival analysis, and machine learning** within a reproducible scientific workflow.

Rather than starting directly with predictive modelling, the project follows a research-oriented approach:

> **Understand the clinical question → understand the data → extract meaningful quantitative features → build and validate statistical and machine-learning models → interpret the results**

## Research Motivation

Medical images contain substantially more information than what is immediately visible to the human eye.

Radiomics attempts to quantify this information by extracting numerical characteristics from defined regions of interest, such as tumors. These features may describe properties including:

- tumor size and shape,
- distribution of CT attenuation values,
- tissue heterogeneity,
- and spatial texture patterns.

The central question of this project is whether such imaging-derived information can contribute to the prediction of patient survival.

The project will investigate this question using both **classical survival analysis** and **machine-learning approaches**.

## Research Questions

The project is structured around several questions:

1. Which quantitative characteristics can be extracted from segmented tumors in CT images?
2. Are individual radiomic features associated with survival outcomes?
3. Can radiomic features provide prognostic information beyond available clinical variables?
4. How does a classical statistical survival model compare with more flexible machine-learning approaches?
5. How stable are the resulting models under appropriate validation procedures?

These questions will be refined as the dataset and its limitations are explored in more detail.

## Dataset

The project uses the **NSCLC-Radiomics (LUNG1)** collection from The Cancer Imaging Archive (TCIA).

The collection contains imaging and clinical data from patients with non-small-cell lung cancer (NSCLC), including CT imaging and tumor delineations.

The original medical data are **not included in this repository**.

### Initial DICOM Inspection

Initial exploration of patient `LUNG1-001` identified a study containing:

- a CT series consisting of 134 DICOM images,
- an RT Structure Set (`RTSTRUCT`),
- a DICOM Segmentation (`SEG`) object.

The inspected CT series has:

- matrix size: `512 × 512`,
- pixel spacing: approximately `0.977 × 0.977 mm`,
- slice thickness: `3 mm`.

The DICOM SEG object contains four segmented structures:

- primary neoplasm (`GTV-1`),
- left lung,
- right lung,
- spinal cord.

These observations currently refer specifically to the inspected case and should not yet be assumed to hold for the complete cohort.

## Mathematical View of the Imaging Data

A CT scan consists of a sequence of two-dimensional image slices that
together represent a three-dimensional region of the patient's body.

Let

$$
\Omega \subset \mathbb{R}^3
$$

denote the spatial region covered by the CT acquisition in the DICOM
patient coordinate system. A point

$$
(x,y,z) \in \Omega
$$

therefore represents a physical location within the scanned volume, with
coordinates measured in millimetres.

In practice, the CT image does not provide measurements at every point
of this continuous region. Instead, $\Omega$ is sampled on a discrete
three-dimensional voxel grid whose geometry is determined by the DICOM
metadata, including pixel spacing, image orientation, and slice
positions.

The CT image can therefore be interpreted conceptually as a spatially
calibrated scalar field

$$
HU : \Omega \rightarrow \mathbb{R},
$$

where $HU(x,y,z)$ denotes the Hounsfield Unit associated with a spatial
location $(x,y,z)$.

The gross tumor volume is represented by a binary segmentation mask

$$
M_{\mathrm{GTV}} : \Omega \rightarrow \{0,1\},
$$

where $M_{\mathrm{GTV}}(x,y,z)=1$ indicates that the corresponding
location belongs to the segmented tumor.

The tumor region can consequently be defined as

$$
\Omega_{\mathrm{GTV}}
=
\{\,
(x,y,z)\in\Omega
\mid
M_{\mathrm{GTV}}(x,y,z)=1
,\}.
$$

Radiomics aims to quantitatively characterize the CT information and
spatial structure within this region.

## From CT Images to Quantitative Data

A CT scan can be represented as a spatially calibrated three-dimensional field of CT values.

For each voxel, DICOM provides both image information and metadata describing its physical location within the patient coordinate system.

Stored CT pixel values are transformed to Hounsfield Units (HU) using the DICOM rescaling parameters:

$$
HU = \text{pixel value} \cdot \text{RescaleSlope}
     + \text{RescaleIntercept}
$$

The tumor segmentation defines a region of interest (ROI) within this volume.

Conceptually, the subsequent radiomics analysis therefore investigates the CT field

$$
HU(x,y,z)
$$

restricted to locations belonging to the segmented gross tumor volume (GTV):

$$
M_{\mathrm{GTV}}(x,y,z) = \begin{cases}
1, & \text{if } (x,y,z) \text{ belongs to the GTV},\\
0, & \text{otherwise}.
\end{cases}.
$$

This provides the basis for extracting quantitative descriptions of tumor intensity, heterogeneity, texture, size, and shape.

Radiomic features are extracted from the CT field restricted to the tumor region:

$$
\{\,HU(x,y,z) \mid M_{\mathrm{GTV}}(x,y,z)=1\,\}
$$


## Planned Analysis

The project will be developed incrementally.

### Phase 0 — Problem and Data Understanding

- define the scientific problem and research questions,
- characterize the patient cohort,
- understand the DICOM imaging structure,
- inspect CT geometry and Hounsfield Units,
- identify tumor segmentations,
- understand clinical variables and survival endpoints,
- assess completeness and potential data-quality issues.

### Phase 1 — Radiomics

- reconstruct CT volumes and tumor masks,
- investigate image preprocessing requirements,
- extract first-order intensity features,
- extract shape features,
- extract texture features,
- assess feature distributions and redundancy.

### Phase 2 — Survival Analysis

A classical statistical model will establish an interpretable baseline.

Planned methods include:

- Kaplan–Meier analysis,
- Cox proportional hazards models,
- assessment of model assumptions,
- appropriate survival-specific performance measures.

### Phase 3 — Machine Learning

Radiomics-based survival prediction will subsequently be explored using more flexible models such as:

- penalized survival models,
- Random Survival Forests,
- potentially neural survival models.

The purpose is not simply to identify the model with the highest score, but to investigate whether additional model complexity provides robust prognostic value.

## Project Structure

```text
radiosurv/
├── data/
│   ├── raw/             # Original data (not tracked)
│   ├── interim/         # Intermediate representations
│   └── processed/       # Analysis-ready datasets
│
├── docs/
│   ├── 01_problem.md
│   ├── 02_dataset.md
│   ├── 03_radiomics.md
│   ├── 04_survival_models.md
│   └── 05_results.md
│
├── notebooks/
│   └── 01_data_inspection.ipynb
│
├── src/
├── tests/
└── README.md
```

The documentation is intended to capture not only the final implementation but also the scientific reasoning behind methodological decisions.

## Current Status

🚧 **Work in progress**

The project is currently in the **data-understanding phase**.

So far, the DICOM structure of an initial patient has been inspected, the CT volume has been reconstructed and visualized, and DICOM segmentation data have been spatially aligned with the corresponding CT images.

The next steps are to systematically characterize the complete dataset, clinical variables, survival endpoints, and segmentation structure before beginning radiomic feature extraction or predictive modelling.

## Guiding Principle

This project deliberately treats machine learning as one component of a broader scientific analysis rather than as the starting point.

The objective is not only to train predictive models, but to understand:

- what information is contained in the data,
- how quantitative imaging features are constructed,
- which assumptions the statistical models require,
- whether observed predictive improvements are robust,
- and what conclusions the available data actually support.