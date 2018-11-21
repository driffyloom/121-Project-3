from bs4 import BeautifulSoup

htmlFile = open("6","r");

soup = BeautifulSoup(htmlFile,'html.parser')

"""
with open("6") as fp:
    soup = BeautifulSoup(fp)

soup = BeautifulSoup("<html>data</html")
"""

for script in soup.find_all('script'):
    script.extract()

for style in soup.find_all('style'):
    style.extract()
    
print(soup.get_text())
