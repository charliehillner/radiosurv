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

### Questions to investigate

The following cohort characteristics still need to be systematically
investigated:

- number of patients,
- disease characteristics,
- demographic characteristics,
- treatment information,
- inclusion and exclusion criteria,
- availability of imaging and segmentation data,
- availability of clinical outcome data.

These characteristics will be documented after inspection of the
collection-level metadata and clinical data.


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

### Questions to investigate

The available clinical data still need to be inspected systematically.

Of particular interest are:

- patient demographics,
- tumor characteristics,
- disease stage,
- treatment-related variables,
- survival information,
- potential prognostic covariates,
- missing values.

These variables will determine which clinical baseline models can be
constructed and whether radiomic features provide additional prognostic
information.


## 7. Survival Endpoints

The exact survival endpoint must be determined from the available clinical
data and dataset documentation.

For survival analysis, at minimum two quantities are required for each
patient:

$$
T_i = \text{observed follow-up time}
$$

and

$$
\delta_i =
\begin{cases}
1, & \text{event observed},\\
0, & \text{right-censored}.
\end{cases}
$$

Before modelling, the following questions must therefore be resolved:

- What event is represented by the available survival endpoint?
- From which starting point is survival time measured?
- In which unit is follow-up time recorded?
- How is censoring represented?
- Are survival time and event status available for all patients?
- Are there inconsistencies or implausible values?


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