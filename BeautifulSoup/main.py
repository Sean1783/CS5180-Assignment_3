from crawler import *
from db_manager import *
from content_parser import*


database_name = 'web_crawler'
collection_name = 'page_data'
seed = 'https://www.cpp.edu/sci/computer-science/'
base_url = 'https://www.cpp.edu'
target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'


def main():
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, collection_name)
    crawler.crawl(seed, db_manager)


def parser_test():
    parser = Parser()
    db_manager = DatabaseManager(database_name, collection_name)
    # html_text = parser.get_source_body(target_url, db_manager)
    extracted_info = parser.extract_info(target_url, db_manager)
    for item in extracted_info:
        print(item)


if __name__ == "__main__":
    parser_test()
    # main()