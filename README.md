# Machine learning for virtual reality experiment with pupillometry and physiological signals

## Overview

This code is meant for analysis of the dataset collected during study with virtual reality headset and bitalino equipment.

## Scripts

Scripts are divided into several directories:

* **preprocessing**:
  * **config.py** - configuration of data paths and random seed's value.
  * **data_merging.py** - iterating over all users - collecting all data for a given user, preprocessing, merging into one file for each user, then one file for all users:
    * calculating statistical features on a given time (window, rolling): mean, variance, skewness and kurtosis for all signals,
    * number of fixations on a given time (window, rolling).
  * **disp_parquet_sample.py** - displaying a sample of a parquet file for a given user.
  * **bitalino_processing.py** - processing of bitalino data:
    * dropping blank columns,
    * rescaling columns with sensor resolution,
    * dropping triggers < 40_000 and >= 45_000,
    * dropping rows with HR < 15 or HR = inf,
    * standaring HR, EKG, EDA, light with StandardScaler(),
    * dropping empty rows,
    * dropping lp column.
  * **pupil_positions_processing.py** - processing of pupil positions data
    * thresholding by confidence (0.8), 
    * choosing only 2d c++ method, 
    * dropping irrelevant columns.
  * **pupil_fixations_processing.py** - processing of pupil fixations data:
    * thresholding by confidence (0.8), 
    * scaling duration,
    * dropping irrelevant columns, 
    * renaming.
  * **pupil_annotations_processing.py** - processing of pupil annotations data.
  * **all_preprocesing.py** - running all preprocessing scripts described above for a given user.

* **analysis**:
    * **aggregate_triggers.py** - iterate through all bitalino data and group all users measurements by triggers.
    * **random_user_eda.ipynb** - very poor exploratory data analysis on a preprocessed data for a randomly chosen user.

* **machine_learning**:
    * **autokeras_learning.ipynb** - a quick performance test of the _AutoKeras_ library for automatic selection of neural network architecture.
    * **pycaret_learning.ipynb** - testing of the _PyCaret_ library for all data on different % of data.

## How to run these scripts?

1. Run _preprocessing/all_preprocessing.py_ to generate preprocessed data - one file for bitalino and 3 files for pupillometry per paritcipant.
2. Run _preprocessing/data_merging.py_ to generate merged data - one file for each study participant and one big file for all users.
3. Run _analysis/random_user_EDA.ipynb_ to analyse preprocessed data for a random user (introductory level only).
4. Run scripts in _machine_learning_ to train machine learning models and evaluate their performance with automl.