from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# html = urlopen('http://www.pythonscraping.com/pages/page1.html')
# bs = BeautifulSoup(html.read(), 'html.parser')

# Open the local HTML file
with open("../page.html", "r") as file:
    html_content = file.read()

# Create a BeautifulSoup object
bs = BeautifulSoup(html_content, "html.parser")



#4.a.
print(bs.find('title').text)

# b. The text of the second list item element <li> below "To show off"? Use the HTML tags
# to do this search. The output should be "To my friends".
elements = bs.find_all('li')
print(elements[3].text)
elements = bs.body.ul.find_all('li')[3]
print(elements.text)

# c.
td_tags = bs.find('table').find('tr').find_all('td')

for tag in td_tags:
    print(tag)

# d.
regex = re.compile('tutorial')
tutorial = bs.find_all('h2', string=regex)
for element in tutorial:
    print(element.text)

# e.
#   All text that includes the “HTML” word. Use the HTML
#   text to do this search.
regex = re.compile('HTML')
html_text = bs.find_all(string=regex)
for example in html_text:
    print(example.text)

# f.
# All text in the second row <tr> of the table.
# Use the HTML tags to do this search.
tr_text = bs.find_all('tr')[1]
print(tr_text.text)

# g.
# All <img> tags from the table. Use the HTML tags to do this search.
img_tags = bs.table.find_all("img")
print(img_tags)







#
# all_hrefs = bs.find_all(href=True)
# print(all_hrefs)
#
# elements = bs.find('body').find('table').find_all('td')
# for element in elements:
#     print(element.text)
#
#
# # find all weblinks.
# a_tags = bs.find_all('a')
# for a_tag in a_tags:
#     print(a_tag.get('href'))
#
#
# # find all URLs
# all_URLs = bs.find_all('a')
# for URL in all_URLs:
#     print(URL.get('href'))
#
# # find all image src URLs
# all_image_tags = bs.find_all('img')
# for image_tag in all_image_tags:
#     print(image_tag.get('src'))
#
#
# # https://www.cpp.edu/sci/computer-science/
#
# html = urlopen('https://www.cpp.edu/sci/computer-science/')
# bs = BeautifulSoup(html.read(), 'html.parser')
#
# frontier = []
#
# regex_one = '.shtml$'
# regex_three = '(?!^https://www.cpp.edu)'
# all_urls = bs.find_all('a')
# for individual_url in all_urls:
#     url_string = individual_url.get('href')
#     target_one = re.findall(regex_one, url_string)
#     if target_one:
#         # print(individual_url.get('href'))
#         target_three = re.findall(regex_three, individual_url.get('href'))
#         if not target_three:
#             print(individual_url.get('href'))
#         if not target_three:
#             absolute_url = 'https://www.cpp.edu' + individual_url.get('href')
#             if absolute_url not in frontier:
#                 frontier.append(individual_url.get('href'))
#         elif url_string not in frontier:
#             frontier.append(url_string)
#
# for url in frontier:
#     print(url)
#
#
