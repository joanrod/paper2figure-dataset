import os
import scipdf
import json
from tqdm import tqdm
import argparse

from util import has_files

# Argument parsing
parser = argparse.ArgumentParser()

parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the dataset is stored')
args = parser.parse_args()


def compute_parsed_files(data_path):
    ids = []
    for pdf_dir in tqdm(os.listdir(data_path)):
        pdf_dir_path = os.path.join(data_path, pdf_dir)
        child_dir = os.listdir(os.path.join(data_path, pdf_dir))[0]

        if has_files(os.path.join(pdf_dir_path, child_dir, 'figures_metadata')):
            ids.append(pdf_dir)

    with open(os.path.join('output', 'error_log_grobid.txt'), 'r') as f:
        error_ids = f.readlines()

    # Add errors to avoid passing again
    for e in error_ids:
        ids.append(e.rstrip().split('\\')[-2])

    print(f'Number of correctly processed files: {len(ids)}')
    return ids


def main():
    ROOT_PATH = args.path_data
    PDF_DATA_PATH = os.path.join(ROOT_PATH, 'pdf')
    PARSED_DATA_PATH = os.path.join(ROOT_PATH, 'parsed')
    # Create dir
    if not os.path.exists(PARSED_DATA_PATH):
        os.makedirs(PARSED_DATA_PATH)
    OUT_PATH = 'output'

    # Remove downloaded ids from list
    print("Checking if you have any of the files already downloaded")
    parsed_ids = compute_parsed_files(PARSED_DATA_PATH)

    for pdf_dir in tqdm(os.listdir(PDF_DATA_PATH)):
        if pdf_dir in parsed_ids:
            continue
        # Keep only last version of the paper
        versions = []
        for paper in os.listdir(os.path.join(PDF_DATA_PATH, pdf_dir)):
            # Store versions of each paper
            versions.append(int(paper.split("v")[1].split(".")[0]))

        pdf_filename = paper.split("v")[0] + "v" + str(max(versions))
        pdf_file_dir = os.path.join(ROOT_PATH, 'pdf', pdf_dir, pdf_filename)
        parsed_pdf_dir = os.path.join(PARSED_DATA_PATH, pdf_dir, pdf_filename)
        pdf_to_parse = pdf_file_dir + ".pdf"

        # Create directory
        if not os.path.exists(parsed_pdf_dir):
            os.makedirs(parsed_pdf_dir)

        try:
            article_dict = scipdf.parse_pdf_to_dict(pdf_to_parse)  # return dictionary
            if article_dict is None:
                print("Error with GROBID parser, check the service is available!")
                break
            with open(os.path.join(parsed_pdf_dir, pdf_filename + ".json"), "w") as f:
                json.dump(article_dict, f, indent=4)
            scipdf.parse_figures(pdf_to_parse, output_folder=parsed_pdf_dir)  # folder should contain only PDF files
        except:
            print("Error in parsing: " + pdf_to_parse)
            # Write error to file in append mode
            with open(os.path.join(OUT_PATH, "error_log_grobid.txt"), "a") as f:
                f.write(pdf_to_parse + "\n")


if __name__ == '__main__':
    main()
