import pandas as pd
import os


def generate_df(data_path):
    dataframes  = []

    cnt = 0
    for filename in os.listdir(data_path):
        cnt += 1
        if cnt == 10: break
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

    # add LOS column to the dataframe, it is the remaining hour of the patient in the ICU, can be calculated through ICULOS column
    # each patient largest ICULOS - cur record ICULOS
    combined_data['LOS'] = combined_data.groupby('PatientID')['ICULOS'].transform(max) - combined_data['ICULOS']

    # add RecordTime column, it can be the same as ICULOS
    combined_data['RecordTime'] = combined_data['ICULOS']    

    # adjust the order and titles of some columns
    columns_ahead = ['PatientID', 'RecordTime', 'SepsisLabel', 'LOS', 'Gender', 'Age', 'HospAdmTime', 'Unit1', 'Unit2', 'ICULOS']
    columns_order = columns_ahead + [col for col in combined_data.columns if col not in columns_ahead]
    combined_data = combined_data[columns_order]

    combined_data = combined_data.rename(columns={'Gender': 'Sex'})
    combined_data = combined_data.rename(columns={'SepsisLabel': 'Outcome'})

    return combined_data

def main():
    df_a = generate_df(data_path='raw/training_setA')
    df_a.to_csv('./processed/sepsis_seta.csv', index=False)
    # df_b = generate_df(data_path='raw/training_setB')
    # df_b.to_csv('./processed/sepsis_setb.csv', index=False)

if __name__ == '__main__':
    main()