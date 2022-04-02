import re
import requests
from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from urllib.parse import urlparse
url = "https://tim.blog/" # the blog we'll scrape
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import urlparse
import time

content_area_class = 'entry-content' # the name of the div class for any given blog post

def fetch_url(url):
    r = requests.get(url)
    return r.text

def soup_a(html, display_result=False):
    soup = BeautifulSoup(html, 'html.parser')
    if display_result:
        print(soup.prettify())
    return soup

def extracting_text(html):
    soup = soup_a(html)
    content_area = soup.find("div", {"class": content_area_class})
    text = content_area.text
    return text


blogpost_pattern = r'^/(?P<year>\d+){4}/(?P<month>\d+){2}/(?P<day>\d+){2}/(?P<slug>[\w-]+)/$'

def matching_path(path):
    pattern = re.compile(blogpost_pattern)
    matching = pattern.match(path)
    if  matching is None:
        return False, None
    return True, matching


def processing_string(string):
    string = string.replace("\n", " ")
    string = string.replace("—", "")
    string = string.replace("|", "")
    string = string.replace("\n", " ")
    string = string.replace("\"", "")
    string = string.replace("\xa0", " ")
    string = string.replace("“", "")
    string = string.replace("”", "")
    string = string.replace("–", "")
    string = string.replace(".", "")
    string = string.replace("?", "")
    string = string.replace(",", "")
    string = string.replace("'ve", " have")
    #string = string.replace(".", " || PERIOD ||")
    #string = string.replace("?", " || QUESTION_MARK ||")
    return string.strip()


def extracting_local_links(html, root_domain, local_only=True):
    soup = soup_a(html)
    href_tags = soup.find_all("a", href=True)
    links = [a['href'] for a in href_tags]
    if local_only:
        paths = []
        for x in links:
            if urlparse(x).netloc == root_domain:
                link = urlparse(x).path
                is_matching = matching_path(link)
                if is_matching[0]:
                    paths.append(link)
    return list(set(paths))



def main_sync(url):
    start_time = time.time()
    parsed_url = urlparse(url)
    root_domain = parsed_url.netloc
    domain = parsed_url.geturl() # includes trailing /
    #print(domain)
    html = fetch_url(url)
    paths = extracting_local_links(html, root_domain)
    #print(paths)
    words = []
    for path in list(set(paths)):
        start_ = time.time()
        post_url  = domain + path
        new_html = fetch_url(post_url)
        text = extracting_text(new_html)
        string = processing_string(text)
        sub_words = string.split()
        words += sub_words
        print(time.time() - start_, "seconds")
    word_freq = Counter(words)
    print("Entire request took", time.time()-start_time, "seconds")
    print(word_freq.most_common(10))



main_sync('http://tim.blog')
