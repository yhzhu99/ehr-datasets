import pandas as pd
import os

def data_generate(data_path):
    dataframes  = []

    for filename in os.listdir(data_path):
        print("[Processing file:]", filename)
        if filename.endswith(".txt"):
            filepath = os.path.join(data_path, filename)
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

            dataframes.append(variable_data)
    combined_data = pd.concat(dataframes, ignore_index=True)

    # adjust the order of columns
    columns_order = ['RecordID', 'Timestamp', 'Age', 'Gender', 'Height', 'ICUType', 'Weight'] + sorted([col for col in combined_data.columns if col not in ['RecordID', 'Timestamp', 'Age', 'Gender', 'Height', 'ICUType', 'Weight']])
    data = combined_data[columns_order]

    patient_info_dict = {}
    for index, row in data.iterrows():
        print("[Current row:]", row)
        record_id = row['RecordID']
        age, gender, height, icu_type = row['Age'], row['Gender'], row['Height'], row['ICUType']
        if record_id not in patient_info_dict:
            patient_info_dict[record_id] = (age, gender, height, icu_type)

    for record_id, (age, gender, height, icu_type) in patient_info_dict.items():
        print("[Current RecordID:]", record_id)
        mask = data['RecordID'] == record_id
        data.loc[mask, ['Age', 'Gender', 'Height', 'ICUType']] = age, gender, height, icu_type

    return data


def merge_with_outcomes(feat_df, outcome_df):
    data = feat_df

    # merge the features and labels
    labels_data = outcome_df

    data_with_labels = pd.merge(data, labels_data, on='RecordID', how='left')

    # insert labels into original datasets
    insert_index = 2 
    for col in labels_data.columns[1:]:  
        data.insert(insert_index, col, data_with_labels[col])

    # adjust the names of some columns
    data = data.rename(columns={'In-hospital_death': 'Outcome'})
    data = data.rename(columns={'Length_of_stay': 'LOS'})
    data = data.rename(columns={'Gender': 'Sex'})

    return data
    

def main():
    feat_df = data_generate(data_path='./raw/set-a')
    outcome_df = pd.read_csv('./raw/Outcomes-a.txt')
    all_df = merge_with_outcomes(feat_df, outcome_df)
    all_df.to_csv('./processed/challenge2012_seta.csv')

if __name__ == '__main__':
    main()