import os
import json
import argparse
import pandas as pd
import numpy as np
import yaml
from tqdm import tqdm
import math


class TSDiscretizer:
    def __init__(self, timestep=1.0, config_path=os.path.join(os.path.dirname(__file__), 'resources/discretizer_config.json')):
        with open(config_path) as f:
            config = json.load(f)
            self._id_to_channel = config['id_to_channel']
            self._channel_to_id = dict(zip(self._id_to_channel, range(len(self._id_to_channel))))
            self._is_categorical_channel = config['is_categorical_channel']
            self._possible_values = config['possible_values']

        self._header = ["Hours"] + self._id_to_channel
        self._timestep = timestep

    def preprocess(self, X, header=None, end=None):
        if header is None:
            header = self._header
        assert header[0] == "Hours"
        eps = 1e-6

        N_channels = len(self._id_to_channel)
        x = X.values
        ts = [float(row[0]) for row in x]
        for i in range(len(ts) - 1):
            assert ts[i] < ts[i+1] + eps
        first_time = ts[0]
        if end is None:
            max_hours = max(ts) - first_time
        else:
            max_hours = end - first_time

        N_bins = int(max_hours / self._timestep + 1.0)

        cur_len = 0
        begin_pos = [0 for i in range(N_channels)]
        end_pos = [0 for i in range(N_channels)]
        for i in range(N_channels):
            channel = self._id_to_channel[i]
            begin_pos[i] = cur_len
            if self._is_categorical_channel[channel]:
                end_pos[i] = begin_pos[i] + len(self._possible_values[channel])
            else:
                end_pos[i] = begin_pos[i] + 1
            cur_len = end_pos[i]
        
        data = np.full([N_bins, cur_len], np.nan)

        def write(data, bin_id, channel, value, begin_pos):
            channel_id = self._channel_to_id[channel]
            if self._is_categorical_channel[channel]:
                category_id = self._possible_values[channel].index(value)
                N_values = len(self._possible_values[channel])
                one_hot = np.zeros((N_values,))
                one_hot[category_id] = 1
                for pos in range(N_values):
                    data[bin_id, begin_pos[channel_id] + pos] = one_hot[pos]
            else:
                data[bin_id, begin_pos[channel_id]] = float(value)

        for row in x:
            t = float(row[0]) - first_time
            if t > max_hours + eps:
                continue
            bin_id = int(t / self._timestep - eps)
            assert 0 <= bin_id < N_bins
            for j in range(1, len(row)):
                if row[j] == "":
                    continue
                channel = header[j]

                write(data, bin_id, channel, row[j], begin_pos)
        
        # create new header
        new_header = []
        for channel in self._id_to_channel:
            if self._is_categorical_channel[channel]:
                values = self._possible_values[channel]
                for value in values:
                    new_header.append(channel + "->" + value)
            else:
                new_header.append(channel)
        ts_df = pd.DataFrame(data, columns=new_header)
        ts_df.insert(0, "RecordTime", np.arange(math.ceil(first_time), math.ceil(first_time)+N_bins))

        return ts_df, new_header


def layout_csv(pid, n_episode, icustay, ts, stay, readmission):
    admission_time = stay[stay['stay_id'] == icustay]['intime'].values[0]
    discharge_time = stay[stay['stay_id'] == icustay]['outtime'].values[0]
    mortality = stay[stay['stay_id'] == icustay]['mortality_inhospital'].values[0]
    los = 24.0 * stay[stay['stay_id'] == icustay]['los'].values[0]
    sex = stay[stay['stay_id'] == icustay]['gender'].values[0]
    if sex in ['M', 'm']: 
        sex = 1
    else: 
        sex = 0
    age = stay[stay['stay_id'] == icustay]['anchor_age'].values[0]

    ts['PatientID'] = '{}_{}'.format(pid, n_episode)
    ts['AdmissionTime'] = admission_time
    ts['DischargeTime'] = discharge_time
    ts['Outcome'] = mortality
    ts['LOS'] = los - ts['RecordTime'].values
    ts['Readmission'] = readmission
    ts['Sex'] = sex
    ts['Age'] = age

    return ts


def get_pheno_definition(args):
    with open(args.phenotype_definitions) as definitions_file:
        definitions = yaml.safe_load(definitions_file)

    code_to_group = {}
    for group in definitions:
        codes = definitions[group]['codes']
        for code in codes:
            if code not in code_to_group:
                code_to_group[code] = group
            else:
                assert code_to_group[code] == group

    id_to_group = sorted(definitions.keys())
    group_to_id = dict((x, i) for (i, x) in enumerate(id_to_group))

    return definitions, code_to_group, id_to_group, group_to_id


