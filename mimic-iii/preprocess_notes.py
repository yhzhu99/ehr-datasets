import os
import json
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle


def diff(time1, time2):
    # compute time2-time1
    # return difference in hours
    a = np.datetime64(time1)
    b = np.datetime64(time2)
    return (a-b).astype('timedelta64[h]').astype(int)


class TextReader():
    def __init__(self, text_fixed_dir):
        self.text_path = text_fixed_dir
    
    def read_all_text(self, filename, intime, period_length=48.0, eps=1e-6):
        filepath = os.path.join(self.text_path, str(filename))
        with open(filepath, 'r') as f:
            d = json.load(f)
        all_time = sorted(d.keys())
        text = []
        time = []
        for t in all_time:
            if -eps < diff(t, intime) < period_length + eps:
                time.append(t)
                text.append(" ".join(d[t]))
        return time, text


def extract_to_csv(args, partition, eps=1e-6):
    output_dir = args.output_path
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    text_fixed_dir = os.path.join(args.root_path, f'{partition}_text_fixed')
    text_reader = TextReader(text_fixed_dir)
    filenames = os.listdir(text_fixed_dir)
    notes_df = pd.DataFrame(columns=['PatientID', 'Recordtime', 'AdmissionTime', 'DischargeTime', 'Text'])
    for filename in tqdm(filenames, desc='Iterating over notes in {}'.format(partition)):
        patient_id, episode_num = filename.split('_')[:2]
        if not episode_num.isdigit():
            continue
        patient_folder = os.path.join(args.root_path, partition, patient_id)
        episode_file = os.path.join(patient_folder, f'episode{episode_num}.csv')
        if not os.path.exists(episode_file):
            print(f'{patient_id}_episode{episode_num}_timeseries does not exist.')
            continue
        label_df = pd.read_csv(episode_file)
        # empty label file
        if label_df.shape[0] == 0:
            continue
        icustay = label_df.iloc[0]['Icustay']
        stay_df = pd.read_csv(os.path.join(patient_folder, "stays.csv"))

        intime = stay_df[stay_df['ICUSTAY_ID'] == icustay].iloc[0]['INTIME']
        outtime = stay_df[stay_df['ICUSTAY_ID'] == icustay].iloc[0]['OUTTIME']
        time, text = text_reader.read_all_text(filename, intime)
        text_df = pd.DataFrame({'PatientID': patient_id, 'Recordtime': time, 'AdmissionTime': intime, 
                                'DischargeTime': outtime, 'Text': text})
        notes_df = pd.concat([notes_df, text_df], ignore_index=True)
    
    notes_df.to_csv(os.path.join(output_dir, f"{partition}.csv"), index=False)
        

def main():
    parser = argparse.ArgumentParser(description="Create data for in-hospital mortality prediction task.")
    parser.add_argument('root_path', type=str, help="Path to root folder containing train and test sets.")
    parser.add_argument('output_path', type=str, help="Directory where the created data should be stored.")
    args, _ = parser.parse_known_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    extract_to_csv(args, "test")
    # extract_to_csv(args, "train")


if __name__ == '__main__':
    main()
