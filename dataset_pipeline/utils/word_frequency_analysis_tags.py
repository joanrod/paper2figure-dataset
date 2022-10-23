# File: word_frequency_analysis_tags.py
# Goal: Extract most frequent words in captions, ignoring a large list of stop words.
# Iteratively (manually) add stopwords that are not related to ML methods or achitectures

import argparse
import json
import os
import timeit
from collections import Counter
from tqdm import tqdm
import re
import numpy as np
import matplotlib.pyplot as plt

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

# Load stopwords list
with open('keywords/stopwords.txt') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

def normalize_text(text):
    lower_string = text.lower()
    no_number_string = re.sub(r'\d+', '', lower_string)
    no_punc_string = re.sub(r'[^\w\s]', '', no_number_string)
    no_wspace_string = no_punc_string.strip()
    return no_wspace_string


def filter_stopwords(text):
    words = [text][0].split()
    ok_words = [w for w in words if w not in stopwords]
    return ok_words


def main() -> None:
    corpus = []
    for paper in tqdm(os.listdir(JSON_DIR)):
        with open(os.path.join(JSON_DIR, paper)) as f:
            paper_data = json.load(f)
            if not paper_data:
                continue
            for fig_data in paper_data:
                for caption in fig_data['captions']:
                    normalized_cap = normalize_text(caption)
                    words_cap = filter_stopwords(normalized_cap)
                    corpus += words_cap

    counts = Counter(corpus)
    labels, values = zip(*counts.items())

    # sort your values in descending order
    indSort = np.argsort(values)[::-1]

    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]

    with open("keywords.txt", "w") as output:
        for row in labels.tolist():
            try:
                output.write(str(row) + '\n')
            except:
                continue
                
    stop = timeit.default_timer()

    print('Time: ', stop - start)


if __name__ == "__main__":
    main()
