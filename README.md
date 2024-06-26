# Paper2Fig dataset
### [OCR-VQGAN: Taming Text-within-Image Generation](https://arxiv.org/abs/2210.11248)

[![arXiv](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs/2210.11248)

[Juan A. Rodríguez](https://scholar.google.es/citations?user=0selhb4AAAAJ&hl=en), [David Vázquez](https://scholar.google.es/citations?user=1jHvtfsAAAAJ&hl=en), [Issam Laradji](https://scholar.google.ca/citations?user=8vRS7F0AAAAJ&hl=en), [Marco Pedersoli](https://scholar.google.com/citations?user=aVfyPAoAAAAJ&hl=en), [Pau Rodríguez](https://scholar.google.com/citations?user=IwBx73wAAAAJ)

-----------
[Computer Vision Center, Autonomous University of Barcelona](http://www.cvc.uab.es/)

[ServiceNow Research, Montréal, Canada](https://www.servicenow.com/research/)

[ÉTS Montreal, University of Québec](https://www.etsmtl.ca/)

------------------

This project is devoted to construct a dataset of pairs of Figures and Captions extracted from research papers, which we call **Paper2Fig**. The current version of the dataset is [**Paper2Fig100k, presented in this paper**](https://arxiv.org/abs/2210.11248). The following are some samples from the dataset.

<p align="center">
  <a href="https://arxiv.org/abs/2209.xxxx"><img src="assets/figures.png" alt="comparison" width="800" border="0"></a>
</p>

Here we present the pipeline designed to construct Paper2Fig dataset using public research papers generally from Computer Science fields like Machine Learning or Computer Vision. The papers are downloaded from arXiv.org thanks to [arxiv kaggle dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) and [scypdf](https://github.com/titipata/scipdf_parser) repository, a pdf-parser based on [GROBID](https://github.com/kermitt2/grobid). 

>Check out our work [**OCR-VQGAN**](https://www.github.com/joanrod/ocr-vqgan), which presents an image encoder especialized in the image domains of figures and diagrams using Paper2Fig100k dataset.
-------------------

## Dataset construction pipeline:
### 1. Download the desired arxiv papers
* **Filter papers from arxiv-metadata.json**

That is, downloading the latest version of the file available at https://www.kaggle.com/datasets/Cornell-University/arxiv.
Then run the script `dataset_pipeline/filter_papers.py` using the following command:

```
python dataset_pipeline/filter_papers.py -s <List of arxiv subjects> -y <year> -m <month> -p <path to arxiv metadata>
```

The available subjects can be found in https://arxiv.org/category_taxonomy. For instance, we can filter papers corresponding to the subject of `Computer Vision (cs.CV)` and `Machine Learning (cs.LG)`, and papers after `01/2010`:
```
python dataset_pipeline/filter_papers -s cs.CV cs.LG -y 10 -m 01 -p path/to/arxiv-metadata-oai-snapshot.json
````

This process will generate a .txt file with the list of extracted papers (arXiv ids). Optionlally, you can generate a xlsx file passing `--export_xlsx` to explore the paper's metadata.

* **Download the filtered papers**

Files can be downloaded using gsutil, as explained in [arXiv Dataset - Bulk access](https://www.kaggle.com/datasets/Cornell-University/arxiv#:~:text=download%20the%20PDF-,Bulk%20access,-The%20full%20set). We use [Google Cloud Storage API](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python) to programmatically download the filtered papers. Follow the steps in the [link](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python) to install `google-cloud-storage`, setting up API authentication and creating a new project.

We can use the `dataset_pipeline/download_papers.py` script as follows:

```
python dataset_pipeline/download_papers.py --paper_ids <path to txt file> --project <Google Cloud project> --out_path <path store pdfs>
````

where we pass the generated .txt file with paper ids using the parameter `--paper_ids`, the project name with `--project`, and the output path with `--out_path`, for pdf storage.

### 2. Parse pdf text and figures using GROBID
In this process, we need to parse and organize the texts and images that are contained in each pdf. We make use of **GROBID** and **SciPdf** to parse images and texts.

* **Install and run GROBID service via Docker**

>GROBID is an open-project for parsing pdf files, that is based in CRF and Deep Learning. The easiest way to use GROBID is via Docker, using the latest version available in Docker Hub. 

You can run the GROBID service locally using Docker desktop and:
```
docker pull lfoppiano/grobid:0.7.1
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.1
````

See the [official GROBID documentation](https://grobid.readthedocs.io/en/latest/Grobid-docker/) to explore the different installation alternatives.

* **Parse pdfs**

Once the GROBID service is running, it can be used through its API using [scipdf](https://github.com/titipata/scipdf_parser) library, by installing int in your env.
Then, use the `dataset_pipeline/parse_pdf.py` script as follows:

```
python dataset_pipeline/parse_pdf.py -p [dataset dir]
````

where `-p` defines the directory where your dataset is located. Note that the directory that you specify should have a directory named `pdf`, where the downloaded pdfs are located.

At the end, you should have the following structure:
```
├── dataset
│   ├── pdf
│   └── parsed
└── ...
```

## 3. Apply heuristics to filter diagram figures for Paper2Fig dataset
In this step we apply heuristic rules to filter images (avoid results figures like plots, charts, etc.) and obtain text captions of figures. This is done using multiprocessing, and can be executed with:

```
python dataset_pipeline/apply_heuristics.py -p <dataset dir>
```

## 4. Perform OCR text recognition over Figures
In this step we process the final set of figures with [EasyOCR](https://github.com/JaidedAI/EasyOCR) text recognizer.

```
pip install easyocr
python dataset_pipeline/apply_ocr.py -p <dataset dir>
```

## 5. Extract class tags from strings
Here we 
```
python dataset_pipeline/assign_class_tags.py -p <dataset dir>
```

## 6. Construct Paper2Fig dataset
Now it's time to put it all together, generating the final dataset using a JSON structure. Also, the split of the dataset in train and test is performed with:

```
python dataset_pipeline/construct_dataset.py -p <dataset dir>
```

In Paper2Fig, each figure has a json object associated that contains the following information:

```json
{
  "figure_id": "...", 
  "captions": ["...", "..."], 
  "captions_norm": ["...", "..."], 
  "ocr_result": [{
    "text": "...", 
    "bbox": "[[71, 18], [134, 18], [134, 44], [71, 44]]", 
    "confidence": 0.99
    }],
  "aspect": 4.7962466487935655
}
```

