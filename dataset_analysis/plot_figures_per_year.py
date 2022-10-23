import argparse
import os
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

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

    labels, values = zip(*dict_year_count.items())
    labels = [f'20{l}' if l is not 22 else f'April\n 20{l}' for l in labels]

    sns.set_style({'font.family': 'serif'})
    sns.set(font_scale=4)
    ax = sns.barplot(x=list(labels), y=list(values), color='gray')
    # ax.set(xlabel="Year", ylabel='Number of figures')
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Number of figures', fontsize=15)
    plt.setp(ax.get_xticklabels(), rotation=45, fontsize=13)
    plt.setp(ax.get_yticklabels(), fontsize=13)
    plt.yticks(range(0, max(values), 5000))
    plt.show()


if __name__ == "__main__":
    main()
