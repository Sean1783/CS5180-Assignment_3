from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from db_manager import *
from bs4 import BeautifulSoup

base_url = 'https://www.cpp.edu'
target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/faculty-research-int.shtml'
collection_name = 'page_data'

def visit_link_and_gather_anchor_tags(link_to_visit):
    try:
        html = urlopen(link_to_visit)
    except HTTPError as e:
        print(f"HTTP error: {e}")
    except URLError as e:
        print(f"URL error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        return bs.find_all('a')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def create_list_of_raw_links(unfiltered_url_list):
    filtered_url_list = []
    for individual_url in unfiltered_url_list:
        url_string = individual_url.get('href')
        if '.shtml' or 'html' in url_string:
            filtered_url_list.append(url_string)
    return filtered_url_list

def construct_valid_links(filtered_url_list):
    frontier_urls = []
    for valid_link in filtered_url_list:
        if base_url not in valid_link:
            reconstructed_link = base_url + valid_link
            if reconstructed_link not in frontier_urls:
                frontier_urls.append(reconstructed_link)
        else:
            if valid_link not in frontier_urls:
                frontier_urls.append(valid_link)
    return frontier_urls

def generate_new_frontier_urls(current_link):
    anchor_tags = visit_link_and_gather_anchor_tags(current_link)
    raw_list = create_list_of_raw_links(anchor_tags)
    frontier = construct_valid_links(raw_list)
    return frontier

def is_target_link(current_link, link_to_find):
    return current_link == link_to_find

def output_target_tag(current_link):
    html = urlopen(current_link)
    bs = BeautifulSoup(html.read(), 'html.parser')
    tag_data = bs.find_all('h1', {'class': 'cpp-h1'})
    print(tag_data)

def get_html(some_url_link):
    html = urlopen(some_url_link)
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs.body.prettify()

def crawler(seed_url):
    base_frontier = generate_new_frontier_urls(seed_url)
    while base_frontier:
        link = base_frontier.pop(0)
        is_target = is_target_link(link, target_url)
        insert_document_into_database(link, is_target)
        if is_target:
            base_frontier.clear()
            return
        additional_frontier = generate_new_frontier_urls(link)
        for new_link in additional_frontier:
            if new_link not in base_frontier:
                base_frontier.append(new_link)
        print(link)

def insert_document_into_database(url_string, is_target):
    db_connection = connect_to_database()
    collection = db_connection[collection_name]
    page_html = get_html(url_string)
    create_document(collection, url_string, page_html, is_target)
