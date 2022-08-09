import json
import os
import pandas as pd
import cv2
from tqdm import tqdm
import argparse
from util import has_files
from pathlib import Path

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')

args = parser.parse_args()

ROOT_PATH = args.path_data  # ROOT_PATH = "D:/arxiv/CVPR_papers"
PARSED_DATA_PATH = os.path.join(ROOT_PATH, 'parsed')  # Already parsed by Grobid
PROCESSED_DATA_PATH = os.path.join(ROOT_PATH, 'paper2figure')
JSON_DIR = os.path.join(PROCESSED_DATA_PATH, 'json_data')
IMAGES_DIR = os.path.join(PROCESSED_DATA_PATH, 'figures')
OUT_PATH = 'output'


def main():
    data_list = []
    for paper in tqdm(os.listdir(JSON_DIR)):
        with open(os.path.join(JSON_DIR, paper)) as f:
            paper_data = json.load(f)
            if not paper_data:
                continue
            for fig_data in paper_data:
                data_list.append(fig_data)
    df = pd.DataFrame(data_list)
    df.to_excel('paper2fig.xlsx')

    # Split data in train and test
    import random
    random.shuffle(data_list)
    train_data = data_list[:int(len(data_list) * 0.8)]
    test_data = data_list[int(len(data_list) * 0.8):]

    # Save data
    with open(os.path.join(OUT_PATH, "train_data.json"), "w") as f:
        json.dump(train_data, f)
    with open(os.path.join(OUT_PATH, "test_data.json"), "w") as f:
        json.dump(test_data, f)

    print("Number of figures: ", len(data_list))


if __name__ == '__main__':
    main()
