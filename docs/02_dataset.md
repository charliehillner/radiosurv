# Dataset

## 1. Purpose of the Dataset Exploration

Before extracting radiomic features or fitting survival models, the dataset
must be understood at both the clinical and technical level.

The data exploration therefore aims to answer five main questions:

1. Which patients are included in the cohort?
2. Which imaging data are available?
3. Which segmentations are available and how are they related to the images?
4. Which clinical variables are available?
5. Which survival endpoints can be constructed?

A particular focus is placed on verifying the spatial relationship between
the CT images and tumor segmentations. Radiomic features can only be
meaningfully extracted if image values and segmentation masks refer to the
same physical locations within the patient.


## 2. Dataset Overview

This project uses the **NSCLC-Radiomics (LUNG1)** collection from
The Cancer Imaging Archive (TCIA).

The collection contains CT imaging, radiotherapy structure information,
segmentations, and clinical outcome information from patients with
non-small-cell lung cancer (NSCLC).

The original medical data are stored locally and are not included in this
repository.

> **Note:** The detailed DICOM observations below were initially obtained
> from the case `LUNG1-001`. They are used to understand the structure of
> the imaging data and must not automatically be assumed to apply identically
> to every patient in the cohort.


## 3. Patient Cohort

## 3. Patient Cohort

The clinical dataset contains 422 unique patients with non-small-cell lung
cancer (NSCLC). Each patient is represented by exactly one clinical record,
identified by a unique `PatientID` of the form `LUNG1-XXX`.

The cohort is predominantly composed of patients with locally advanced
disease. Overall clinical stage is available for 421 patients:

| Overall stage | Patients |
|---|---:|
| I | 93 |
| II | 40 |
| IIIa | 112 |
| IIIb | 176 |
| Missing | 1 |

Thus, 288 of 421 patients with known overall stage (68.4%) have stage IIIa
or IIIb disease.

The cohort contains 290 male and 132 female patients.

Age is available for 400 patients. The median age is 68.6 years, with
observed ages ranging from 33.7 to 91.7 years.

Pretreatment CT imaging is available as part of the LUNG1 collection.
Consequently, the imaging information used for radiomic feature extraction
precedes the survival follow-up starting at treatment initiation.


## 4. Imaging Data

### 4.1 DICOM Structure

Initial inspection of `LUNG1-001` identified three relevant DICOM series:

| Modality | Purpose | Files / Frames |
|---|---|---:|
| CT | Computed tomography images | 134 DICOM files |
| RTSTRUCT | Radiotherapy structure information | 1 DICOM file |
| SEG | DICOM segmentation object | 1 DICOM file containing 536 frames |

The CT series consists of individual two-dimensional image slices that
together describe a three-dimensional region of the patient.


### 4.2 CT Image Geometry

For `LUNG1-001`, each CT slice has an image matrix of

$$
512 \times 512
$$

pixels.

An inspected slice contained the following geometric metadata:

```text
Rows:                    512
Columns:                 512
PixelSpacing:            [0.9765625, 0.9765625]
SliceThickness:          3 mm
ImageOrientationPatient: [1, 0, 0, 0, 1, 0]
```

The pixel spacing indicates a distance of approximately

$$
0.977 \text{ mm} \times 0.977 \text{ mm}
$$

between neighbouring pixel centres within the image plane.

`ImagePositionPatient` specifies the physical position of the centre of
the first transmitted pixel of a slice in the DICOM patient coordinate
system.

For example, one inspected slice had

```text
ImagePositionPatient:
[-249.51171875, -460.51171875, -282.5]
```

with coordinates measured in millimetres.

`ImageOrientationPatient` provides two direction vectors describing the
orientation of the image rows and columns in the patient coordinate system.

Together,

- `ImagePositionPatient`,
- `ImageOrientationPatient`, and
- `PixelSpacing`

define the transformation from a two-dimensional image index $(i,j)$ to a
physical position $(x,y,z)$ within the patient.

Across the complete CT series, the slice positions provide the third
dimension of the reconstructed CT volume.

Thus, the image stack can be represented computationally as

$$
I[k,i,j],
$$

where $k$ denotes the slice index and $(i,j)$ the pixel position within a
slice, while the DICOM geometry establishes the corresponding physical
location

$$
(k,i,j) \longrightarrow (x,y,z).
$$


