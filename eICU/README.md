eICU-CRD  Benchmarks
=========================

The code is based on repository [eICU_Benchmark](https://github.com/mostafaalishahi/eICU_Benchmark) for [eICU Collaborative Research Database v2.0](https://physionet.org/content/eicu-crd/2.0/). 

---

## Database Description

### Stats of eICU Collaborative Research Database v2.0

|***`Number of patients`***|
|:------------------:|
|74336|

### Data Modalities

- **EHR**

### Prediction Tasks

|***`Task`***|***`Description`***|
|:----|:-----------|
|**In-hospital Mortality Prediction**|Predict in-hospital mortality based on the first 48 hours since admit.|
|**Length of Stay Prediction**|Predict remaining time spent in ICU at each hour of stay.|
|**Decompensation prediction**|Predict whether the patient's health will rapidly deteriorate in the next 24 hours.|
|**Phenotype Classification**|Classify whether a condition (ICD-9 code) is present in a particular ICU stay record.|

## Building the Benchmark

### eICU Preprocessing

1. Change the directory.

       cd eICU/

2. The following command generates one directory per each patient and writes patients demographics into `pats.csv`, the items extracted from Nursecharting into `nc.csv` and the lab items into `lab.csv` and then converts these three csv files into one `timeseries.csv` for each patient. you will have one csv file `all_data.csv` with all the patients data in a time-series manner for all the four tasks.

       python -m data_extraction.data_extraction_root {PATH TO eICU CSVs} data/root/

3. The following commands will generate formatted EHR csv file, which contains basic information of patiens, lables of prediction tasks and time series data. It will be stored in `data/processed/ehr/eICU_dataset_formatted.csv`.

       python -m preprocess_eICU {PATH TO eICU CSVs} data/root/ data/processed/


## Formatted CSV File Description

|***`Basic Information`***|***`(columns 0-3)`***|
|:---------------------|:-----------------|
|**PatientID**|`patientunitstayid` in raw CSVs.|
|**RecordTime**|`itemoffset` in raw CSVs.Relative time of the record since admit. (hours since admit)|
|**AdmissionTime**|Set all admisstion time as zero.|
|**DischargeTime**|`unitdischargeoffset` in raw CSVs.|

|***`Prediction Label`***|***`(columns 4-31)`***|
|:---------------------|:-----------------|
|**Outcome**|In-hospital Mortality (binary classification). '1' represents the patient's death within the hospital.|
|**LOS**|Length of Stay. (days since admit)|
|**Decompensation**|Decompensation prediction (binary classification). We define the task as mortality prediction in the next 24 hours at each hour of an ICU stay. '1' represents the patient's death.|
|**Phenotype**|Phenotype Classification, multi-label classification task. `['Respiratory failure', 'Essential hypertension', 'Cardiac dysrhythmias', 'Fluid disorders', 'Septicemia', 'Acute and unspecified renal failure', 'Pneumonia', 'Acute cerebrovascular disease', 'CHF', 'CKD', 'COPD', 'Acute myocardial infarction', 'Gastrointestinal hem', 'Shock', 'lipid disorder', 'DM with complications', 'Coronary athe', 'Pleurisy', 'Other liver diseases', 'lower respiratory', 'Hypertension with complications', 'Conduction disorders', 'Complications of surgical', 'upper respiratory', 'DM without complication']`|

|***`Demographics`***|***`(columns 32-33)`***|
|:---------------------|:-----------------|
|**Sex**|Female (0) or Male (1)|
|**Age**|Age of Patients.|

|***`Lab tests`***|***`(columns 34-49)`***|
|:---------------------|:-----------------|
|**Categorical**|`["GCS Total", "Eyes", "Motor", "Verbal"]`|
|**Numerical**|`["admissionheight", "admissionweight", "Heart Rate", "MAP (mmHg)", "Invasive BP Diastolic", "Invasive BP Systolic", "O2 Saturation", "Respiratory Rate", "Temperature (C)", "glucose", "FiO2", "pH"]`|



