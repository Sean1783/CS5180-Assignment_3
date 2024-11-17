from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# Open the local HTML file
with open("../page.html", "r") as file:
    html_content = file.read()

# Create a BeautifulSoup object
bs = BeautifulSoup(html_content, "html.parser")

print('#4.a.')
print(bs.find('title').text)

# b. The text of the second list item element <li> below "To show off"? Use the HTML tags
# to do this search. The output should be "To my friends".
print('#4.b.')
elements = bs.find_all('li')
print(elements[3].text)

print('#4.c.')
td_tags = bs.find('table').find('tr').find_all('td')

for tag in td_tags:
    print(tag)

print('#4.d.')
regex = re.compile('tutorial')
tutorial = bs.find_all('h2', string=regex)
for element in tutorial:
    print(element.text)

print('#4.e.')
#   All text that includes the “HTML” word. Use the HTML
#   text to do this search.
regex = re.compile('HTML')
html_text = bs.find_all(string=regex)
for example in html_text:
    print(example.text)

print('#4.f.')
# All text in the second row <tr> of the table.
# Use the HTML tags to do this search.
tr_text = bs.find_all('tr')[1]
print(tr_text.text)

print('#4.g.')
# All <img> tags from the table. Use the HTML tags to do this search.
img_tags = bs.table.find_all("img")
print(img_tags)
