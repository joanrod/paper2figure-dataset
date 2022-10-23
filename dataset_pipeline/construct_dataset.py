# File: generate_splits.py
# Goal: (Step 4) - Perform the split of the dataset and store in train and val json files

import argparse
import json
import multiprocessing as mp
import os
import timeit
from pathlib import Path

import cv2
from tqdm import tqdm

start = timeit.default_timer()
# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')

args = parser.parse_args()

ROOT_PATH = args.path_data
PARSED_DATA_PATH = os.path.join(ROOT_PATH, 'parsed')  # Already parsed by Grobid
PROCESSED_DATA_PATH = os.path.join(ROOT_PATH, 'paper2figure')
JSON_DIR = os.path.join(PROCESSED_DATA_PATH, 'json_data')
IMAGES_DIR = os.path.join(PROCESSED_DATA_PATH, 'figures')
OUT_PATH = 'output'

MAX_WORKERS = mp.cpu_count()
CHUNK_SIZE = 50

# Define text filters over caption # TODO: Store this in a file, this is ugly
text_filters = [
    'model architecture', 'architecture', 'model diagram', 'overview', 'pipeline',
    'flowchart', 'proposed method', 'framework', 'schem',
    'network structure', 'network diagram', 'flow-chart']

text_avoid = ['exampl', 'table', '=', '>', '<', 'methods', 'comparison', 'compare', 'ablation']

# Test if we can find architecture types from text (not used for now)
# TO DO: Use a clustering technique to obtain the classes
architecture_types = {
    'cnn': ['cnn', 'convolutional', 'convnet', 'conv2d', 'resnet', 'vgg', 'mobilenet', 'efficientnet', 'inceptionV',
            'alexnet'],
    'rnn': ['rnn', 'recurrent neural', ' gru ', '(gru)'],
    'lstm': ['lstm', 'long-short term'],
    'transformer': ['transformer', ' bert ', ' bart ', 't5', 'self-attention', 'cross-attention'],
    'contrastive': ['triplet', 'siamese', 'contrastive'],
    'gan': [' gan ', '(gan)', 'discriminator', 'adversarial'],
    'svm': [' svm ', '(svm)', 'support vector'],
    'mlp': [' mlp ', '(mlp)', 'dnn', 'feed forward', 'multi layer perceptron', 'linear layer'],
    'vae': [' vae ', '(vae)', 'variational autoencoder'],
    'unet': ['unet'],
    'rcnn': ['rcnn', 'r-cnn', 'yolo'],
    'nlp': ['nlp', 'natural language', 'language model'],
    'rl': ['reinforcement learning', 'Q-Learning'],
    'clustering': ['cluster', 'kmeans', 'k-means', 'k means'],
    'difusion': ['diffusion'],
    'distillation': ['teacher network', 'student network', 'distill'],
    'graph': ['gnn', '(gnn)', 'graph neural network', 'graph network'],
}


def validate_reference(ref, paragraph):
    # Avoid not allowed chars after the Fig reference
    not_allowed_chars_after_ref = ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                                   "0"]  # Find case where "Fig 1", and "Fig 11"
    try:
        next_char = paragraph[paragraph.find(ref) + len(ref)]
    except:
        return True
    return not any(next_char == c for c in not_allowed_chars_after_ref)


def get_figure_type(text):
    types = []
    for type in architecture_types:
        if any(name in text.lower() for name in architecture_types[type]):
            types.append(type)
    return types


def retrieve_text_for_figure(figure, paper, caption):
    captions = []

    # Get figure number
    figure_num = figure['name']

    # Prepare strings to look in the paper referencing this figure
    figure_names = [f'fig {figure_num}', f'fig. {figure_num}',
                    f'fig{figure_num}', f'fig.{figure_num}',
                    f'figure {figure_num}', f'figure. {figure_num}',
                    f'figure{figure_num}', f'figure.{figure_num}', f'figure . {figure_num}']

    types = get_figure_type(caption)  # Init types by first search in actual caption

    # Prepare paper text
    for section in paper['sections']:
        section_text = section['text']

        # Split in paragraphs, using \n
        paragraphs = section_text.split('\n')
        for p in paragraphs:
            if any(validate_reference(name, p.lower()) if name in p.lower() else False for name in figure_names):
                captions.append(p)
                types = types + get_figure_type(p)

    # Remove duplicates
    types = list(dict.fromkeys(types))

    # Insert caption at start
    captions.insert(0, figure['caption'])  # Add the actual caption at [0]
    return captions, types

def process_pdf(paper):
    pdf_dir = os.path.join(PARSED_DATA_PATH, paper)
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
        return

    data_pdf = []
    # Read the captions and filter the ones that have a text of "method" or "model"
    for figure in data:
        # Filter figures
        if figure['figType'] == "Figure":
            # Filter figures with desired text in caption
            if any(text_filter in figure["caption"].lower() for text_filter in text_filters) and not any(
                    avoid in figure["caption"].lower() for avoid in text_avoid):
                try:
                    im = cv2.imread(figure['renderURL'])
                    aspect = im.shape[1] / im.shape[0]

                    image_color = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    hist = cv2.calcHist([image_color], [0], None, [16], [0, 256])
                    cv2.normalize(hist, hist, norm_type=cv2.NORM_L1)
                    if hist[-1] < 0.1 or hist[-1] > 0.95:
                        continue
                except:
                    continue

                # Retrieve all sentences that describe that figure in the paper
                captions, types = retrieve_text_for_figure(figure, paper_data, caption=figure['caption'])

                figure_id = Path(figure['renderURL']).stem

                # Store image
                im_filename = os.path.join(IMAGES_DIR, figure_id + '.png')
                cv2.imwrite(im_filename, im)
                data_fig = {
                    "figure_id": figure_id,
                    "types": types,
                    "figure_path": im_filename,
                    "captions": captions,
                    "aspect": aspect
                }
                data_pdf.append(data_fig)
    if data_pdf:
        with open(os.path.join(JSON_DIR, paper + '.json'), 'w') as f:
            json.dump(data_pdf, f)

    return len(data_pdf)


def compute_processed_files(papers_to_process):
    for paper in tqdm(papers_to_process):
        if os.path.exists(os.path.join(JSON_DIR, paper + '.json')):
            papers_to_process.remove(paper)
    return papers_to_process


def main() -> None:
    # Create folder for json data and images data
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    # prepare
    print("Preparing I: Counting papers to process")
    papers_to_process = []
    for paper in tqdm(os.listdir(PARSED_DATA_PATH)):
        papers_to_process.append(paper)

    # compute already computed papers
    print("Preparing II: Counting papers already processed")
    papers_to_process = compute_processed_files(papers_to_process)

    with mp.Pool(processes=MAX_WORKERS) as p:
        count_images = list(
            tqdm(p.imap(process_pdf, papers_to_process, CHUNK_SIZE), total=len(papers_to_process)))

    stop = timeit.default_timer()

    print('Time: ', stop - start)


if __name__ == "__main__":
    main()
