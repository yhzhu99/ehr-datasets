MIMIC-III Benchmarks
=========================

The code is based on repository [mimic3-benchmark](https://github.com/YerevaNN/mimic3-benchmarks) and [ClinicalNotesICU](https://github.com/kaggarwal/ClinicalNotesICU) for [MIMIC-III Clinical Database v1.4](https://physionet.org/content/mimiciii/1.4/).

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

## Building the Benchmark

### EHR Data Preprocessing

Here are the required steps to build the benchmark. It assumes that you already have MIMIC-III dataset (lots of CSV files) on the disk.

1. Change the directory.

       cd mimic-iii/
    
2. The following command takes MIMIC-III CSVs, generates one directory per `SUBJECT_ID` and writes ICU stay information to `data/{SUBJECT_ID}/stays.csv`, diagnoses to `data/{SUBJECT_ID}/diagnoses.csv`, and events to `data/{SUBJECT_ID}/events.csv`.

       python -m mimic3benchmark.scripts.extract_subjects {PATH TO MIMIC-III CSVs} data/root/

3. The following command attempts to fix some issues (ICU stay ID is missing) and removes the events that have missing information. About 80% of events remain after removing all suspicious rows (more information can be found in [`mimic3benchmark/scripts/more_on_validating_events.md`](mimic3benchmark/scripts/more_on_validating_events.md)).

       python -m mimic3benchmark.scripts.validate_events data/root/

4. The next command breaks up per-subject data into separate episodes (pertaining to ICU stays). Time series of events are stored in ```{SUBJECT_ID}/episode{#}_timeseries.csv``` (where # counts distinct episodes) while episode-level information (patient age, gender, ethnicity, height, weight) and outcomes (mortality, length of stay, diagnoses) are stores in ```{SUBJECT_ID}/episode{#}.csv```. This script requires two files, one that maps event ITEMIDs to clinical variables and another that defines valid ranges for clinical variables (for detecting outliers, etc.). **Outlier detection is disabled in the current version**.

       python -m mimic3benchmark.scripts.extract_episodes_from_subjects data/root/
	
5. The following commands will generate formatted EHR csv file, which contains basic information of patiens, lables of prediction tasks and time series data. It will be stored in `data/processed/ehr/mimic3_ehr_dataset_formatted.csv`.

       python -m preprocess_mimic3 data/root/ data/processed/ehr/

## Notes Data Preprocessing

1. The following commands will generate one directory per `SUBJECT_ID` and extract the notes dictionary in it.

       python -m scripts.extract_notes {PATH TO MIMIC-III CSVs} data/root/

2. The following commands will generate formatted notes csv file, which contains basic information of patiens and notes in first 48 hours of an ICU stay. It will be stored in `data/processed/ehr/mimic4_notes_dataset_formatted.csv`.

       python -m preprocess_notes data/root/ data/processed/notes/


## Formatted CSV File Description

|***`Basic Information`***|***`(columns 0-3)`***|
|:---------------------|:-----------------|
|**PatientID**|`SUBJECT_ID_{#}` (where # counts distinct episodes) |
|**RecordTime**|Relative time of the record since `INTIME`. (hours since admit)|
|**AdmissionTime**|`INTIME` in raw CSVs.|
|**DischargeTime**|`OUTTIME` in raw CSVs.|
|***`Prediction Label`***|***`(columns 4-31)`***|
|**Outcome**|In-hospital Mortality. '1' represents the patient's death within the hospital.|
|**LOS**|Length of Stay. (hours since `INTIME`)|
|**Decompensation**|Decompensation prediction. We define the task as mortality prediction in the next 24 hours at each hour of an ICU stay. '1' represents the patient's death.|
|**Phenotype**|Phenotype Classification. The specific 25 conditions can be found in `mimic3benchmark/resources/hcup_ccs_2015_definitions.yaml`. |
|***`Demographics`***|***`(columns 32-33)`***|
|**Sex**|Female (0) or Male (1)|
|**Age**|Age of Patiens.|
|***`Laboratory Features`***|***`(columns 34-92)`***|
|**Categorical**|["Capillary refill rate" (cols 34-35),<br>&nbsp;"Glascow coma scale eye opening" (cols 36-43),<br>&nbsp;"Glascow coma scale motor response" (cols 44-55),<br>&nbsp;"Glascow coma scale total" (cols 56-68),<br>&nbsp;"Glascow coma scale verbal response" (cols 69-80)]|
|**Numerical**|(cols 81-92)<br>["Diastolic blood pressure",<br>&nbsp;"Fraction inspired oxygen",<br>&nbsp;"Glucose",<br>&nbsp;"Heart Rate",<br>&nbsp;"Height",<br>&nbsp;"Mean blood pressure",<br>&nbsp;"Oxygen saturation",<br>&nbsp;"Respiratory rate",<br>&nbsp;"Systolic blood pressure",<br>&nbsp;"Temperature",<br>&nbsp;"Weight",<br>&nbsp;"pH"]|