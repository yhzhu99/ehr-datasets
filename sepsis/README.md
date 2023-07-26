# Predicting Sepsis / PhysioNet Challenge 2019 Datasets Information

Source:	https://physionet.org/content/challenge-2019/1.0.0/

## Database Description

### Stats of Datasets

| Datasets | Number of patients | Number of Record |
| -------- | ------------------ | ---------------- |
| A        | 20336              | 790215           |
| B        | 20000              | 761995           |

### Data Modalities

- **EHR**

### Task

- The goal of this Challenge is the early detection of sepsis using physiological data.

- Participants need to **predict sepsis 6 hours before the clinical prediction of sepsis**.

- Algorithms **based only on the clinical data provided**, automatically identify a patient's risk of sepsis and **make a positive or negative prediction of sepsis for every time interval**.

| ***`Task`***                  | ***`Description`***                                          |
| ----------------------------- | ------------------------------------------------------------ |
| **Sepsis Prediction**         | Predict a patient's risk of sepsis for every time interval. |
| **Length of Stay Prediction**        | Predict remaining days spent in ICU at each hour of stay.    |

### Columns in each training data file

| ID and Label             | (columns 1-3)                                                |
| ------------------------ | ------------------------------------------------------------ |
| PatientID               |                                                              |
| **Outcome(SepsisLabel)** | For sepsis patients, `SepsisLabel` is 1 if $t≥t_{sepsis}−6$ , and 0 if $t<t_{sepsis}−6$. For non-sepsis patients, `SepsisLabel` is 0. |
| **LOS**       | remaining days spent in ICU |

| Demographics | (columns 4-8)                                 |
| ------------ | --------------------------------------------- |
| Sex          | Female (0) or Male (1)                        |
| Age          | Years (100 for patients 90 or above)          |
| HospAdmTime  | Hours between hospital admit and ICU admit    |
| Unit1        | Administrative identifier for ICU unit (MICU) |
| Unit2        | Administrative identifier for ICU unit (SICU) |
| ICULOS       | ICU length-of-stay (**hours since ICU admit**)|

| Vital signs | col (9-16)                            |
| ----------- | ------------------------------------- |
| HR          | Heart rate (beats per minute)         |
| O2Sat       | Pulse oximetry (%)                    |
| Temp        | Temperature (Deg C)                   |
| SBP         | Systolic BP (mm Hg)                   |
| MAP         | Mean arterial pressure (mm Hg)        |
| DBP         | Diastolic BP (mm Hg)                  |
| Resp        | Respiration rate (breaths per minute) |
| EtCO2       | End tidal carbon dioxide (mm Hg)      |

| Laboratory values | (columns 17-42)                                              |
| ----------------- | ------------------------------------------------------------ |
| BaseExcess        | Measure of excess bicarbonate (mmol/L)                       |
| HCO3              | Bicarbonate (mmol/L)                                         |
| FiO2              | Fraction of inspired oxygen (%)                              |
| pH                | N/A                                                          |
| PaCO2             | Partial pressure of carbon dioxide from arterial blood (mm Hg) |
| SaO2              | Oxygen saturation from arterial blood (%)                    |
| AST               | Aspartate transaminase (IU/L)                                |
| BUN               | Blood urea nitrogen (mg/dL)                                  |
| Alkalinephos      | Alkaline phosphatase (IU/L)                                  |
| Calcium           | (mg/dL)                                                      |
| Chloride          | (mmol/L)                                                     |
| Creatinine        | (mg/dL)                                                      |
| Bilirubin_direct  | Bilirubin direct (mg/dL)                                     |
| Glucose           | Serum glucose (mg/dL)                                        |
| Lactate           | Lactic acid (mg/dL)                                          |
| Magnesium         | (mmol/dL)                                                    |
| Phosphate         | (mg/dL)                                                      |
| Potassium         | (mmol/L)                                                     |
| Bilirubin_total   | Total bilirubin (mg/dL)                                      |
| TroponinI         | Troponin I (ng/mL)                                           |
| Hct               | Hematocrit (%)                                               |
| Hgb               | Hemoglobin (g/dL)                                            |
| PTT               | partial thromboplastin time (seconds)                        |
| WBC               | Leukocyte count (count*10^3/µL)                              |
| Fibrinogen        | (mg/dL)                                                      |
| Platelets         | (count*10^3/µL)                                              |

## Dataset Building

1. Change the directory

   ```
   cd sepsis/
   ```

2. Download raw data from https://physionet.org/content/challenge-2019/1.0.0/

3. Create two folders `./raw`  and `./processed `. 

   ```
   mkdir raw
   mkdir processed
   ```

4. Put the downloaded folder `sepsis/challenge-2019/1.0.0/training/training_set{A|B}` to the `./raw` folder. Both set A and set B have patient files like `p${PatientID}.psv`.

5. Run `preprocess_sepsis.py`, it will generate two csv files `sepsis_seta.csv` and `sepsis_setb.csv` in `./processed` folder.

   ```
   python preprocess_sepsis.py
   ```

Set A and set B share the same data format, these two sets are from two hospital systems which published by the Challenge for training.
