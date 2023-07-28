# Predicting Mortality /PhysioNet Challenge 2012 Datasets Information

source : https://github.com/alistairewj/challenge2012/tree/master

## Database Description

### Stats of Datasets

| Datasets | Number of patients | Number of Record |
| -------- | ------------------ | ---------------- |
| A        | 4000              | 299264           |
| B        | 4000              | 299068           |

### Data Modalities

- **EHR**

### Task

| ***`Task`***                         | ***`Description`***                                          |
| ------------------------------------ | ------------------------------------------------------------ |
| **In-hospital Mortality Prediction** | Predict in-hospital mortality based on the data collected during the first two days of an ICU stay. |
| **Length of Stay Prediction**        | Predict remaining days spent in ICU at each hour of stay.    |

## Dataset Building

1. Change the directory.

   ```
   cd challenge2012/
   ```

2. Download raw data from https://physionet.org/content/challenge-2012/1.0.0/

3. Create two folders `./raw`  and `./processed `. 

   ```
   mkdir raw
   mkdir processed
   ```

4. Put the downloaded and unzipped data folder `set-{a|b}` and file `Outcomes-{a|b}.txt` to the `./raw` folder.

5. Run preprocessing script `format_challange.py` for set A or set B (choose which type in `main()` function). The processed CSV dataset will be generated in `processed/` folder with name `challenge2012_seta.csv` or `challenge2012_setb.csv`

   ```
   python format_challenge.py
   ```

6. Apply normalization, imputation, outlier filtering, dataset splitting (7-1-2, train/val/test) process, and export the final dataset to `./processed` folder. Run `preprocess.ipynb`

**Set A is the official *training dataset* and Set B is the *test set*** mentioned in the Challenge 2012 website. We can only use set A to do various prediction tasks

## Formatted CSV File Description

