import re
from nltk import ngrams



#method call
result = []

def FileInitiation():
    wList = []
    stop_wordList = []
    bullyList = []
    fopen1 = open("./words_lists/wordlist.txt", encoding = 'utf8')
    fopen2 = open("./words_lists/stop_words.txt", encoding = 'utf8')
    fopen3 = open("./words_lists/bullywords.txt", encoding = 'utf8')
    
    wList.extend([t.strip() for t in fopen1.readlines()])
    wList.extend([t.strip() for t in fopen2.readlines()])
    wList.extend([t.strip() for t in fopen3.readlines()])

    stop_wordList.extend([t.strip() for t in fopen2.readlines()])
    bullyList.extend([t.strip() for t in fopen3.readlines()])
    #print("I am fileinitiation")

    return list(set(wList)),list(set(stop_wordList)),list(set(bullyList))

def NgramSplit(inputstring,matchlist):
    #print("I am NgramSplit")
    data = syllbreak(inputstring)
    text = inputstring
    temp = []
    
    val = tokenize(data,4,matchlist)
    
    if len(val['dd']) != 0:
        temp.extend(val['mm'])
        val1 = tokenize(val['dd'],3,matchlist)
        
        if len(val1['dd']) != 0:
            
            temp.extend(val1['mm'])
            val2 = tokenize(val1['dd'],2,matchlist)
            
            if len(val2['dd']) != 0:
                
                temp.extend(val2['mm'])
                #temp.extend(val2['dd'])
            else:
                var = ""
                
        else:
            temp.extend(val1['mm'])
    else:
        temp.extend(val['mm'])   
    
        
    for t in temp:
        if t in text:
            text = text.replace(t," "+t+" ")
            
    finallist = []
    tmpdict = {}
    for i,val in enumerate(text.split()):
        tmpdict[i] = val
    for i in tmpdict:
        
        if tmpdict[i] in temp:
            finallist.append(tmpdict[i])
        else:
            s = syllbreak(tmpdict[i])
            finallist.extend(s) 
    return finallist
    
    #change file name and path here
##    fffopen = open("./3seminorsegmentedfile.txt","a+",encoding = "utf-8-sig")
##    for rr in finallist:
##        fffopen.write(rr+"\n")

def tokenize(data,n,matchlist):
    #print("I am tokenize")
    FGMatch = []
    text = "".join(data)
    templist = []
    tt = ngrams(data,n)
    for aa in tt:                  
        i = "".join(aa)
        temp = ""
        
        ss = MatchText(i,matchlist)
        if ss['flag'] == True:
            #print(ss['val'])
            FGMatch.append(ss['val'])            
            temp = text.replace(ss['val'],'')
            text = temp
            templist.append(text)
            
        else:
            templist.append(text)
            continue
    
    try: 
        return {'dd':syllbreak(templist[-1]),'mm':FGMatch}
    except:
        return {'dd':data,'mm':FGMatch}
def syllbreak(text):
    #print("Syllbreak")
    text = re.sub(r'(?:(?<!္)([က-ဪဿ၊-၏]|[၀-၉]+|[^က-၏]+)(?![ှျ]?[့္်]))',r's\1',text).strip('s').split('s')   
    temp = text    
    return temp

def MatchText(text,matchlist):
    
    wordVal = {'flag':False, 'val':''}
    for w in matchlist:
        if text == w:
            wordVal['flag'] = True
            wordVal['val'] = text
        
    return wordVal

def removeStopWord(text,stopwordslist):
    vWord = text
    returnList = []       
    
    for v in vWord:
        if v in stopwordslist:
            continue
        else:
            returnList.append(v)

    tempp = ""
    for ff in returnList:
        if (len(returnList)>0):
            if ff == returnList[-1]:
                tempp += ff
            else:
                tempp += ff+" "
            
    return tempp

def TokenizeWithLSMA(text):
    res = []
    matchList,stopWordsList, bullyList = FileInitiation()
    #sentence = input("Input Text: ")
##    
##    fopen4 = open("./normalizedCleanData4.txt", encoding = 'utf-8-sig')
##
##    for sentence in fopen4.readlines():
##        sentence = sentence.rstrip()
##        s1 = NgramSplit(sentence)
##        s2 = removeStopWord(s1,stopWordsList)
##        
##        res.extend(s2)
##    fopen5 = open("./segmentedfile.txt","a+", encoding = 'utf-8-sig')
##    for r in res:
##        fopen5.write(r+"\n")

    text1 = text.strip()
    text2 = NgramSplit(text1,matchList)
    text3 = removeStopWord(text2,stopWordsList)
    return text3
##    ("Successfully Segmented")