### 4.3 CT Values and Hounsfield Units

The values returned by the DICOM `pixel_array` are stored CT image values
resulting from the image reconstruction process.

For CT data, these stored values can be transformed into Hounsfield Units
using the DICOM rescaling parameters:

$$
HU =
I \cdot \text{RescaleSlope} +
\text{RescaleIntercept}.
$$

Hounsfield Units provide a standardized representation of X-ray attenuation
relative to water.

Conceptually, the reconstructed CT volume can therefore be interpreted as
a spatially calibrated, discretely sampled field

$$
HU(x,y,z),
$$

where $(x,y,z)$ denotes a physical position in the scanned region of the
patient.

This representation separates two aspects of the CT data:

- the **image value**, describing tissue attenuation through HU,
- the **geometry**, describing where that value is located within the patient.


## 5. Segmentations

### 5.1 Available Structures

The DICOM SEG object of `LUNG1-001` contains four segments:

| Segment | Label | Description |
|---:|---|---|
| 1 | Neoplasm, Primary | GTV-1 |
| 2 | Lung | Lung-Left |
| 3 | Lung | Lung-Right |
| 4 | Spinal cord | Spinal-Cord |

The gross tumor volume (`GTV-1`) is the primary region of interest for the
planned radiomics analysis.


### 5.2 SEG Frame Structure

The SEG object contains a total of 536 frames.

Inspection of the per-frame metadata using the referenced segment numbers
showed that the frames are distributed equally across the four segments:

| Segment | Total frames | Non-empty frames |
|---|---:|---:|
| GTV-1 | 134 | 21 |
| Lung-Left | 134 | 88 |
| Lung-Right | 134 | 86 |
| Spinal-Cord | 134 | 84 |

A frame may therefore exist for a particular structure and CT plane while
containing no segmented pixels.

For example, the GTV segmentation contains 134 frames but is non-empty on
only 21 of them.


### 5.3 Spatial Correspondence Between CT and SEG

The ordering of frames in a DICOM SEG object must not be assumed to be
identical to the ordering of CT slices.

Before constructing a three-dimensional tumor mask, the spatial
correspondence between the segmentation frames and the CT images was
therefore explicitly verified for `LUNG1-001`.

For each SEG frame, its physical image position was extracted from the
per-frame DICOM metadata. The corresponding CT slice was identified by
minimizing the Euclidean distance between the SEG frame position and all
CT slice positions:

$$
k^*
=
\operatorname*{arg\,min}_k
\left\lVert
p_{\mathrm{SEG}} - p_{\mathrm{CT},k}
\right\rVert_2.
$$

The resulting mapping showed that, for each of the four segments:

- all 134 SEG frames matched a CT slice,
- all 134 CT slice positions were represented exactly once,
- the matched CT indices covered the complete range from 0 to 133.

The maximum observed positional discrepancy was

$$
2.65 \times 10^{-5}\text{ mm},
$$

which is negligible at the spatial resolution of the images.

For `LUNG1-001`, the SEG object can therefore be interpreted as four
three-dimensional binary mask volumes aligned with the CT volume:

$$
M_{\mathrm{GTV}}[k,i,j],
$$

$$
M_{\mathrm{LeftLung}}[k,i,j],
$$

$$
M_{\mathrm{RightLung}}[k,i,j],
$$

and

$$
M_{\mathrm{SpinalCord}}[k,i,j].
$$

After spatial alignment, $HU[k,i,j]$ and $M_s[k,i,j]$ refer to the same
physical location within the patient.


### 5.4 Relevance for Radiomics

The spatial correspondence between CT and segmentation is a fundamental
requirement for subsequent radiomic feature extraction.

For the GTV, define the binary mask

$$
M_{\mathrm{GTV}}(x,y,z) \in \lbrace 0,1 \rbrace.
$$

The segmented tumor region is

$$
\Omega_{\mathrm{GTV}}
=
\lbrace
(x,y,z)\in\Omega
\mid
M_{\mathrm{GTV}}(x,y,z)=1
\rbrace.
$$

Only after establishing that the CT and segmentation share the same spatial
geometry can the CT values within the tumor be meaningfully defined as

$$
\lbrace
HU(x,y,z)
\mid
(x,y,z)\in\Omega_{\mathrm{GTV}}
\rbrace.
$$

