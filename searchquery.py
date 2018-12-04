import string
import sys
import re
import io
import heapq
import math
from Tkinter import *
import webbrowser

searchQuery = ""

totalWords = 0
docFreq = dict() #{token:numberOfFilesTokenIsFoundIn}
invertedIndex = dict() #token:dict{docID:tf-idf} A DICT WITH DICT VALUES
searchResultDict = dict() #token:dict{url:tf-idf}
indexElimination = dict() #number of words in a doc matching


#opens file and creates dictionary from inverted index file
invertedIndexFile = io.open("invIndex.txt","r", encoding = 'utf8', errors = 'ignore')
singleLine = invertedIndexFile.readline()

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))
    
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

#load in the bookkeeping information so we can look up the URLs for each folder.file key
urls = dict()

bookkeepingFile = io.open("WEBPAGES_RAW/bookkeeping.json", "r", encoding = 'utf-8', errors = 'ignore')
urlLine = bookkeepingFile.readline() #skip this line since it's just {
urlLine = bookkeepingFile.readline()
print("Loading in bookkeeping URLs. Please wait.")
while urlLine:
    allTokens = re.split(':', urlLine.encode('utf-8'))
    if allTokens[0] == "}":
        urlLine = bookkeepingFile.readline()
        break
    urls[allTokens[0].strip().strip('"').replace('/', '.')] = allTokens[1].strip().strip('",')
    urlLine = bookkeepingFile.readline()
''' #this is for debugging
for key in urls.keys():
    print(key + " " + urls[key])
''' 

#Added for Milestone 2: for each word in the query that matches a token in the
#inverted index, sort the token's doc list by tf-idf.
    #Higher tf-idf = rarer in collection, higher occurrances in doc

print("Inverted Index Length: " + str(len(invertedIndex)))
print("Total words: " + str(totalWords))


class Application(Frame):

    def search(self):
        searchQuery = self.e1.get().lower().strip()
        queryWords = searchQuery.split()
        results = []
        if len(queryWords) == 1:
            if searchQuery in invertedIndex.keys():
                count = 0
                for key, value in sorted(invertedIndex[searchQuery].items(), key = lambda(x,y): y, reverse = True):
                    #then print out the keys in the sorted, decreasing tf-idf order
                    results.append(key)
                    count+=1
                    if count == 10:
                        break;
                    #print(+ " " + invertedIndex[searchQuery][key])
            else:
                print("No entries found for query: " + searchQuery)
        else: #query has multiple words and should take cosine into account too
            for word in searchQuery.split():
             
                if word in invertedIndex.keys():

                        
                    for url in invertedIndex[word]:
                        if url in invertedIndex.keys():  
                            searchResultDict[url] += invertedIndex[word][url]
                        else:
                            searchResultDict[url] = invertedIndex[word][url]
                        if url in indexElimination.keys():  
                            indexElimination[url] += 1
                        else:
                            indexElimination[url] = 1

                        
            count = 0
            for key, value in sorted(searchResultDict.items(), key = lambda(x,y): y, reverse = True):
                #then print out the keys in the sorted, decreasing tf-idf order
                if (len(searchQuery.split()) >= 4):
                    if(float(indexElimination[key])*.75)>= (float(len(searchQuery.split())*.75)):
                        results.append(key)
                        #print(key + " " + value)
                        count+=1
                        if count == 10:
                            break;
                else:
                    results.append(key)
                    #print(key + " " + value)
                    count+=1
                    if count == 10:
                        break;

        indexElimination.clear()
        searchResultDict.clear()

        if(len(self.labels)>0):
            for label in self.labels:
                label.destroy()
            self.labels = []
            
        searchString = ""

        searchResultLabel = Label(root, text = "Search Results:")
        searchResultLabel.pack()
        
        for key in results:
            lbl = Label(root, text=urls[key], fg="blue", cursor="hand2")
            lbl.pack()
            lbl.bind("<Button-1>", callback)
            self.labels.append(lbl)
            #print(urls[key] + " (Folder.file: " + key + ")" )

        #configuring a tag with a certain style (font color)
        #self.searchResults.tag_configure("blue", foreground="blue")
        

    def createWidgets(self):
        self.MOOGLE = Label(root, text = "MOOGLE SEARCH")
        self.MOOGLE.pack({"side": "top"})

        self.e1 = Entry(root)
        self.e1.pack({"side": "top"})
        
        self.searchButton = Button(self)
        self.searchButton["text"] = "Search"
        self.searchButton["command"] = self.search
            
        self.searchButton.pack({"side": "left"})
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "right"})



    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.labels = []
        self.pack()
        self.createWidgets()

root = Tk()

root.title("SEARCH ENGINE")

root.geometry("800x400")

root.configure(background = 'black')
            
app = Application(master=root)
app.mainloop()
root.destroy()

   
