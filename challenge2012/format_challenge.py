import pandas as pd
import os

def generate_df(data_path):
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

            variable_data = pd.DataFrame(list(variable_data.values()))
            # df = df.groupby(['patientID','RecordTime'], dropna=True, as index = False).mean()

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

    data['RecordID'] = data['RecordID'].astype(str)
    return data


def merge_with_outcomes(feat_df, outcome_df):
    data = feat_df
    # merge the features and labels
    labels_data = outcome_df

    data_with_labels = pd.merge(data, labels_data, on='RecordID', how='left')

    # insert labels into original datasets
    insert_index = 2
    prediction_targets = labels_data.columns[1:]
    for col in prediction_targets:
        data.insert(insert_index, col, data_with_labels[col])

    data['Height'] = data['Height'].astype(float)
    # replace -1 value in Height column with NaN in data dataframe
    data['Height'] = data['Height'].replace(-1, float('nan'))
    print(data['Height'])

    # adjust the names of some columns
    data = data.rename(columns={'RecordID': 'PatientID'})
    data = data.rename(columns={'Timestamp': 'RecordTime'})
    data = data.rename(columns={'In-hospital_death': 'Outcome'})
    data = data.rename(columns={'Length_of_stay': 'LOS'})
    data = data.rename(columns={'Gender': 'Sex'})

    # fill the static demographic features for each patient's records
    data[['Sex', 'Age', 'ICUType']] = data.groupby(['PatientID'])[['Sex', 'Age', 'ICUType']].ffill()

    return data
    

def main():
    set_type = 'a' # 'a' or 'b'
    feat_df = generate_df(data_path=f'./raw/set-{set_type}')
    outcome_df = pd.read_csv(f'./raw/Outcomes-{set_type}.txt')
    outcome_df['RecordID'] = outcome_df['RecordID'].astype(str)
    all_df = merge_with_outcomes(feat_df, outcome_df)
    all_df.to_csv(f'./processed/challenge2012_set{set_type}.csv', index=False)


if __name__ == '__main__':
    main()