import json
import os

import cv2
from tqdm import tqdm
import argparse
from util import has_files

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')

parser.add_argument('-plot', '--plot', type=bool, default=False, required=False,
                    help='Activate image plotting')

args = parser.parse_args()


def compute_processed_files(data_path):
    ids = []
    for pdf_dir in tqdm(os.listdir(data_path)):
        if has_files(os.path.join(data_path, pdf_dir)):
            ids.append(pdf_dir)
    return ids


def main():
    # Get constants
    plot_figures = args.plot
    ROOT_PATH = args.path_data  # ROOT_PATH = "D:/arxiv/CVPR_papers/pdf"
    PARSED_DATA_PATH = os.path.join(ROOT_PATH, 'parsed')
    PROCESSED_DATA_PATH = os.path.join(ROOT_PATH, 'paper2figure')
    # Create dir
    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH)

    OUT_PATH = 'output'

    # Remove downloaded ids from list
    print("Checking if you have any of the files already downloaded")
    processed_ids = compute_processed_files(PROCESSED_DATA_PATH)

    counter = 0
    data_list = []
    for pdf_dir in tqdm(os.listdir(PARSED_DATA_PATH)):
        parsed_pdf_dir = os.path.join(PARSED_DATA_PATH, pdf_dir)
        child = os.path.join(parsed_pdf_dir, os.listdir(parsed_pdf_dir)[0])

    #     for path in os.listdir(parsed_pdf_dir):
    #         if not path.endswith(".pdf"):
    #             # Open json file eith figures data
    #             try:  # This is if for some reason the json file is not there (To do: compute it from erro_filter.txt)
    #                 with open(os.path.join(parsed_pdf_dir, path, 'figures_metadata', path + ".json"), "r") as f:
    #                     data = json.load(f)
    #             except:
    #                 with open("error_filter.txt", "a") as f:
    #                     f.write(path + "\n")
    #                 continue
    #             # Read the captions and filter the ones that have a text of "method" or "model"
    #             for figure in data:
    #                 if figure['figType'] == "Figure":
    #
    #                     if "model architecture" in figure["caption"].lower() or "model diagram" in figure[
    #                         "caption"].lower() or "overview" in figure["caption"].lower() or "pipeline" in figure[
    #                         "caption"].lower():
    #                         if plot_figures:
    #                             print(figure['caption'])
    #                             im = cv2.imread(figure['renderURL'])
    #                             cv2.imshow('image', im)
    #                             cv2.waitKey(0)
    #                         # Retrieve data from paper related to figure
    #                         with open(os.path.join(parsed_pdf_dir, path, path + ".json"), "r") as f:
    #                             paper_data = json.load(f)
    #                         paper = {"paper_id": pdf_dir,
    #                                  "title": paper_data["title"],
    #                                  "authors": paper_data["authors"],
    #                                  "abstract": paper_data["abstract"],
    #                                  "sections": paper_data["sections"], }
    #                         data_list.append({
    #                             "figure_id": counter,
    #                             "figure_path": figure['renderURL'].split("CVPR_papers")[1],
    #                             "caption": figure['caption'],
    #                             "paper": paper
    #                         })
    #                         counter += 1
    #
    # # Split data in train and test
    # import random
    # random.shuffle(data_list)
    # train_data = data_list[:int(len(data_list) * 0.8)]
    # test_data = data_list[int(len(data_list) * 0.8):]
    #
    # # Save data
    # with open("train_data.json", "w") as f:
    #     json.dump(train_data, f)
    # with open("test_data.json", "w") as f:
    #     json.dump(test_data, f)
    #
    # print("Number of figures: ", counter)


if __name__ == '__main__':
    main()
