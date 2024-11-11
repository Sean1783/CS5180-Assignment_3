from bs4 import BeautifulSoup
from db_manager import *
import re


class Parser:
    def __init__(self):
        pass

    def extract_info(self, page_url, db_manager):
        content_string = db_manager.get_document_html(page_url)
        profile_info = list()

        if not content_string or "html" not in content_string:
            print("Error: 'html' content not found in the document.")
            return None

        try:
            bs = BeautifulSoup(content_string["html"], 'html.parser')
            target_objects = bs.find_all(class_='clearfix')

            if target_objects is None:
                print("Error: No target objects found with class 'clearfix'.")
                return None

            for current_obj in target_objects:
                current_profile = dict()

                name = current_obj.find('h2')
                if name:
                    current_profile['Name'] = name.get_text().strip()
                else:
                    print("Warning: Name tag (<h2>) not found for a profile.")
                    continue

                email = ''
                website = ''

                web_contact_info = current_obj.find_all('a', href=True)
                if len(web_contact_info) >= 2:
                    web_contact_info = current_obj.find_all('a')
                    email = web_contact_info[0].get_text().strip()
                    website = web_contact_info[1].get_text().strip()
                    # current_profile['Email'] = web_contact_info[0].get_text().strip()
                    # current_profile['Web'] = web_contact_info[1].get('href')
                else:
                    print("Warning: Insufficient web contact information found.")

                additional_details = current_obj.find_all('strong')
                for detail in additional_details:
                    # category = detail.get_text(strip=True)
                    # sibling = detail.next_sibling
                    # value = sibling.strip() if sibling else None
                    # if category and value:
                    #     current_profile[category.replace(":", "")] = value  # Clean up the category key
                    category = detail.get_text().strip()
                    if re.match(r'^Email:?', category):
                        current_profile[category] = email
                    elif re.match(r'^Web:?', category):
                        current_profile[category] = website
                    else:
                        value = detail.next_sibling.strip()
                        current_profile[category] = value
                profile_info.append(current_profile)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        return profile_info


    def get_source_body(self, page_url, db_manager):
        content_string = db_manager.get_document_html(page_url)
        try:
            bs = BeautifulSoup(content_string["html"], 'html.parser')
        except AttributeError as e:
            return None
        return bs.body.prettify()


    def get_tag_content(self, content):
        bs = BeautifulSoup(content, 'html.parser')
        return bs.find_all(class_='clearfix')


    def get_names(self, list_of_tag_obj):
        tag_obj = list_of_tag_obj[0]
        # print(tag_obj)
        print(tag_obj.find('h2'))
        # print(tag_obj.find_all('strong'), tag_obj.find('strong').next_siblings)
        try:
            print(tag_obj.find('strong', text='Title').next_sibling)
        except AttributeError as e:
            return None


    def get_title_content(self, content):
        if not content:
            return []  # Return an empty list if content is None or empty
        bs = BeautifulSoup(content, 'html.parser')
        titles = bs.find_all(text=re.compile(r'Title'))  # Matches any text containing 'Title'
        return titles