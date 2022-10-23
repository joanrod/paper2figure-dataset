
import argparse
import os

from tqdm import tqdm
import matplotlib.pyplot as plt
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
    # Read txt files
    path = 'output'
    splits = ["train", "test"]
    list_samples = []
    for split in splits:

        with open(os.path.join(path, 'paper2fig1_img_' + split + ".txt"), "r") as f:
            data = f.read().splitlines()
        list_samples += data
    dict_year_count = {}
    [dict_year_count.setdefault(i, 0) for i in range(10, 23)]
    for p in tqdm(list_samples):
        yymm = p.split("/")[-1].split("v")[0].split(".")[0]
        yy = yymm[:2]
        dict_year_count[int(yy)] += 1
        # mm = yymm[2:]

    print(dict_year_count)
    plt.bar(*zip(*dict_year_count.items()))
    plt.xlabel("Year")
    plt.ylabel("number of figures")
    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
