from google.cloud import storage
import os
import argparse
from tqdm import tqdm

from util import has_files

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--project', type=str, default=None, required=True,
                    help='Name of Google Cloud project')
parser.add_argument('--paper_ids', type = str, default=None, required=True,
                    help = 'path to the .txt file with the paper ids to download')
parser.add_argument('-out', '--out_path', type=str, default=None, required=True,
                    help='Path where the data will be stored (careful, choose a path with sufficient disk space')
args = parser.parse_args()

def compute_downloaded_files(data_path):
    ids = []
    for pdf_dir in tqdm(os.listdir(data_path)):
        if os.path.exists(os.path.join(data_path, pdf_dir)) and has_files(os.path.join(data_path, pdf_dir)):
            ids.append(pdf_dir)
    return ids


def main():
    client = storage.Client(project=args.project)
    bucket = client.bucket('arxiv-dataset')

    # Read txt file with ids
    with open(os.path.join(args.out_path, 'paper_ids.txt'), 'r') as f:
        ids = f.readlines()

    download_format = 'pdf'
    OUT_PATH = args.out_path + "/paper2figure_dataset/" + download_format + "/"
    os.makedirs(OUT_PATH, exists_ok = True)

    # Remove downloaded ids from list
    print("Checking if you have any of the files already downloaded")
    downloaded_ids = compute_downloaded_files(OUT_PATH)
    
    print("Downloading papers...")
    for id in tqdm(ids):
        id = id.rstrip()
        if id in downloaded_ids:
            continue

        yymm = id.split('.')[0]

        blobs = bucket.list_blobs(prefix='arxiv/arxiv/' + download_format + '/' + yymm + '/' + id)
        for blob in blobs:
            out_dir = OUT_PATH + id + '/'
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            blob.download_to_filename(out_dir + blob.name.split('/')[-1])
    print("Finished, there you go human")


if __name__ == '__main__':
    main()
