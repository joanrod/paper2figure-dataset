# File: filter_papers.py
# Goal: (Step 1) - Filter desired papers from arxiv using the kaggle dataset paper metadata

import argparse
import json
import os
import pandas as pd

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subjects', type=str, default=None,
                    help='List of arxiv subjects')
parser.add_argument('-m', '--month', type=str, default='01',
                    help='Begin from this month')
parser.add_argument('-y', '--year', type=str, default='20',
                    help='Begin from this year')
parser.add_argument('-p', '--path_json', type=str, default=None, required=True,
                    help='path of metadata json file')
parser.add_argument('--export_xlsx', type=bool, default=True,
                    help='Boolean to export into xlsx')
args = parser.parse_args()

def get_metadata(data_file):
    with open(data_file, 'r') as f:
        for line in f:
            yield line

def str2list(string):
    li = []
    for s in string.split(","):
        li.append(s)
    return li

def date_in_range(year_month, year_month_filter):
    # Parse inputs
    try:
        y = int(year_month[:2])
        m = int(year_month[2:])
    except:
        return False

    y_filter = int(year_month_filter[:2])
    m_filter = int(year_month_filter[2:])

    # Decision
    if y > y_filter:  # if year is higher go for True
        return True
    elif y == y_filter and m >= m_filter:  # In case its same year, check if month is equal or higher
        return True
    return False

def main():
    # Parse args
    subjects = str2list(args.subjects)
    month = args.month
    year = args.year
    year_month_filter = year + month  # year-month id following arxiv format (ex: 0704.0671, random paper of april 2007)

    path_json = args.path_json
    export_excel = args.export_excel

    # Create output directory
    OUTPUT_PATH = 'output'
    os.makedirs(OUTPUT_PATH, exists_ok = True)

    # Lists for relevant fields
    titles = []
    ids = []
    abstracts = []
    authors_parsed = []
    authors = []
    years = []
    journals = []
    categories = []

    print("Processing json file...")
    metadata = get_metadata(path_json)
    print("Finished processing json file.")

    print("Processing papers...")
    for paper in metadata:
        # Get metadata of current paper
        paper_dict = json.loads(paper)

        # filter by date
        year_month = paper_dict.get('id').split(".")[0]
        if date_in_range(year_month, year_month_filter):
            if any(subject in paper_dict['categories'] for subject in subjects):  # Filter subjects

                years.append(paper_dict.get('year'))
                ids.append(paper_dict.get('id'))
                authors_parsed.append(paper_dict.get('authors_parsed'))
                authors.append(paper_dict.get('authors'))
                titles.append(paper_dict.get('title'))
                abstracts.append(paper_dict.get('abstract'))
                journals.append(paper_dict.get('journal-ref'))
                categories.append(paper_dict['categories'])

    print(f"Extracted {len(titles)} papers. Storing results...")
    # Write ids to file
    with open(os.path.join(OUTPUT_PATH, 'paper_ids.txt'), 'w') as f:
        for id in ids:
            f.write(id + '\n')
    if export_excel:
        papers = pd.DataFrame({
            'id': ids,
            'title': titles,
            'authors': authors,
            'authors parsed': authors_parsed,
            'abstract': abstracts,
            'year': years,
            'journal': journals,
            'categories': categories
        })
        papers.head()

        papers.to_excel(os.path.join(OUTPUT_PATH, 'filtered_papers_metadata.xlsx'))

    print("There you go human")


if __name__ == '__main__':
    main()
