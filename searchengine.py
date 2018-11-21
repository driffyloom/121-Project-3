from bs4 import BeautifulSoup



soup = BeautifulSoup(DOCNAME ,'html.parser')

print(soup.prettify())
