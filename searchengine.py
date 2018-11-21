from bs4 import BeautifulSoup
import io


htmlFile = open("6","r");

with io.open("6", "r", encoding="utf-8", errors='ignore') as fp:
    soup = BeautifulSoup(fp)

for script in soup.find_all('script'):
    script.extract()

for style in soup.find_all('style'):
    style.extract()

for href in soup.find_all('href'):
    href.extract()

print(soup.get_text().encode("utf-8"))
for string in soup.stripped_strings:
    print(string.encode("utf-8"))

fp.close()
