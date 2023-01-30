# File: construct_dataset.py
# Created by Juan A. Rodriguez on 02/11/2022
# Goal: (Step 4) - Perform the split of the dataset and store in train and val json files
# Output: At the end of this process you will have a directory 'json_data' with text pairs 
# and metadata for each figure in json format (on json per figure) 

import argparse
import json
import os
from tqdm import tqdm
import random

# Deprecated, merge from _rm version
# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')
args = parser.parse_args()

# TODO: Update this to use correct paths an logic from construct_dataset_rm.py

def main():
    ROOT_PATH = args.path_data
    PROCESSED_DATA_PATH = os.path.join(ROOT_PATH, 'paper2figure')
    JSON_DIR = os.path.join(PROCESSED_DATA_PATH, 'json_data')
    
    # Read individual json files and store in list
    data_list = []
    for paper in tqdm(os.listdir(JSON_DIR)):
        with open(os.path.join(JSON_DIR, paper)) as f:
            paper_data = json.load(f)
            if not paper_data:
                continue
            for fig_data in paper_data:
                data_list.append(fig_data)

    # Split data in train and test
    random.shuffle(data_list)
    train_data = data_list[:int(len(data_list) * 0.8)]
    test_data = data_list[int(len(data_list) * 0.8):]

    # Save data
    with open(os.path.join(PROCESSED_DATA_PATH, "train_data.json"), "w") as f:
        json.dump(train_data, f)
    with open(os.path.join(PROCESSED_DATA_PATH, "test_data.json"), "w") as f:
        json.dump(test_data, f)

if __name__ == '__main__':
    main()
