import string
import sys
import re
import io
import heapq
import math
from Tkinter import *
import webbrowser
from collections import defaultdict

searchQuery = ""

totalWords = 0
invertedIndex = defaultdict() #token:dict{docID:tf-idf} A DICT WITH DICT VALUES
searchResultDict = defaultdict() #token:dict{url:tf-idf}
snippetsDict = defaultdict()

#------------------------------------------------------------------------------------------
#TITLE SNIPPETS READING
#opens snippets file and creates the snippetsDict from it -> file of Title tags
'''
Snippets file format:
<folder>/<file> title
'''
snippetsFile = io.open("snippets.txt", "r", encoding = 'utf8', errors = 'ignore')
oneSnippet = snippetsFile.readline()
print("Loading in search result snippets. Please wait.")
while oneSnippet:
    title = ""
    snippetTokens = re.split(' ', oneSnippet.encode('utf8'))
    for word in snippetTokens[1:]:
        title += word + " "
    snippetsDict[snippetTokens[0]] = title.strip()
    oneSnippet = snippetsFile.readline()

#-------------------------------------------------------------------------------------------
#INVERTED INDEX READING
#opens file and creates dictionary from inverted index file
invertedIndexFile = io.open("invIndex.txt","r", encoding = 'utf8', errors = 'ignore')
singleLine = invertedIndexFile.readline()

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))
    
print("Loading in inverted index. Please wait.")
'''
Inverted index file format:
<token>:
<folder>/<file> <tf-idf weight>
'''
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
            invertedIndex[indexToken][docName] = float(token.strip())

        count += 1
                          
    singleLine = invertedIndexFile.readline()

#----------------------------------------------------------------------------------------------
#URL TO FOLDER.FILE MAPPING THROUGH BOOKKEEPING.JSON
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
    urls[allTokens[0].strip().strip('"')] = allTokens[1].strip().strip('",')
    urlLine = bookkeepingFile.readline()

#Added for Milestone 2: for each word in the query that matches a token in the
#inverted index, sort the token's doc list by tf-idf.
    #Higher tf-idf = rarer in collection, higher occurrances in doc

print("Inverted Index Length: " + str(len(invertedIndex)))
print("Total words: " + str(totalWords))

#---------------------------------------------------------------------------------------------
#TKINTER GUI, SEARCHING

class Application(Frame):

    def search(self):
        searchQuery = self.e1.get().lower().strip()
        queryWords = searchQuery.split()
        results = []
        if len(queryWords) == 1:
            if searchQuery in invertedIndex.keys():
                count = 0
                for key, value in sorted(invertedIndex[searchQuery].items(), key = lambda(x,y): (-y,x)):
                    #then print out the keys in the sorted, decreasing tf-idf order
                    results.append(key)
                    count+=1
                    if count == 10:
                        break;
                    #print(+ " " + invertedIndex[searchQuery][key])
            else:
                print("No entries found for query: " + searchQuery)
        else: #query has multiple words
            for word in searchQuery.split():
                if word in invertedIndex.keys():
                    for url in invertedIndex[word]:
                        if url in searchResultDict.keys():  
                            searchResultDict[url] = searchResultDict[url] + invertedIndex[word][url]
                        else:
                            searchResultDict[url] = invertedIndex[word][url]
                        
            count = 0
            for key, value in sorted(searchResultDict.items(), key = lambda(x,y):(-y,x)):
                #then print out the keys in the sorted, decreasing tf-idf order
                results.append(key)
                #print(key + " " + str(value))
                count+=1
                if count == 10:
                    break;

        searchResultDict.clear()

        if(len(self.labels)>0):
            for label in self.labels:
                label.destroy()
            self.labels = []
            
        searchString = ""

        searchResultLabel = Label(root, text = "Search Results:")
        searchResultLabel.pack()
        self.labels.append(searchResultLabel)
        count = 1        
        for key in results: #creates hyperlinks?
            #FOR NOW, JUST PRINT TITLE SNIPPET OUT ONTO CONSOLE. MOVE INTO GUI LATER
            #print(snippetsDict[key])
            titleLabel = Label(root, text=str(count) + ".) " + snippetsDict[key])
            count+=1
            titleLabel.pack()
            self.labels.append(titleLabel)
            lbl = Label(root, text=urls[key], fg="blue", cursor="hand2")
            lbl.pack()
            lbl.bind("<Button-1>", callback)
            self.labels.append(lbl)
            #print(urls[key] + " (Folder.file: " + key + ")")
        

    def createWidgets(self): #creates button layouts, text box layouts
        self.MOOGLE = Label(root, text = "MOOGLE SEARCH")
        self.MOOGLE.pack(side="top",padx=20, pady=20)

        self.e1 = Entry(root)
        self.e1.pack(side="top",padx=20, pady=20, anchor = "center")
        
        self.searchButton = Button(self)
        self.searchButton["text"] = "Search"
        self.searchButton["command"] = self.search
        self.searchButton.pack(side="bottom",anchor = "center")
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack(side="top",anchor = "center")
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.labels = []
        self.pack()
        self.createWidgets()

root = Tk()

root.title("SEARCH ENGINE")

root.geometry("800x650")

root.configure(background = 'black')
            
app = Application(master=root)
app.mainloop()
root.destroy()

   
