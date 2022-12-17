import os
import json
import re
# Note: This logic should be added to the pipeline (the latest code is in local, not here)

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')
args = parser.parse_args()
ROOT_PATH = args.path_data

def normalize_caption(text):
    lower_string = text.lower()
    citation_token_string = re.sub(r'\[.+\]', 'citation-tk', lower_string) # Manage citations
    number_token_string = re.sub(r'[+-]?((\d+(\.\d+)?)|(\.\d+)|(\d[-/]\d))[ .:\n,]', 'number-tk ', citation_token_string) # Manage numbers TODO: Revise this
    no_weird_dots = re.sub(r' +\.', '.', number_token_string) # Manage weird dots
    no_weird_symbols = re.sub(r'(• ?)|(@)', '', no_weird_dots) # Manage weird symbols
    no_double_spaces = re.sub(r'  ', ' ', no_weird_symbols) # Manage double spaces
    no_wspace_string = no_double_spaces.strip()
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
