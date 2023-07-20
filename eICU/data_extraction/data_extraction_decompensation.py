from __future__ import absolute_import
from __future__ import print_function


import os
import numpy as np
import argparse
from data_extraction import utils


def data_extraction_decompensation(args):
    all_df = utils.embedding(args.output_dir)
    all_dec = utils.filter_decom_data(all_df)
    all_dec = utils.label_decompensation(all_dec)
    return all_dec


def main():
    parser = argparse.ArgumentParser(description="Create data for root")
    parser.add_argument('output_dir', type=str, help="Path to root folder containing all_data.csv.")
    args, _ = parser.parse_known_args()

    data = data_extraction_decompensation(args)
    data.to_csv(os.path.join(args.output_dir, 'decompensation.csv'), index=False)


if __name__ == '__main__':
    main()
