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
import sys, io, string

def replacePunc(s): #no punctuation or any weird non english characters
    newS = ''
    for char in s:
        if char in string.letters or char in string.digits:
            newS += char
        else:
            newS += ' '
    return newS

def outputFrequencies(f): #f is the input file
    freq = dict()
    for line in f: #/n is the default EOL in Python
        try:
            lLine = line.lower() #get rid of all capitalization
            sLine = replacePunc(lLine) #replace punctuation with spaces
            words = sLine.split() #separates at whitespaces
            for word in words:
                try:
                    if word not in freq:
                        freq[word] = 1
                    else:
                        freq[word] += 1
                except Exception:
                    continue
        except Exception:
            continue
    #sort the dictionary
    sortedFreq = sorted(freq.items(), key=lambda(k,v): (-v,k))
    for item in sortedFreq:
        print(item[0] + '\t' + str(item[1]))#Output: [token]\t[frequency]
    

if __name__ == "__main__":
    try:
        inputFile = sys.argv[1]
        f = io.open(inputFile, mode='r', encoding='utf-8', errors='ignore')
        outputFrequencies(f)
        f.close()
    except IOError:
        print("File not found, or path is incorrect")
    except Exception as ex:
        print(ex.message)
    
