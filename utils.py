from trafilatura import fetch_url, extract, baseline
from trafilatura.settings import use_config
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

config = use_config()
config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")

def get_urls_and_titles(query):
    urls = []
    titles = []
    page = 1
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&num=3"
    data = requests.get(url, headers=headers).json()
    search_items = data.get("items")
    for search_item in search_items:
        title = search_item.get("title")
        link = search_item.get("link")
        urls.append(link)
        titles.append(title)
    return [urls, titles]

def extract_all_text(url):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return " ".join(t.strip() for t in visible_texts)

def extract_paragraphs_trafilatura(url, include_formatting=True):
    downloaded = fetch_url(url)
    result = baseline(fetch_url(url))[1]
    return result

def extract_paragraphs(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True, separator='\n')
        if '.' in text:
            paragraphs.append(text)
    return paragraphs        

def extract_paragraphs_lists(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True, separator='\n')
        if '.' in text:
            paragraphs.append(text)
    elements = []
    uls = soup.find_all('ul')
    for ul in uls:
        for li in ul.findAll('li'):
            text = li.get_text(strip=True, separator='\n')
            arr = text.split('\n')
            for a in arr:
                if '.' in a:
                    elements.append(a)
    total = paragraphs + elements
    return total


def get_query_passages(school_name, queries):
    passages = {}
    for query in queries:
        urls = get_urls_and_titles(f'{school_name} Computer Science department {query}')[0]
        for url in urls:
            print(url)
            paragraphs = extract_paragraphs(url)
            if query in passages:
                passages[query].append(' '.join(paragraphs))
            else:
                passages[query] = [' '.join(paragraphs)]
            
    return passages