| ID and Outcome-related Descriptors | columns | Descriptions                                                 |
| ---------------------------------- | ------- | ------------------------------------------------------------ |
| Record ID                          | 1       | a unique integer for each ICU stay                           |
| Timestamp                          | 2       | indicating the elapsed time of the observation since ICU admission in each case, in hours and minutes |
| Outcome                            | 3       | *In-hospital death* (0: survivor, or 1: died in-hospital)    |
| Survival(days)                     | 4       | If the patient's death was recorded (in or out of hospital), then *Survival* is the number of days between ICU admission and death; otherwise, *Survival* is assigned the value -1. |
| LOS(days)                          | 5       | *Length of stay* (days), the number of days between the patient's admission to the ICU and the end of hospitalization (including any time spent in the hospital after discharge from the ICU) |
| SOFA                               | 6       | a score related to prediction ([Ferreira et al., 2001](http://www.ncbi.nlm.nih.gov/pubmed/11594901)) |
| SAPS-I                             | 7       | a score related to prediction ([Le Gall et al., 1984](http://www.ncbi.nlm.nih.gov/pubmed/6499483)) |

*Survival* > *Length of stay* ⇒ Survivor
 	*Survival* = -1 ⇒ Survivor
 	2 ≤ *Survival* ≤ *Length of stay* ⇒ In-hospital death

| General Descriptors | columns | Descriptions                                                 |
| ------------------- | ------- | ------------------------------------------------------------ |
| Age                 | 8       | years                                                        |
| Sex                 | 9       | 0: female, or 1: male                                        |
| Height              | 10      | cm                                                           |
| ICUType             | 11      | 1: Coronary Care Unit, 2: Cardiac Surgery Recovery Unit, 3: Medical ICU, or 4: Surgical ICU |
| Weight              | 12      | kg, **may change in the following time like time series variables** |

| Time Series Variables                                        | Descriptions (36 variables)                      |
| ------------------------------------------------------------ | ------------------------------------------------------- |
| [*Albumin*](http://en.wikipedia.org/wiki/Human_serum_albumin) | g/dL                                                    |
| [*ALP*](http://en.wikipedia.org/wiki/Alkaline_phosphatase)   | Alkaline phosphatase (IU/L)                             |
| [*ALT*](http://en.wikipedia.org/wiki/Alanine_transaminase)   | Alanine transaminase (IU/L)                             |
| [*AST*](http://en.wikipedia.org/wiki/Aspartate_transaminase) | Aspartate transaminase (IU/L)                           |
| [*Bilirubin*](http://en.wikipedia.org/wiki/Bilirubin)        | mg/dL                                                   |
| [*BUN*](http://en.wikipedia.org/wiki/BUN)                    | Blood urea nitrogen (mg/dL)                             |
| [*Cholesterol*](http://en.wikipedia.org/wiki/Cholesterol)    | Serum creatinine (mg/dL)                                |
| [*DiasABP*](http://en.wikipedia.org/wiki/Diastolic_blood_pressure) | Invasive diastolic arterial blood pressure (mmHg)       |
| [*FiO2*](http://en.wikipedia.org/wiki/FIO2)                  | Fractional inspired O2 (0-1)                            |
| [*GCS*](http://en.wikipedia.org/wiki/Glasgow_coma_score)     | Glasgow Coma Score (3-15)                               |
| [*Glucose*](http://en.wikipedia.org/wiki/Serum_glucose)      | Serum glucose (mg/dL)                                   |
| [*HCO3*](http://en.wikipedia.org/wiki/Bicarbonate#Diagnostics) | Serum bicarbonate (mmol/L)                              |
| [*HCT*](http://en.wikipedia.org/wiki/Hematocrit)             | Hematocrit (%)                                          |
| [*HR*](http://en.wikipedia.org/wiki/Heart_rate)              | Heart rate (bpm)                                        |
| [*K*](http://en.wikipedia.org/wiki/Hypokalemia)              | Serum potassium (mEq/L)                                 |
| [*Lactate*](http://en.wikipedia.org/wiki/Lactic_acid)        | mmol/L                                                  |
| [*Mg*](http://en.wikipedia.org/wiki/Magnesium#Biological_role) | Serum magnesium (mmol/L)                                |
| [*MAP*](http://en.wikipedia.org/wiki/Mean_arterial_pressure) | Invasive mean arterial blood pressure (mmHg)            |
| [*MechVent*](http://en.wikipedia.org/wiki/Mechanical_ventilation) | Mechanical ventilation respiration (0:false, or 1:true) |
| [*Na*](http://en.wikipedia.org/wiki/Serum_sodium)            | Serum sodium (mEq/L)                                    |
| [*NIDiasABP*](http://en.wikipedia.org/wiki/Diastolic_blood_pressure) | Non-invasive diastolic arterial blood pressure (mmHg)   |
| [*NIMAP*](http://en.wikipedia.org/wiki/Mean_arterial_pressure) | Non-invasive mean arterial blood pressure (mmHg)        |
| [*NISysABP*](http://en.wikipedia.org/wiki/Systolic_blood_pressure) | Non-invasive systolic arterial blood pressure (mmHg)    |
| [*PaCO2*](http://en.wikipedia.org/wiki/Arterial_blood_gas)   | partial pressure of arterial CO2 (mmHg)                 |
| [*PaO2*](http://en.wikipedia.org/wiki/Arterial_blood_gas)    | Partial pressure of arterial O2 (mmHg)                  |
| [*pH*](http://en.wikipedia.org/wiki/Arterial_blood_gas)      | Arterial pH (0-14)                                      |
| [*Platelets*](http://en.wikipedia.org/wiki/Platelets)        | cells/nL                                                |
| [*RespRate*](http://en.wikipedia.org/wiki/Respiratory_physiology) | Respiration rate (bpm)                                  |
| [*SaO2*](http://en.wikipedia.org/wiki/Arterial_blood_gas)    | O2 saturation in hemoglobin (%)                         |
| [*SysABP*](http://en.wikipedia.org/wiki/Systolic_blood_pressure) | Invasive systolic arterial blood pressure (mmHg)        |
| [*Temp*](http://en.wikipedia.org/wiki/Normal_human_body_temperature) | Temperature (°C)                                        |
| [*TropI*](http://en.wikipedia.org/wiki/Troponin)             | Troponin-I (μg/L)                                       |
| [*TropT*](http://en.wikipedia.org/wiki/Troponin)             | Troponin-T (μg/L)                                       |
| [*Urine*](http://en.wikipedia.org/wiki/Fluid_balance)        | Urine output (mL)                                       |
| [*WBC*](http://en.wikipedia.org/wiki/Reference_ranges_for_blood_tests#Hematology) | White blood cell count (cells/nL)                       |

For details of time series variables, please see https://physionet.org/content/challenge-2012/1.0.0/

