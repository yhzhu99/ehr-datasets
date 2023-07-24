import pandas as pd
import os


def generate_df(data_path):
    dataframes  = []

    for filename in os.listdir(data_path):
        print("[Processing file:]", filename)
        if filename.endswith(".psv"):
            filepath = os.path.join(data_path, filename)
            data = pd.read_csv(filepath, sep='|', skipinitialspace=True)
            
            # get the ID and label
            patient_id = str(filename[1:7])
            sepsis_label = data['SepsisLabel'].values
            data['PatientID'] = patient_id
            data['SepsisLabel'] = sepsis_label

            dataframes.append(data)
    combined_data = pd.concat(dataframes, ignore_index=True)

    # adjust the order and titles of some columns
    columns_order = ['PatientID', 'SepsisLabel', 'ICULOS', 'Gender', 'Age', 'HospAdmTime', 'Unit1', 'Unit2'] + [col for col in combined_data.columns if col not in ['PatientID', 'SepsisLabel', 'ICULOS', 'Gender', 'Age', 'HospAdmTime', 'Unit1', 'Unit2']]
    combined_data = combined_data[columns_order]

    combined_data = combined_data.rename(columns={'Gender': 'Sex'})
    combined_data = combined_data.rename(columns={'SepsisLabel': 'Outcome'})
    
    return combined_data

def main():
    df_a = generate_df(data_path='raw/training_setA')
    df_a.to_csv('./processed/sepsis_seta.csv', index=False)
    df_b = generate_df(data_path='raw/training_setB')
    df_b.to_csv('./processed/sepsis_setb.csv', index=False)

if __name__ == '__main__':
    main()