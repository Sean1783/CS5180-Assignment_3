from db_manager import DatabaseManager
from content_parser import *
from crawler import *


database_name = 'web_crawler'
web_crawler_collection_name = 'page_data'
professor_info_collection_name = 'professors'
seed = 'https://www.cpp.edu/sci/computer-science/'
base_url = 'https://www.cpp.edu'
target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'


def crawler_test():
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, web_crawler_collection_name)
    crawler.crawl(seed, db_manager)


def parser_test():
    parser = Parser()
    db_manager = DatabaseManager(database_name, web_crawler_collection_name)
    extracted_info = parser.extract_info(target_url, db_manager)
    db_new_collection_manager = DatabaseManager(database_name, professor_info_collection_name)
    for item in extracted_info:
        db_new_collection_manager.insert_document_duplicate_accepted(item)
        print(item)


if __name__ == "__main__":
    crawler_test()
    parser_test()