This spatially aligned CT and GTV representation forms the basis for the
subsequent extraction of intensity, texture, size, and shape features.


## 6. Clinical Variables

## 6. Clinical Variables

The clinical dataset contains the following variables:

| Variable | Description | Missing |
|---|---|---:|
| `PatientID` | Patient identifier | 0 |
| `age` | Age | 22 |
| `clinical.T.Stage` | Clinical T-stage code | 1 |
| `Clinical.N.Stage` | Clinical N-stage code | 0 |
| `Clinical.M.Stage` | Clinical M-stage code | 0 |
| `Overall.Stage` | Overall clinical stage | 1 |
| `Histology` | Histological tumor type | 42 |
| `gender` | Sex | 0 |
| `Survival.time` | Observed survival/follow-up time | 0 |
| `deadstatus.event` | Survival event indicator | 0 |

The observed histological categories are:

| Histology | Patients |
|---|---:|
| Squamous cell carcinoma | 152 |
| Large cell | 114 |
| NOS | 63 |
| Adenocarcinoma | 51 |
| Missing | 42 |

The TNM variables are numerically encoded but should not automatically be
interpreted as continuous numerical variables.

Furthermore, several uncommon codes occur:

- `clinical.T.Stage = 5` for 2 patients,
- `Clinical.N.Stage = 4` for 3 patients,
- `Clinical.M.Stage = 3` for 4 patients.

These values fall outside the conventional integer ranges expected from a
simple encoding of the corresponding TNM categories. Their meaning has not
yet been established from the available variable documentation.

Internal consistency checks provide additional evidence that these values
should not be interpreted naively as conventional TNM categories. In
particular, all four patients with `Clinical.M.Stage = 3` are classified as
overall stage IIIa or IIIb rather than as metastatic stage IV disease.

The uncommon codes will therefore be retained unchanged during the data
understanding phase and must be resolved before the TNM variables are used
for statistical modelling.


## 7. Survival Endpoints

## 7. Survival Endpoints

The clinical dataset provides survival information for all 422 patients.

`Survival.time` represents the observed survival or follow-up time in days,
measured from the start of treatment.

Let

$$
T_i
$$

denote the true time from treatment initiation to death and

$$
C_i
$$

the censoring time. The observed time is therefore

$$
Y_i = \min(T_i,C_i).
$$

The variable `deadstatus.event` represents the event indicator

$$
\delta_i =
\begin{cases}
1, & \text{death observed},\\
0, & \text{right-censored}.
\end{cases}
$$

The cohort contains:

- 373 observed deaths (88.4%),
- 49 right-censored observations (11.6%).

For a censored patient with observed time $Y_i$, the exact survival time is
unknown; the available information is

$$
T_i > Y_i.
$$

Observed follow-up/survival times range from 10 to 4454 days, with a median
observed time of 545.5 days.

The median of the observed `Survival.time` variable must not be interpreted
as the median survival time. The latter must account for right censoring and
is defined through the estimated survival function, for example using the
Kaplan-Meier estimator.


## 8. Data Quality and Completeness

Before radiomic feature extraction, the complete cohort should be checked
systematically for:

- missing CT series,
- missing or unusable segmentations,
- missing clinical variables,
- missing survival outcomes,
- inconsistent patient identifiers,
- differences in image geometry,
- differences in voxel spacing,
- differences in slice thickness,
- unexpected segmentation structures,
- spatial inconsistencies between CT and segmentation.

The detailed investigation of `LUNG1-001` establishes the procedure for
these checks but does not yet demonstrate that the complete cohort has the
same structure.


## 9. Current Findings and Open Questions

### Established for `LUNG1-001`

- CT imaging can be reconstructed as a spatially calibrated 3D volume.
- The CT series contains 134 slices with a matrix size of 512 × 512.
- CT values can be transformed into Hounsfield Units.
- Four segmentation structures are available.
- GTV-1 represents the primary tumor ROI.
- Each segmentation contains 134 frames.
- CT and SEG positions show complete spatial correspondence.
- The GTV is non-empty on 21 CT planes.

### Still to be established for the complete cohort

- cohort characteristics,
- consistency of CT acquisition geometry,
- consistency and availability of GTV segmentations,
- clinical variable definitions,
- survival endpoint definition,
- censoring mechanism and coding,
- missingness and exclusions,
- preprocessing requirements before radiomic feature extraction.