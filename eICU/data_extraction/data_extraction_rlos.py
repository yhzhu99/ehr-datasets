from __future__ import absolute_import
from __future__ import print_function


import os
import numpy as np
import argparse
from data_extraction import utils


def data_extraction_rlos(args):
    all_df = utils.embedding(args.root_path)
    all_los = utils.filter_rlos_data(all_df)
    return all_los



def main():
    parser = argparse.ArgumentParser(description="Create data for root")
    parser.add_argument('root_path', type=str, help="Path to root folder containing all_data.csv.")
    parser.add_argument('output_path', type=str, help="Directory where the processed data should be stored.")
    args, _ = parser.parse_known_args()

    data = data_extraction_rlos(args)
    data.to_csv(os.path.join(args.output_path, 'rlos.csv'), index=False)


if __name__ == '__main__':
    main()
