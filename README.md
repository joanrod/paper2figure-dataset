# Paper2Fig dataset
### [OCR-VQGAN: Taming Text-within-Image Generation](https://arxiv.org/abs/2210.11248)
[![arXiv](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs/2210.11248)

<br>


[Juan A. Rodríguez](https://scholar.google.es/citations?user=0selhb4AAAAJ&hl=en), [David Vázquez](https://scholar.google.es/citations?user=1jHvtfsAAAAJ&hl=en), [Issam Laradji](https://scholar.google.ca/citations?user=8vRS7F0AAAAJ&hl=en), [Marco Pedersoli](https://scholar.google.com/citations?user=aVfyPAoAAAAJ&hl=en), [Pau Rodríguez](https://scholar.google.com/citations?user=IwBx73wAAAAJ)

-----------
[Computer Vision Center, Autonomous University of Barcelona](http://www.cvc.uab.es/)

[ServiceNow Research, Montréal, Canada](https://www.servicenow.com/research/)

[ÉTS Montreal, University of Québec](https://www.etsmtl.ca/)

------------------

This project is devoted to construct a dataset of pairs of Figures and Captions extracted from research papers, named **Paper2Fig**. The current version of the dataset is [**Paper2Fig100k, presented in this paper**](https://arxiv.org/abs/2210.11248).

The papers are extracted from arXiv.org thanks to [arxiv kaggle dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) and [scypdf](https://github.com/titipata/scipdf_parser) repository, a pdf-parser based on [GROBID](https://github.com/kermitt2/grobid).

>Check out our work [**OCR-VQGAN**](https://www.github.com/joanrod/ocr-vqgan) project, which presents an image encoder especialized in the image domains of figures and diagrams using Paper2Fig100k dataset.
-------------------

## Dataset construction pipeline:
### 1. Download the desired arxiv papers
* **Filter papers from arxiv-metadata.json**

That is, downloading the latest version of the file available at https://www.kaggle.com/datasets/Cornell-University/arxiv.
Then run the script filter_papers.py using the following command:

    python filter_papers.py -s [List of arxiv subjects] -y [year] -m [month] -p [path to json]

The available subjects can be found in https://arxiv.org/category_taxonomy. Example for filtering the papers corresponding to
the subject of Computer Vision (cs.CV) and Machine Learning (cs.LG), and papers after 01/2010:

    python filter_papers -s cs.CV cs.LG -y 10 -m 01 -p D:/arxiv/arxiv-metadata-oai-snapshot.json

This process will generate a csv file (and optionally xlsx file) with the filtered papers.

* **Download the filtered papers**

Files can be downloaded using gsutil, as explained in [arXiv Dataset - Bulk access](https://www.kaggle.com/datasets/Cornell-University/arxiv#:~:text=download%20the%20PDF-,Bulk%20access,-The%20full%20set). 
But we use [Google Cloud Storage API](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python) to programmatically download the filtered papers. 
Follow the steps in the link to install google-cloud-storage, setting up API authentication and creating a project.

We can use the download_papers.py script as follows:
        
    python download_papers.py -path [path to txt file] -project [Google Cloud project]

We pass the generated txt file with paper ids using the parameter -path, and the project name with -project.

### 2. Parse pdf text and figures using GROBID

* **Install and run GROBID service via Docker**

GROBID is an open-project for parsing pdf files, that is based in CRF and Deep Learning. The easiest way to use GROBID is via Docker, using the latest version available in Docker Hub. 
You can run the GROBID service locally using Docker desktop and:

    docker pull lfoppiano/grobid:0.7.1
    docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.1

See the [official GROBID documentation](https://grobid.readthedocs.io/en/latest/Grobid-docker/) to explore the different installation alternatives.

* **Parse pdfs**

Once the GROBID service is running, it can be used through its API using [scipdf](https://github.com/titipata/scipdf_parser) library, by installing int in your env.
Then, use the parse_pdf.py script as follows:
        
    python parse_pdf.py -p [dataset dir]

The parameter "-p" defines a directory where your dataset is located. Note that the directory that you specify should have a directory named "pdf", where the downloaded pdfs are located.
At the end, you should have the following structure:

    ├── dataset
    │   ├── pdf
    │   └── parsed
    └── ...

### 2. Build Paper2Fig dataset

    python paper2fig_multiprocessing.py -p [dataset dir]