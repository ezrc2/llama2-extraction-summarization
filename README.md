# llama2-extraction-summarization

## Setup

Python 3.8, conda, cuda 11.6

I have provided a conda environment file, please create the environment using this command:
```
conda env create -f environment.yml
```

NLTK requires some extra downloads, so run this in a python file:
```Python
import nltk

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
```

**Directory Structure**
```
eric-chen-web-extraction-summarization/
  - classification_dataset                   # classification dataset of 5 categories about universities
      - labels.txt
      - passages.txt
  - experiments
      - ape_test.ipynb                       # implementation of an example of the Automatic Prompt Engineer paper
      - basic_implementation.ipynb           # example of each step of the wiki generation workflow
      - citation_aware.ipynb                 # find prompt to generate summaries with citations from each passage
      - extraction.ipynb                     # content extraction method and evaluation, also use Llama 2 reformat into displayable string
      - extraction_dataset.csv               # dataset with url and main text from web page
      - scraping.ipynb                       # testing different web scraping methods, and try clustering to group information
      - utils.py                             # helper functions file, scraping and extraction
      - webpage_categorization.ipynb         # test out categorizing web pages into textual vs tabular based on some text density techniques
  - evaluate_classification.ipynb            # comparing traditional classifiers to llama 2 zero-shot classification
```
