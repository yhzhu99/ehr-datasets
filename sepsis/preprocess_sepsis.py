import pandas as pd
import os


def generate_dataset(data_file_path, set):
    combined_data = pd.DataFrame()
    psv_folder = data_file_path  

    for filename in os.listdir(psv_folder):
        if filename.endswith(".psv"):
            filepath = os.path.join(psv_folder, filename)
            data = pd.read_csv(filepath, sep='|', skipinitialspace=True)
            
            # get the ID and label
            patient_id = int(filename[1:7])
            sepsis_label = data['SepsisLabel'].values
            data['PatientID'] = patient_id
            data['SepsisLabel'] = sepsis_label

            combined_data = combined_data.append(data, ignore_index=True)

    # adjust the order and titles of some columns
    columns_order = ['PatientID', 'SepsisLabel', 'ICULOS', 'Gender', 'Age', 'HospAdmTime', 'Unit1', 'Unit2'] + [col for col in combined_data.columns if col not in ['PatientID', 'SepsisLabel', 'ICULOS', 'Gender', 'Age', 'HospAdmTime', 'Unit1', 'Unit2']]
    combined_data = combined_data[columns_order]

    combined_data = combined_data.rename(columns={'Gender': 'Sex'})
    combined_data = combined_data.rename(columns={'SepsisLabel': 'Outcome'})

    if set == 1:
        combined_data.to_csv('training_dataA.csv', index=False)
    else:
        combined_data.to_csv('training_dataB.csv', index=False)


def main():
    # Replace with your PSV folder path
    data_file_path1 = 'training_setA'
    generate_dataset(data_file_path1, set=1)

    data_file_path2 = 'training_setB'
    generate_dataset(data_file_path2, set=2)


if __name__ == '__main__':
    main()