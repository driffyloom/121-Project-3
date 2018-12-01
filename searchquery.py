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

print("Loading in inverted index. Please wait.")
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

#Added for Milestone 2: for each word in the query that matches a token in the
#inverted index, sort the token's doc list by tf-idf.
    #Higher tf-idf = rarer in collection, higher occurrances in doc
 
while searchQuery != "quit":
    print("Enter Search Query:")
    searchQuery = raw_input().lower().strip()
    queryWords = searchQuery.split()
    results = []
    if searchQuery == "quit":
        break
    if len(queryWords) == 1:
        if searchQuery in invertedIndex.keys():
            for key, value in sorted(invertedIndex[searchQuery].items(), key = lambda(x,y): y, reverse = True):
                #then print out the keys in the sorted, decreasing tf-idf order
                results.append(key)
                #print(+ " " + invertedIndex[searchQuery][key])
        else:
            print("No entries found for query: " + searchQuery)
    else: #query has multiple words and should take cosine into account too
        #UNFINISHEDDDDDDD
        print("No entries found for query: " + searchQuery)
        #DELETE THIS PRINT STATEMENT ONCE WE REPLACE ITTTT
    if len(results) > 10:
        for i in range(10):
            print(results[i])
    else:
        for key in results:
            print(key)

print("Inverted Index Length: " + str(len(invertedIndex)))
print("Total words: " + str(totalWords))
   
