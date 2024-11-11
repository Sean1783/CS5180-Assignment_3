from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, base_url, target_url):
        self.base_url = base_url
        self.target_url = target_url


    def visit_link_and_gather_anchor_tags(self, link_to_visit):
        html = None
        try:
            with urlopen(link_to_visit) as html:
                bs = BeautifulSoup(html.read(), 'html.parser')
                return bs.find_all('a')
        except HTTPError as e:
            print(f"HTTP error: {e}" + link_to_visit)
        except URLError as e:
            print(f"URL error: {e}" + link_to_visit)
        except Exception as e:
            print(f"An unexpected error occurred: {e}" + link_to_visit)
        return []


    def create_list_of_raw_links(self, unfiltered_url_list):
        filtered_url_list = []
        for individual_url in unfiltered_url_list:
            url_string = individual_url.get('href')
            if url_string and url_string.endswith(('.html', '.shtml')):
                filtered_url_list.append(url_string)
                # print(url_string)
        return filtered_url_list


    def construct_full_links(self, filtered_url_list):
        frontier_urls = set()
        for link in filtered_url_list:
            if self.is_correct_domain(link):
                if link.startswith('/'):
                    full_link = self.base_url + link
                elif link.startswith(self.base_url):
                    full_link = link
                else:
                    full_link = self.base_url + '/' + link
                # full_link = link if self.base_url in link else self.base_url + link
                # print(full_link)
                frontier_urls.add(full_link)
        return list(frontier_urls)


    def is_correct_domain(self, link):
        scheme = 'http://'
        scheme_secure = 'https://'
        if link.startswith(self.base_url):
            return True
        elif link.startswith(scheme) or link.startswith(scheme_secure):
            return False
        else:
            return True


    def generate_new_frontier_urls(self, current_link):
        anchor_tags = self.visit_link_and_gather_anchor_tags(current_link)
        raw_list = self.create_list_of_raw_links(anchor_tags)
        frontier = self.construct_full_links(raw_list)
        return frontier


    def is_target_link(self, current_link, link_to_find):
        return current_link == link_to_find


    def get_html(self, some_url_link):
        html = None
        try:
            with urlopen(some_url_link) as html:
                bs = BeautifulSoup(html.read(), 'html.parser')
                # return bs.body.prettify()
                return bs.prettify()
        except HTTPError as e:
            print(f"HTTP error: {e}" + some_url_link)
        except URLError as e:
            print(f"URL error: {e}" + some_url_link)
        except Exception as e:
            print(f"An unexpected error occurred: {e}" + some_url_link)
        return ""


    def crawl(self, seed_url, db_manager):
        base_frontier = self.generate_new_frontier_urls(seed_url)
        while base_frontier:
            link = base_frontier.pop(0)
            is_target = self.is_target_link(link, self.target_url)
            page_html = self.get_html(link)
            if page_html:
                db_manager.insert_document(link, page_html, is_target)
            if is_target:
                base_frontier.clear()
                return
            additional_frontier = self.generate_new_frontier_urls(link)
            for next_link in additional_frontier:
                if next_link not in base_frontier:
                    base_frontier.append(next_link)