from bs4 import BeautifulSoup
import io
import os


for subdir, dirs, files in os.walk(os.getcwd()+'\WEBPAGES_RAW'):
    for file in files:
        
        filepath = subdir + os.sep + file
        
        if(filepath == "C:\\Users\\Austin\\Desktop\\121-Project-3\\WEBPAGES_RAW\\0\\6"):
            print(filepath)
            
            with io.open(filepath, "r", encoding="utf8", errors='ignore') as fp:
                soup = BeautifulSoup(fp)

            for script in soup.find_all('script'):
                script.extract()

            for style in soup.find_all('style'):
                style.extract()

            for href in soup.find_all('href'):
                href.extract()

            """
            for string in soup.stripped_strings:
                print(string.encode("utf-8"))
            """

            fp.close()



