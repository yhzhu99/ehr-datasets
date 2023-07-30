import os
import argparse
import numpy as np
import pandas as pd
from data_extraction import utils


label_pheno = ['Respiratory failure', 'Essential hypertension',
               'Cardiac dysrhythmias', 'Fluid disorders', 'Septicemia',
               'Acute and unspecified renal failure', 'Pneumonia',
               'Acute cerebrovascular disease', 'CHF', 'CKD', 'COPD',
               'Acute myocardial infarction', "Gastrointestinal hem",
               'Shock', 'lipid disorder', 'DM with complications', 'Coronary athe',
               'Pleurisy', 'Other liver diseases', 'lower respiratory',
               'Hypertension with complications', 'Conduction disorders',
               'Complications of surgical', 'upper respiratory',
               'DM without complication']


def extraction_phenotyping_label(args, all_df):
    diag_ord_col = ["patientunitstayid", "itemoffset", "Respiratory failure", "Fluid disorders",
                    "Septicemia", "Acute and unspecified renal failure", "Pneumonia",
                    "Acute cerebrovascular disease",
                    "Acute myocardial infarction", "Gastrointestinal hem", "Shock", "Pleurisy",
                    "lower respiratory", "Complications of surgical", "upper respiratory",
                    "Hypertension with complications", "Essential hypertension", "CKD", "COPD",
                    "lipid disorder", "Coronary athe", "DM without complication",
                    "Cardiac dysrhythmias",
                    "CHF", "DM with complications", "Other liver diseases", "Conduction disorders"]
    
    diag_columns = ['patientunitstayid', 'itemoffset', 'Respiratory failure', 'Essential hypertension', 'Cardiac dysrhythmias',
                    'Fluid disorders', 'Septicemia', 'Acute and unspecified renal failure', 'Pneumonia',
                    'Acute cerebrovascular disease', 'CHF', 'CKD', 'COPD', 'Acute myocardial infarction', "Gastrointestinal hem",
                    'Shock', 'lipid disorder', 'DM with complications', 'Coronary athe', 'Pleurisy', 'Other liver diseases', 'lower respiratory',
                    'Hypertension with complications', 'Conduction disorders', 'Complications of surgical', 'upper respiratory',
                    'DM without complication']
    
    diag = utils.read_diagnosis_table(args.eicu_dir)
    diag = utils.diag_labels(diag)
    diag.dropna(how='all', subset=label_pheno, inplace=True)

    stay_diag = set(diag['patientunitstayid'].unique())
    stay_all = set(all_df.patientunitstayid.unique())
    stay_intersection = stay_all.intersection(stay_diag)
    stay_pheno = list(stay_intersection)

    diag = diag[diag['patientunitstayid'].isin(stay_pheno)]
    diag.rename(index=str, columns={"diagnosisoffset": "itemoffset"}, inplace=True)
    diag = diag[diag_columns]
    label = diag.groupby('patientunitstayid').sum()
    label = label.reset_index()
    label[label_pheno] = np.where(label[label_pheno] >= 1, 1, label[label_pheno])
    all_pheno = all_df[all_df["patientunitstayid"].isin(stay_pheno)]
    label = label[diag_ord_col]
    all_pheno_label = label[label.patientunitstayid.isin(list(all_pheno.patientunitstayid.unique()))]

    return all_pheno_label


def extract_to_csv(args):
    all_df = utils.embedding(args.root_path)

    # Mortality + Length of Stay + Decompensation
    all_mort_los_decom = utils.filter_out_data(all_df)

    # Phenotyping
    all_pheno_label = extraction_phenotyping_label(args, all_mort_los_decom)

    all_out = pd.merge(all_mort_los_decom, all_pheno_label, on='patientunitstayid', how='left')

    all_out.rename(columns={'patientunitstayid': 'PatientID', 'itemoffset_x': 'RecordTime',
                            'unitdischargeoffset': 'DischargeTime',
                            'hospitaldischargestatus': 'Outcome', 'RLOS': 'LOS',
                            'unitdischargestatus': 'Decompensation',
                            'gender': 'Sex', 'age': 'Age'},
                   inplace=True)
    
    all_out.insert(2, 'AdmissionTime', 0)

    cols = all_out.columns.tolist()
    decom_index = cols.index('Decompensation')
    pheno_index = cols.index('itemoffset_y')
    cols = cols[:decom_index+1] + label_pheno + cols[decom_index+1:pheno_index]

    all_out = all_out[cols]

    return all_out


def main():
    parser = argparse.ArgumentParser(description="Create data for root")
    parser.add_argument('eicu_dir', type=str, help="Path to root folder containing all the patietns data")
    parser.add_argument('root_path', type=str, help="Path to root folder containing all_data.csv.")
    parser.add_argument('out_path', type=str, help="Path to store formatted dataset.csv")
    args, _ = parser.parse_known_args()
    
    data = extract_to_csv(args)
    data.to_csv(os.path.join(args.root_path, 'format_eICU.csv'), index=False)


if __name__ == '__main__':
    main()
