from __future__ import absolute_import
from __future__ import print_function


import os
import numpy as np
import argparse
from data_extraction import utils
import pandas as pd


def data_extraction_mortality(args):
    period_length = args.period_length
    all_df = utils.embedding(args.root_dir)
    all_mort = utils.filter_mortality_data(all_df)
    all_mort = all_mort[all_mort['itemoffset']<=period_length]
    return all_mort


def main():
    parser = argparse.ArgumentParser(description="Create data for root")
    parser.add_argument('root_path', type=str, help="Path to root folder containing all_data.csv.")
    parser.add_argument('output_path', type=str, help="Directory where the processed data should be stored.")
    parser.add_argument('--period_length', type=int, default=48, help="The period length for the time series data")
    args, _ = parser.parse_known_args()

    data = data_extraction_mortality(args)
    data.to_csv(os.path.join(args.output_path, 'mortality.csv'), index=False)


if __name__ == '__main__':
    main()
