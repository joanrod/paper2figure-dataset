# File: apply_ocr.py
# Goal: (Step 5) - Perform ocr over images to extract texts and bounding boxes
# Output: At the end, you will have a directory

import argparse
import os
from tqdm import tqdm
import easyocr
import json

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default = None, required=True,
                    help='Path where the figures are stored (all figures in the same directory)')
args = parser.parse_args()

def main():
    ROOT_PATH = args.path_data
    IMAGES_DIR = os.path.join(ROOT_PATH, 'figures')
    OCR_OUT_DIR = os.path.join(ROOT_PATH, 'ocr_results_2')
    os.makedirs(OCR_OUT_DIR, exist_ok = True)

    # Instantiate OCR
    reader = easyocr.Reader(['en'])

    # Get figures
    for figure in tqdm(os.listdir(IMAGES_DIR)):
        if figure.endswith(".png"):
            figure_id=figure.split(".png")[0]
            try:
                result = reader.readtext(os.path.join(IMAGES_DIR, figure))
                ocr_results = []
                for res in result:
                    ob = {
                        "text" : str(res[1]),
                        "bbox" : str(res[0]),
                        "confidence" : str(round(res[2], 2))
                    }
                    ocr_results.append(ob)
                out = {
                    "figure_id":figure_id,
                    "ocr_result":ocr_results
                }
                
            except:
                out = {
                    "figure_id":figure_id,
                    "ocr_result": 'error'
                }
            
            with open(os.path.join(OCR_OUT_DIR, figure_id + '.json'), 'w') as f:
                    json.dump(out, f)


if __name__ == '__main__':
    main()