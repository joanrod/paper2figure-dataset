import os
from tqdm import tqdm

# os.listdir(os.path.join(data_path, pdf_dir))[0]
def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                        help='Path where the data is stored')

    args = parser.parse_args()

    ROOT_PATH = args.path_data  

    for pdf_dir in tqdm(os.listdir(ROOT_PATH)):
        # Keep only last version of the paper
        versions = []
        for paper in os.listdir(os.path.join(ROOT_PATH, pdf_dir)):
            # Store versions of each paper
            versions.append(int(paper.split("v")[1].split(".")[0]))
        if len(versions) > 1:
            versions.remove(max(versions))
            for v in versions:
                pdf_filename = paper.split("v")[0] + "v" + str(v)
                pdf_file_dir = os.path.join(ROOT_PATH, pdf_dir, pdf_filename+'.pdf')
                os.remove(pdf_file_dir)


if __name__ == '__main__':
    main()
