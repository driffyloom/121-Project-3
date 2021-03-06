from bs4 import BeautifulSoup
import io
import os
import PartA
from math import log10
import string
from collections import defaultdict


if __name__ == "__main__":
    #goes through all the files in the WEBPAGES_RAW folder and calculates their td-idf
    #THE INDEX PRINTOUT AT THE BOTTOM IS FORMATTED LIKE SO:
    '''
    <token>:
    Doc: <folder>/<file> -> Weight: <tf-idf>
    Doc: <folder>/<file> -> Weight: <tf-idf>
    '''
    
    docFreq = defaultdict() #{token:numberOfFilesTokenIsFoundIn}
    invertedIndex = defaultdict() #token:dict{docID:tf-idf} A DICT WITH DICT VALUES
    numFiles = 0;
    snippetsDict = defaultdict() #{docID:title)
    try:
        for subdir, dirs, files in os.walk(os.getcwd()+'\WEBPAGES_RAW'):
            folderName = subdir[len(os.getcwd())+14:]
            for file in files:
                numFiles += 1 
                filepath = subdir + os.sep + file
                docName = folderName + '/' + file
                
                with io.open(filepath, "r", encoding="utf8", errors='ignore') as fp:
                    soup = BeautifulSoup(fp)

                for script in soup.find_all('script'):
                    script.extract()

                for style in soup.find_all('style'):
                    style.extract()

                for href in soup.find_all('href'):
                    href.extract()
                
                #grab the title
                if soup.title != None:
                    title = ''
                    titleWords = str(soup.title).strip("<title>").strip("</title>").replace('<',' <').replace('>', '> ').strip().split()
                    for word in titleWords:
                        if word[0] != '<':
                            for letter in word:
                                if letter in string.printable: #take out any characters that aren't A-Z or 0-9 for easier reading
                                    title += letter
                            title += " "
                    if (title.strip() != "" and title.strip() != " "):
                        snippetsDict[docName] = title.strip()
                        print(title.strip())
                
                #sortedFreq has the log-freq weighted term frequency for EACH term in one file: [item(token:weighted term freq)]
                #w = 1 + log10(tf)
                freq = PartA.outputFrequencies(soup.stripped_strings)
                for item in freq:
                    #fill in document frequency dict
                    if item[0] not in docFreq:
                        docFreq[item[0]] = 1
                    else:
                        docFreq[item[0]] += 1
                    if item[0] not in invertedIndex:
                        invertedIndex[item[0]] = dict({docName:item[1]}) #for now, store tf. Then, after we know how total docs, calc and mult. by IDF
                    else: #token may be in there, but the doc is new       
                        invertedIndex[item[0]][docName] = item[1]
                
                fp.close()
#-----------------------------------------------------------------------------------------
#GENERATE THE TF-IDF FOR EACH DOCUMENT IN EACH TOKEN DICT
#note: the tf is already stored for each document. Just multiply it by idf
        
        print("Going through and calculating tf-idfs")
        for token, docDict in invertedIndex.items():
            #idf = log10(N/df)
            #tf-idf = tf x idf
            for docID, tf in docDict.items():
                docDict[docID] = tf * log10(numFiles/docFreq[token])
        print("Calculated tf-idfs")
        
    except IOError:
            print("File not found, or path is incorrect")
    except Exception as ex:
        print(ex.message)
        
#----------------------------------------------------------------------------------------
#FILE WRITING: INVERTED INDEX AND SNIPPETS (TITLES IF THEY EXIST) DICT
    
    #write the index to a file in the format:
    '''
    #<token>:
    #<folder>/<file> <tf-idf weight>
    '''
    indexFile = open('invIndex.txt', 'w+')
    for k,v in invertedIndex.items():
        indexFile.write(k + ":\n")
        for vk, vv in v.items():
            indexFile.write(vk + " " + str(vv) + '\n')
    indexFile.close()
    print("Created index!")

    
    #write snippetsDict to a file in the format:
    '''
    <folder>/<file> title
    '''
    snippetsFile = open('snippets.txt', 'w+')
    for k,v in snippetsDict.items(): #k is docName, v is title
        snippetsFile.write(k + " " +  v + "\n")
    snippetsFile.close()
    print("Created snippets file!")

