# File: construct_dataset.py
# Created by Juan A. Rodriguez on 02/11/2022
# Goal: (Step 4) - Perform the split of the dataset and store in train and val json files
# Output: At the end of this process you will have a directory 'json_data' with text pairs 
# and metadata for each figure in json format (on json per figure) 

import argparse
import json
import os
from tqdm import tqdm
import re

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')
args = parser.parse_args()

def normalize_texts_scipdf(text):
    lower_string = text.lower()
    citation_token_string = re.sub(r'\[.+\]', 'citation-tk', lower_string) # Manage citations
    number_token_string = re.sub(r'[+-]?((\d+(\.\d+)?)|(\.\d+)|(\d[-/]\d))[ .:\n,]', 'number-tk ', citation_token_string) # Manage numbers
    no_weird_dots = re.sub(r' +\.', '.', number_token_string) # Manage weird dots
    no_weird_symbols = re.sub(r'(• ?)|(@)', '', no_weird_dots) # Manage weird symbols
    no_double_spaces = re.sub(r'  ', ' ', no_weird_symbols) # Manage double spaces
    no_wspace_string = no_double_spaces.strip()
    return no_wspace_string

def normalize_texts_galai(text):
    lower_string = text.lower()
    citation_token_string = re.sub(r'\[.+\]', '[START_REF][END_REF]', lower_string) # Manage citations
    no_weird_dots = re.sub(r' +\.', '.', citation_token_string) # Manage weird dots like ' .' -> '.'
    no_weird_symbols = re.sub(r'(•)|(@)|(\?)', '', no_weird_dots) # remove stop symbols
    no_double_spaces = re.sub(r'  ', ' ', no_weird_symbols) # Manage double spaces
    no_wspace_string = no_double_spaces.strip()
    return no_wspace_string

def main():
    ROOT_PATH = args.path_data
    OCR_OUT_DIR = os.path.join(ROOT_PATH, 'ocr_results_2') # ocr_results_2 is the more updated dir, ocr_results is the v1
    splits = ['train', 'test']
    for split in splits:
        data_split = []
        with open(os.path.join(ROOT_PATH, f'{split}_data.json')) as f:
            data = json.load(f)
        for fig in tqdm(data):    
            figure_id = fig['figure_id']
            try:
                with open(os.path.join(OCR_OUT_DIR, figure_id + '.json')) as f:
                    ocr_result = json.load(f)

                ob = {
                    "figure_id" : figure_id,
                    "captions" : fig['captions'],
                    "captions_scipdf" : [normalize_texts_scipdf(text) for text in fig['captions']],
                    "captions_galai" : [normalize_texts_galai(text) for text in fig['captions']],
                    "ocr_result": ocr_result,
                    "aspect": round(fig['aspect'], 2)
                }
                data_split.append(ob)
            except:
                continue

        with open(os.path.join(ROOT_PATH, f"paper2fig_{split}.json"), "w") as f:
            json.dump(data_split, f)

if __name__ == '__main__':
    main()