def extract_to_csv(args, eps=1e-6, decom_future_time_interval=24.0):
    output_dir = args.output_path
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    definitions, code_to_group, id_to_group, group_to_id = get_pheno_definition(args)
    phneo_cols = [x for x in id_to_group
                  if definitions[x]['use_in_benchmark']]

    all_patient_ts = pd.DataFrame()
    patients = list(filter(str.isdigit, os.listdir(args.root_path)))
    for patient in tqdm(patients, desc='Iterating over patients'):
        patient_folder = os.path.join(args.root_path, patient)
        patient_ts_files = list(filter(lambda x: x.find("timeseries") != -1, os.listdir(patient_folder)))
        patient_ts_files = sorted(patient_ts_files, key=lambda x: int(x.split('_')[0].split('episode')[-1]))
        stay_df = pd.read_csv(os.path.join(patient_folder, "stays.csv"))
        
        for ts_filename in patient_ts_files:
            with open(os.path.join(patient_folder, ts_filename)) as tsfile:
                lb_filename = ts_filename.replace("_timeseries", "")
                n_episode = int(lb_filename.split('.')[0].split('episode')[-1])
                label_df = pd.read_csv(os.path.join(patient_folder, lb_filename))
                
                # empty label file
                if label_df.shape[0] == 0:
                    continue
                
                mortality = int(label_df.iloc[0]["Mortality"])
                los = 24.0 * label_df.iloc[0]['Length of Stay']
                if pd.isnull(los):
                    print("\n\t(length of stay is missing)", patient, ts_filename)
                    continue

                icustay = label_df.iloc[0]['Icustay']
                stay = stay_df[stay_df.stay_id == icustay]
                deathtime = pd.to_datetime(stay['deathtime'].iloc[0])
                intime = pd.to_datetime(stay['intime'].iloc[0])
                if pd.isnull(deathtime):
                    lived_time = 1e18
                else:
                    # conversion to pydatetime is needed to avoid overflow issues when subtracting
                    lived_time = (deathtime.to_pydatetime() - intime.to_pydatetime()).total_seconds() / 3600.0

                # readmission
                readmission = 0
                if n_episode < len(patient_ts_files):
                    outtime = np.datetime64(stay['outtime'].iloc[0])
                    readmit_intime = np.datetime64(stay_df.loc[n_episode, 'intime'])
                    if (readmit_intime - outtime).astype('timedelta64[D]') <= np.timedelta64(30, 'D'):
                        readmission = 1
                elif n_episode == len(patient_ts_files) and pd.notnull(deathtime):
                    outtime = np.datetime64(stay['outtime'].iloc[0])
                    deadtime = np.datetime64(stay['deathtime'].iloc[0])
                    if (deadtime - outtime).astype('timedelta64[D]') <= np.timedelta64(30, 'D'):
                        readmission = 1
                
                ts_lines = tsfile.read().splitlines()
                header = ts_lines[0]
                ts_lines = ts_lines[1:]
                event_times = [float(line.split(',')[0]) for line in ts_lines]

                ts_lines = [line for (line, t) in zip(ts_lines, event_times)
                            if -eps < t < los + eps]
                event_times = [t for t in event_times
                               if -eps < t < los + eps]
                
                # no measurements in ICU
                if len(ts_lines) == 0:
                    print("\n\t(no events in ICU) ", patient, ts_filename)
                    continue
                
                # time series
                ts_df = pd.DataFrame(columns=header.split(','))
                for i in range(len(ts_lines)):
                    ts_df.loc[i] = ts_lines[i].split(',')
                discretizer = TSDiscretizer()
                ts_df, new_header = discretizer.preprocess(ts_df)

                out_df = layout_csv(patient, n_episode, icustay, ts_df, stay_df, readmission)

                # decompensation
                sample_times = np.arange(0.0, min(los, lived_time) + eps)
                sample_times = list(filter(lambda x: x > event_times[0], sample_times))
                decom = []
                for t in sample_times:
                    if mortality == 0:
                        cur_mortality = 0
                    else:
                        cur_mortality = int(lived_time - t < decom_future_time_interval)
                    decom.append(cur_mortality)

                decom_df = pd.DataFrame({'PatientID': f'{patient}_{n_episode}', 'RecordTime': sample_times, 'Decompensation': 0})

                # phenotyping
                cur_labels = [0 for i in range(len(id_to_group))]
                diagnoses_df = pd.read_csv(os.path.join(patient_folder, "diagnoses.csv"),
                                           dtype={"icd_code": str})
                diagnoses_df = diagnoses_df[diagnoses_df.stay_id == icustay]
                for index, row in diagnoses_df.iterrows():
                    if row['USE_IN_BENCHMARK']:
                        code = row['icd_code']
                        if code in code_to_group:
                            group = code_to_group[code]
                            group_id = group_to_id[group]
                            cur_labels[group_id] = 1
                        else:
                            print(f'{code} code not found') 

                cur_labels = [x for (i, x) in enumerate(cur_labels)
                              if definitions[id_to_group[i]]['use_in_benchmark']]

                # merge four tasks data
                out_df = pd.merge(out_df, decom_df, how='left', on=['PatientID', 'RecordTime'])
                out_df[phneo_cols] = cur_labels
                all_patient_ts = pd.concat([all_patient_ts, out_df], ignore_index=True)
                
    # format the csv file
    basic_cols = ['PatientID', 'RecordTime', 'AdmissionTime', 'DischargeTime']
    task_cols = ['Outcome', 'LOS', 'Readmission', 'Decompensation'] + phneo_cols
    demo_cols = ['Sex', 'Age']
    # lab_cols = all_patient_ts.columns[len(demo_cols):]
    lab_cols = new_header
    cate_cols = [_ for _ in lab_cols if '->' in _]
    num_cols = [_ for _ in lab_cols if '->' not in _]
    columns = basic_cols + task_cols + demo_cols + cate_cols + num_cols
    all_patient_ehr = all_patient_ts[columns]
    all_patient_ehr.to_csv(os.path.join(output_dir, 'format_mimic4_ehr.csv'), index=False)


def main():
    parser = argparse.ArgumentParser(description="Create data for in-hospital mortality prediction task.")
    parser.add_argument('root_path', type=str, help="Path to root folder containing train and test sets.")
    parser.add_argument('output_path', type=str, help="Directory where the created data should be stored.")
    parser.add_argument('--phenotype_definitions', '-p', type=str,
                        default=os.path.join(os.path.dirname(__file__), './mimic3benchmark/resources/icd_9_10_definitions_2.yaml'),
                        help='YAML file with phenotype definitions.')
    args, _ = parser.parse_known_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    extract_to_csv(args)


if __name__ == '__main__':
    main()
