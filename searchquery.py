import string
import sys
import re
import io
import heapq

searchQuery = ""

totalWords = 0
docFreq = dict() #{token:numberOfFilesTokenIsFoundIn}
invertedIndex = dict() #token:dict{docID:tf-idf} A DICT WITH DICT VALUES


#opens file and creates dictionary from inverted index file
invertedIndexFile = io.open("invIndex.txt","r", encoding = 'utf8', errors = 'ignore')
singleLine = invertedIndexFile.readline()
       
while singleLine:
    allTokensInLine = re.split(' ',singleLine.encode('utf8'))
    count = 0
    for token in allTokensInLine:
        if token[len(token)-2] == ":":
            indexToken = token[:(len(token)-2)]
            invertedIndex[indexToken[:(len(token)-2)]] = dict()
            totalWords += 1
            break
                          
        if count == 0:
            docName = token

        if count == 1:
            invertedIndex[indexToken][docName] = token.strip()

        count += 1
                          
    singleLine = invertedIndexFile.readline()
 
while searchQuery != "quit":
    print("Enter Search Query:")
    searchQuery = raw_input().lower().strip()
    print(len(invertedIndex[searchQuery]))
    

print(len(invertedIndex))
print(totalWords)
   
