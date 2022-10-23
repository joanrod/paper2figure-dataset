from __future__ import annotations
import os
from tqdm import tqdm
import os
from tqdm import tqdm
import argparse

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


def main() -> None:
    counter = 0
    for paper in tqdm(os.listdir(PARSED_DATA_PATH)):
        try:
            pdf_dir = os.path.join(PARSED_DATA_PATH, paper)
            pdf_file_name = os.listdir(pdf_dir)[0]

            figures_dir = os.path.join(pdf_dir, pdf_file_name, 'figures')  # Open the dir inside (always one)
            for figure in os.listdir(figures_dir):
                counter += 1
        except:
            continue
    print(counter)

if __name__ == "__main__":
    main()
