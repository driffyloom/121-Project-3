from bs4 import BeautifulSoup
import io
import os
import PartA
from math import log10
if __name__ == "__main__":
    #goes through all the files in the WEBPAGES_RAW folder and calculates their td-idf
    #THE INDEX PRINTOUT AT THE BOTTOM IS FORMATTED LIKE SO:
    '''
    <token>:
    Doc: <folder>.<file> -> Weight: <tf-idf>
    Doc: <folder>.<file> -> Weight: <tf-idf>
    '''
    #so a file with the full path C:\\Users\\Biancat\\Documents\\CS121-InfoRetrieval\\121-Project-3\\WEBPAGES_RAW\\0\\6
    #ends up with a docName of 0.6

    docFreq = dict() #{token:numberOfFilesTokenIsFoundIn}
    invertedIndex = dict() #token:dict{docID:tf-idf} A DICT WITH DICT VALUES
    numFiles = 0;
    try:
        for subdir, dirs, files in os.walk(os.getcwd()+'\WEBPAGES_RAW'):
            folderName = subdir[len(os.getcwd())+14:]
            for file in files:
                
                numFiles += 1
                filepath = subdir + os.sep + file
                docName = folderName + '.' + file
                
                #if("WEBPAGES_RAW\\0" in filepath): #== "C:\\Users\\Biancat\\Documents\\CS121-InfoRetrieval\\121-Project-3\\WEBPAGES_RAW\\0\\6"):
                #print(docName)
                
                with io.open(filepath, "r", encoding="utf8", errors='ignore') as fp:
                    soup = BeautifulSoup(fp)

                for script in soup.find_all('script'):
                    script.extract()

                for style in soup.find_all('style'):
                    style.extract()

                for href in soup.find_all('href'):
                    href.extract()

                #sortedFreq has the log-freq weighted term frequency: [item(token:weighted term freq)]
                #w = 1 + log10(tf)
                sortedFreq = PartA.outputFrequencies(soup.stripped_strings) 
                #calculate the tf-idf of each term, and stick it in the filesFreq
                for item in sortedFreq:
                    #fill in document frequency dict
                    if item[0] not in docFreq:
                        docFreq[item[0]] = 1
                    else:
                        docFreq[item[0]] += 1
                    if item[0] not in invertedIndex:
                        invertedIndex[item[0]] = dict({docName:item[1]*(log10(numFiles/docFreq[item[0]]))})
                    else: #token may be in there, but the doc is new, so add to the doc/tf-idf dict
                        #idf = log10(N/df)
                        #tf-idf = tf x idf
                        invertedIndex[item[0]][docName] = item[1]*(log10(numFiles/docFreq[item[0]]))

                '''
                for item in sortedFreq:
                    if item[0] not in fileFreq:
                        fileFreq[item[0]] = item[1]
                    else:
                        fileFreq[item[0]] += item[1]
                '''     
                '''
                for string in soup.stripped_strings:
                    print(string.encode("utf-8"))
                '''        
                fp.close()

    except IOError:
            print("File not found, or path is incorrect")
    except Exception as ex:
        print(ex.message)
    ''' #debugging prints
    for k,v in invertedIndex.items():
        print(k + ":" )
        for vk, vv in v.items():
            print('\tDoc: ' + vk + ' Weight: ' + str(vv))
    '''
    #sortedFileFreq = sorted(fileFreq.items(), key=lambda(k,v) : (-v,k)) #descending order of term frequencies
    #for item in sortedFileFreq:
        #print(item[0] + '\t' + str(item[1]))#Output: [token]\t[frequency]

    #write the index to a file in the format:
    '''
    <token>:
    <folder>.<file> <tf-idf weight>
    '''
    indexFile = open('invIndex.txt', 'w+')
    for k,v in invertedIndex.items():
        indexFile.write(k + ":\n")
        for vk, vv in v.items():
            indexFile.write(vk + " " + str(vv) + '\n')
    indexFile.close()
    print("Created index!")

    
    
