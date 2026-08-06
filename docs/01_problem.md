# Problem Definition

## Background

Medical images contain more information than can be captured through visual
inspection alone. Radiomics aims to extract quantitative characteristics from
medical images, such as tumour shape, intensity distribution and texture.

These imaging features may contain prognostic information about disease
progression and patient survival. Combining radiomics with survival analysis
therefore provides a natural link between medical imaging, biostatistics and
machine learning.

## Project Objective

The objective of this project is to investigate whether quantitative features
extracted from pre-treatment CT images can be used to predict survival outcomes
in patients with non-small cell lung cancer.

The project will compare a classical statistical survival model with a
machine-learning-based survival model:

- Cox proportional hazards model
- Random survival forest

An optional later extension may include a neural-network-based survival model.

## Primary Research Question

Can radiomic features extracted from pre-treatment CT images provide useful
prognostic information for overall survival in patients with non-small cell
lung cancer?

## Secondary Research Questions

1. Which radiomic feature groups are associated with survival outcomes?
2. How does a Cox proportional hazards model compare with a random survival
   forest in terms of predictive performance?
3. Does nonlinear modelling improve prediction compared with the classical Cox
   model?
4. How stable are the selected features and model predictions?
5. How well calibrated are the predicted survival probabilities?
6. What additional value do radiomic features provide beyond available clinical
   variables?

## Scope

The initial project scope includes:

1. loading CT images and tumour segmentations;
2. extracting predefined radiomic features;
3. cleaning and preprocessing the resulting feature matrix;
4. conducting exploratory survival analysis;
5. fitting a Cox proportional hazards model;
6. fitting a random survival forest;
7. comparing the models using survival-specific evaluation metrics;
8. documenting assumptions, limitations and results.

The initial version will use existing expert tumour segmentations. Training a
segmentation model is explicitly outside the first project scope.

## Outcomes

The main outcome will be overall survival, represented by:

- an observed follow-up time;
- an event indicator describing whether death was observed or the observation
  was censored.

The exact variable names and definitions will be verified against the clinical
metadata supplied with the selected dataset.

## Evaluation Criteria

The models will primarily be evaluated using:

- concordance index;
- time-dependent Brier score;
- integrated Brier score;
- time-dependent ROC or AUC;
- calibration at selected time horizons.

For the Cox model, the proportional hazards assumption and coefficient
uncertainty will also be examined.

## Intended Deliverables

The project will produce:

- a reproducible Python pipeline;
- documented radiomic feature extraction;
- classical and machine-learning survival models;
- model comparison tables and visualisations;
- a technical report describing methods, assumptions and limitations;
- automated tests for selected preprocessing and evaluation components.

## Scientific and Practical Limitations

This is an exploratory portfolio and research project rather than a validated
clinical prediction tool.

The results must not be interpreted as clinical recommendations. Potential
limitations include:

- retrospective data collection;
- limited sample size relative to the number of radiomic features;
- censoring;
- possible missing clinical information;
- scanner and acquisition heterogeneity;
- segmentation variability;
- risk of overfitting and data leakage;
- lack of independent external validation.