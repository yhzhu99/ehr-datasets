MIMIC-IV Benchmarks
=========================

We modified the repository [mimic3-benchmark](https://github.com/YerevaNN/mimic3-benchmarks) for [MIMIC-IV Clinical Database v2.2](https://www.physionet.org/content/mimiciv/2.2/). 

---

## Database Description

### Stats of MIMIC-III Clinical Database v1.4

|***`Number of patients`***|***`Number of Records`***|
|:------------------:|:-----------------:|
|33488|41637|


### Data Modalities

- **EHR**
- **Notes**

### Prediction Tasks

|***`Task`***|***`Description`***|
|:----|:-----------|
|**In-hospital Mortality Prediction**|Predict in-hospital mortality based on the first 48 hours of an ICU stay.|
|**Length of Stay Prediction**|Predict remaining time spent in ICU at each hour of stay.|
|**Decompensation prediction**|Predict whether the patient's health will rapidly deteriorate in the next 24 hours.|
|**Phenotype Classification**|Classify which of 25 acute care conditions are present in a given patient ICU stay record.|
|**30 Days Readmission**|Predict readmission after 30 days since discharge. (If a patient dies within 30 days from discharge date, then that visit is also marked as readmission.)|

## Building the Benchmark

### EHR Date preprocessing

Here are the required steps to build the benchmark. It assumes that you already have MIMIC-IV dataset (lots of CSV files) on the disk.

1. Change the directory.

       cd mimic-iv/
    
2. The following command takes MIMIC-III CSVs, generates one directory per `subject_id_` and writes ICU stay information to `data/{subject_id_}/stays.csv`, diagnoses to `data/{subject_id_}/diagnoses.csv`, and events to `data/{subject_id_}/events.csv`.

       python -m mimic3benchmark.scripts.extract_subjects {PATH TO MIMIC-IV CSVs} data/root/

3. The following command attempts to fix some issues (ICU stay ID is missing) and removes the events that have missing information.

       python -m mimic3benchmark.scripts.validate_events data/root/

4. The next command breaks up per-subject data into separate episodes (pertaining to ICU stays). Time series of events are stored in ```{SUBJECT_ID}/episode{#}_timeseries.csv``` (where # counts distinct episodes) while episode-level information (patient age, gender, ethnicity, height, weight) and outcomes (mortality, length of stay, diagnoses) are stores in ```{SUBJECT_ID}/episode{#}.csv```. This script requires two files, one that maps event ITEMIDs to clinical variables and another that defines valid ranges for clinical variables (for detecting outliers, etc.).

       python -m mimic3benchmark.scripts.extract_episodes_from_subjects data/root/
	
5. The following commands will generate formatted EHR csv file, which contains basic information of patiens, lables of prediction tasks and time series data. It will be stored in `data/processed/ehr/format_mimic4_ehr.csv`.

       python -m preprocess_mimic4 data/root/ data/processed/ehr/


## Formatted CSV File Description

|***`Basic Information`***|***`(columns 0-3)`***|
|:---------------------|:-----------------|
|**PatientID**|`subject_id_{#}` (where # counts distinct episodes) |
|**RecordTime**|Relative time of the record since `intime`. (hours since admit)|
|**AdmissionTime**|`intime` in raw CSVs.|
|**DischargeTime**|`outtime` in raw CSVs.|

|***`Prediction Label`***|***`(columns 4-32)`***|
|:---------------------|:-----------------|
|**Outcome**|In-hospital Mortality. '1' represents the patient's death within the hospital.|
|**LOS**|Length of Stay. (hours since `intime`)|
|**Readmission**|30 Days Radmission. (30 days after `OUTTIME`)|
|**Decompensation**|Decompensation prediction. We define the task as mortality prediction in the next 24 hours at each hour of an ICU stay. '1' represents the patient's death.|
|**Phenotype**|Phenotype Classification, multi-label classification task. `'Acute and unspecified renal failure', 'Acute cerebrovascular disease', 'Acute myocardial infarction', 'Cardiac dysrhythmias', 'Chronic kidney disease', 'Chronic obstructive pulmonary disease and bronchiectasis', 'Complications of surgical procedures or medical care', 'Conduction disorders', 'Congestive heart failure; nonhypertensive', 'Coronary atherosclerosis and other heart disease', 'Diabetes mellitus with complications', 'Diabetes mellitus without complication', 'Disorders of lipid metabolism', 'Essential hypertension', 'Fluid and electrolyte disorders', 'Gastrointestinal hemorrhage', 'Hypertension with complications and secondary hypertension', 'Other liver diseases', 'Other lower respiratory disease', 'Other upper respiratory disease', 'Pleurisy; pneumothorax; pulmonary collapse', 'Pneumonia (except that caused by tuberculosis or sexually transmitted disease)', 'Respiratory failure; insufficiency; arrest (adult)', 'Septicemia (except in labor)', 'Shock'`|

|***`Demographics`***|***`(columns 33-34)`***|
|:---------------------|:-----------------|
|**Sex**|Female (0) or Male (1)|
|**Age**|Age of Patiens.|

|***`Laboratory Features`***|***`(columns 35-93)`***|
|:---------------------|:-----------------|
|**Categorical**|`["Capillary refill rate", "Glascow coma scale eye opening", "Glascow coma scale motor response", "Glascow coma scale total", "Glascow coma scale verbal response"]`|
|**Numerical**|`["Diastolic blood pressure", "Fraction inspired oxygen", "Glucose", "Heart Rate", "Height", "Mean blood pressure", "Oxygen saturation", "Respiratory rate", "Systolic blood pressure", "Temperature", "Weight", "pH"]`|
