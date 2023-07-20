import pandas as pd
import os

def data_generate(origin_data_file_path):
    combined_data = pd.DataFrame()
    time_series_folder = origin_data_file_path

    for filename in os.listdir(time_series_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(time_series_folder, filename)
            # extract patient ID from files' names
            patient_id = int(filename[:-4])  

            with open(filepath, 'r') as file:
                file.readline()

                # read the data recorded at every timestamp
                variable_data = {}
                for line in file:
                    timestamp, parameter, value = line.strip().split(',')
                    if timestamp not in variable_data:
                        variable_data[timestamp] = {'RecordID': patient_id, 'Timestamp': timestamp}
                    variable_data[timestamp][parameter] = value

                    # 'Age', 'Gender', 'Height', 'ICUType' in every line as Patient's personal info
                    if parameter in ['Age', 'Gender', 'Height', 'ICUType']:
                        for ts in variable_data:
                            variable_data[ts][parameter] = value

            variable_data = pd.DataFrame(list(variable_data.values()))
            # df = df.groupby(['patientID','RecordTime'], dropna=True, as index = False) .mean()

            combined_data = combined_data.append(variable_data, ignore_index=True)

    # adjust the order of columns
    columns_order = ['RecordID', 'Timestamp', 'Age', 'Gender', 'Height', 'ICUType', 'Weight'] + sorted([col for col in combined_data.columns if col not in ['RecordID', 'Timestamp', 'Age', 'Gender', 'Height', 'ICUType', 'Weight']])
    combined_data = combined_data[columns_order]

    combined_data.to_csv('converted_data.csv', index=False)


    data = pd.read_csv('converted_data.csv')

    patient_info_dict = {}

    for index, row in data.iterrows():
        record_id = row['RecordID']
        age, gender, height, icu_type = row['Age'], row['Gender'], row['Height'], row['ICUType']
        if record_id not in patient_info_dict:
            patient_info_dict[record_id] = (age, gender, height, icu_type)

    for record_id, (age, gender, height, icu_type) in patient_info_dict.items():
        mask = data['RecordID'] == record_id
        data.loc[mask, ['Age', 'Gender', 'Height', 'ICUType']] = age, gender, height, icu_type

    data.to_csv('updated_dataset.csv', index=False)


def merge_with_outcomes(outcome_file_path):
    data = pd.read_csv('updated_dataset.csv')

    # merge the datasets and labels
    labels_file = outcome_file_path
    labels_data = pd.read_csv(labels_file)

    data_with_labels = pd.merge(data, labels_data, on='RecordID', how='left')

    # insert labels into original datasets
    insert_index = 2 
    for col in labels_data.columns[1:]:  
        data.insert(insert_index, col, data_with_labels[col])

    # adjust the names of some columns
    data = data.rename(columns={'In-hospital_death': 'Outcome'})
    data = data.rename(columns={'Length_of_stay': 'LOS'})
    data = data.rename(columns={'Gender': 'Sex'})


    data.to_csv('challenge_dataset_formatted_b.csv', index=False)
    

def main():
    origin_data_file_path = 'set-b'
    outcome_file_path = 'Outcomes-b.txt'

    data_generate(origin_data_file_path)
    merge_with_outcomes(outcome_file_path)

    os.remove('converted_data.csv')
    os.remove('updated_dataset.csv')

if __name__ == '__main__':
    main()