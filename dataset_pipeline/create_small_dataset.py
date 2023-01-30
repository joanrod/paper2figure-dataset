
import random
import json
import os
import shutil

def main():
    ROOT_PATH = "/mnt/colab_public/datasets/joan/arxiv/Paper2Fig100k"
    OUT_DIR = os.path.join(ROOT_PATH, 'fig_subset')
    os.makedirs(OUT_DIR, exist_ok=True)

    # Read train json file
    with open(os.path.join(ROOT_PATH, 'train_data.json')) as f:
        data = json.load(f)
    
    # Extract 10 figs
    figs_test = [random.randint(0, len(data)) for i in range(10)]

    list_figs = []
    for fig_id in figs_test:
        ob = data[fig_id]

        
        # Store images in a separate folder
        src = os.path.join(ROOT_PATH, 'figures', f'{ob["figure_id"]}.png')
        dst = os.path.join(OUT_DIR, f'{ob["figure_id"]}.png')
        shutil.copyfile(src, dst)

        list_figs.append(ob)

    with open(os.path.join(ROOT_PATH, f"paper2fig_aspect_ratio.json"), "w") as f:
        json.dump(list_figs, f)



if __name__ == '__main__':
    main()