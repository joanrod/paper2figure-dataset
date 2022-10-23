import os
import json
import re
# Note: This logic should be added to the pipeline (the latest code is in local, not here)

ROOT_PATH = "/mnt/colab_public/datasets/joan/arxiv/Paper2Fig100k"

def normalize_caption(text):
    lower_string = text.lower()
    no_number_string = re.sub(r'\d+', 'NUM-TK', lower_string)
    no_punc_string = re.sub(r'[^\w\s]', '', no_number_string)
    no_wspace_string = no_punc_string.strip()
    return no_wspace_string


def main() -> None:
    splits = ["train", "test"]
    for split in splits:
        filename = os.path.join(ROOT_PATH, f'{split}_data.json')
        with open(filename, "r") as f:
            data = json.load(f)
        for figure in data:
            captions = figure['captions']
            norm_captions = [normalize_caption(cap) for cap in captions]
        

if __name__ == "__main__":
    main()
