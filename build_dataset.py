import json
import os

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


def compute_processed_files(data_path):
    ids = []
    for paper in tqdm(os.listdir(data_path)):
        ids.append(paper + '.json')
    return ids


def validate_reference(ref, paragraph):
    # Avoid not allowed chars after the Fig reference
    not_allowed_chars_after_ref = ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                                   "0"]  # Find case where "Fig 1", and "Fig 11"
    try:
        next_char = paragraph[paragraph.find(ref) + len(ref)]
    except:
        return True
    return not any(next_char == c for c in not_allowed_chars_after_ref)


def retrieve_text_for_figure(figure, paper):
    captions = []

    # Get figure number
    figure_num = figure['name']

    # Prepare strings to look in the paper referencing this figure
    figure_names = [f'fig {figure_num}', f'fig. {figure_num}',
                    f'fig{figure_num}', f'fig.{figure_num}',
                    f'figure {figure_num}', f'figure. {figure_num}',
                    f'figure{figure_num}', f'figure.{figure_num}', f'figure . {figure_num}']

    # Prepare paper text
    for section in paper['sections']:
        section_text = section['text']

        # Split in paragraphs, using \n
        paragraphs = section_text.split('\n')
        for p in paragraphs:
            if any(validate_reference(name, p.lower()) if name in p.lower() else False for name in figure_names):
                captions.append(p)

    return captions


def main():
    # Get constants
    plot_figures = False
    ROOT_PATH = args.path_data  # ROOT_PATH = "D:/arxiv/CVPR_papers/pdf"
    PARSED_DATA_PATH = os.path.join(ROOT_PATH, 'parsed')
    PDF_DATA_PATH = os.path.join(ROOT_PATH, 'pdf')
    PROCESSED_DATA_PATH = os.path.join(ROOT_PATH, 'paper2figure')
    # Create dir
    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH)

    OUT_PATH = 'output'

    # Remove downloaded ids from list
    print("Checking if you have any of the files already downloaded")
    processed_ids = compute_processed_files(PROCESSED_DATA_PATH)

    # Define text filters over caption # TODO: Store this in a file, this is ugly
    text_filters = [
        'model architecture', 'architecture', 'model diagram', 'overview', 'pipeline',
        'flowchart', 'illustration', 'proposed method', 'framework', 'schem',
        'network structure', 'network diagram', 'outline']

    text_avoid = ['exampl', 'exampl', 'table', 'architectures']

    count_texts = 0
    counter = 0
    data_list = []
    for pdf_dir_name in tqdm(os.listdir(PARSED_DATA_PATH)):

        if pdf_dir_name in processed_ids:
            continue

        pdf_dir = os.path.join(PARSED_DATA_PATH, pdf_dir_name)
        pdf_file_name = os.listdir(pdf_dir)[0]

        parsed_pdf_dir = os.path.join(pdf_dir, pdf_file_name)  # Open the dir inside (always one)

        # Load json file regarding figures
        try:  # if for some reason the json file is not there
            with open(os.path.join(parsed_pdf_dir, 'figures_metadata', pdf_file_name + ".json"), "r") as f:
                data = json.load(f)
            with open(os.path.join(parsed_pdf_dir, pdf_file_name + ".json"), "r") as f:
                paper_data = json.load(f)
        except:
            with open(os.path.join(OUT_PATH, "error_log_build_dataset.txt"), "a") as f:
                f.write(pdf_file_name + "\n")
            continue

        # Read the captions and filter the ones that have a text of "method" or "model"
        for figure in data:

            # Filter figures
            if figure['figType'] == "Figure":
                # Filter figures with desired text in caption
                if any(text_filter in figure["caption"].lower() for text_filter in text_filters) and not any(
                        avoid in figure["caption"].lower() for avoid in text_avoid):
                    im = cv2.imread(figure['renderURL'])
                    aspect = im.shape[1] / im.shape[0]

                    # Retrieve all sentences that describe that figure in the paper
                    captions = retrieve_text_for_figure(figure, paper_data)
                    captions.insert(0, figure['caption'])  # Add the actual caption at [0]
                    if len(captions) > 1:
                        count_texts += 1

                    figure_id = Path(figure['renderURL']).stem
                    data_list.append({
                        "figure_id": figure_id,
                        "figure_path": figure['renderURL'],
                        "captions": captions,
                        "aspect": aspect
                    })
                    # with open(os.path.join(+'.json'), 'w') as f:
                    #     json.dump(data, f)
                    counter += 1

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

    print("Number of figures: ", counter, "samples with more than 1 caption: ", count_texts)


if __name__ == '__main__':
    main()
