from crawler import *
from db_manager import *

def main():
    database_name = 'web_crawler'
    collection_name = 'page_data'
    seed = 'https://www.cpp.edu/sci/computer-science/'
    base_url = 'https://www.cpp.edu'
    target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/faculty-research-int.shtml'
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, collection_name)
    crawler.crawl(seed, db_manager)

if __name__ == "__main__":
    main()