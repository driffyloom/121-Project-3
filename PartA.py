#Bianca Tang (biancat1) (38478644)
#CS 112 Assignment 1 - Text Processing functions
#Repurposed for Assignment 3

#Part A: Word Frequencies

#Write a program that takes a text file as a command line arg and outputs the word frequency
#in decreasing order.
#Functionality:
    #Read input file passed as command line arg
    #Tokenize (token - sequence of alphanumeric chars, independent of capitalization)
    #Counts the number of occurrences of ech word in the tokens generated
    #Prints out the word frequency ordered by decreasing frequency. Resolve ties alphabetically
#Should work for bad inputs -> error handling -> skip the bad inputs and continue with the rest
#Should work for files that are too big to fit in memory

#----------------------------------------------------------------------------------------------
#COMPLEXITY: O(n log n)time. Finding the frequency of each word in the file is O(n), but sorting
#           the dictionary entries takes O(nlogn) time with sorted, 
#----------------------------------------------------------------------------------------------
import sys, io, string, re
from bs4 import BeautifulSoup
from math import log10
from nltk.corpus import stopwords

def replacePunc(s): #no punctuation or any weird non english characters
    #print('s: ' + s)
    newS = ''
    isAllNums = True
    if (len(s) > 28) or (len(s) < 3): #longest non-technical, non-coined english word is 28 letters long
        return " "
    for char in s:
        try:
            #print('char: ' + char)
            if (char in string.letters):
                isAllNums = False
                newS += char
            elif (char in string.digits):
                newS += char
            else:
                newS += ' '
        except Exception:
            continue
    if isAllNums == True and len(newS) < 11: #skip any tokens that are JUST numbers
        return " "
    else:
        return newS

def outputFrequencies(f): #f is the string gen (whole file)
    freq = dict()
    sws = set(stopwords.words('english'))
    for string in f:
        try:
            lLine = string.lower().encode("utf-8") #get rid of all capitalization
            #print('Lower line: ' + lLine)
            sLine = replacePunc(lLine) #replace punctuation with spaces
            #print('Spaced line: ' + sLine)
            words = sLine.strip().split() #separates at whitespaces
            #print(words)
            for word in words:
                if word not in sws and len(word) > 2 and len(word) < 29:
                    #INDEXING IMPROVEMENT -> take out stopwords using nltk given stopwords list
                    #take out words that are 2 letters or less
                    #the longest non-coined, non-technical word is 28 letters long (according to Wikipedia)
                    #print(word)
                    try:
                        if word not in freq:
                            freq[word] = 1
                        else:
                            freq[word] += 1
                    except Exception:
                        continue
        except Exception as ex:
            print(ex.message)
    #sort the dictionary
    for k,v in freq.items(): #do log-frequency weighting on the term frequency
        freq[k] = 1 + log10(v)
    sortedFreq = sorted(freq.items(), key=lambda(k,v): (-v,k))
    #for item in sortedFreq:
        #print(item[0] + '\t' + str(item[1]))#Output: [token]\t[frequency]
    return sortedFreq #total frequency of a term in the doc
    

if __name__ == "__main__":
    fileFreq = dict() 
    try:
        inputFile = sys.argv[1]
        f = io.open(inputFile, mode='r', encoding='utf-8', errors='ignore')
        #lines here are added from searchengine.py
        soup = BeautifulSoup(f, 'html.parser')
        for script in soup.find_all('script'):
            script.extract()
        for style in soup.find_all('style'):
            style.extract()
        for href in soup.find_all('href'):
            href.extract()
        sortedFreq = outputFrequencies(soup.stripped_strings)
        for item in sortedFreq:
            if item[0] not in fileFreq:
                fileFreq[item[0]] = item[1]
            else:
                fileFreq[item[0]] += item[1]
        sortedFileFreq = sorted(fileFreq.items(), key=lambda(k,v) : (-v,k))
        for item in sortedFileFreq:
            print(item[0] + '\t' + str(item[1]))#Output: [token]\t[frequency]
        f.close()
    except IOError:
        print("File not found, or path is incorrect")
    except Exception as ex:
        print(ex.message)
