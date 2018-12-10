import re
from functools import reduce

_M = 'ျ ြ ွ ှ'
_V = 'ါ ာ ိ ီ ု ူ ေ ဲ'
_S = '္'
_A = '်'
_F = 'ံ ့ း'
_I = 'ဤ ဧ ဪ ၌ ၍ ၏'
_E = 'ဣ ဥ ဦ ဩ ၎'
_G = 'ဿ'
_D = '၀ ၁ ၂ ၃ ၄ ၅ ၆ ၇ ၈ ၉'
_P = '၊ ။'
_C = 'က ခ ဂ ဃ င စ ဆ ဇ ဈ ည ဋ ဌ ဍ ဎ ဏ တ ထ ဒ ဓ န  ပ ဖ ဗ ဘ မ ယ ရ လ ဝ သ ဟ ဠ အ'

M = _M.split()
V = _V.split()
S = _S.split()
A = _A.split()
F = _F.split()
I = _I.split()
E = _E.split()
G = _G.split()
D = _D.split()
P = _P.split()
C = _C.split()

rankingMap = {
  # M
  'ျ': 1,
  'ြ': 2,
  'ွ': 3,
  'ှ': 4,
  # V 
  'ေ': 5,
  'ါ': 6,
  'ာ': 7,
  'ိ': 8,
  'ီ': 9,
  'ု': 10,
  'ူ': 11,
  'ဲ': 12,
  # A
  '်': 13,
  # F
  'ံ': 14,
  '့': 15,
  'း': 16,
}

rules = {"၀":"ဝ",           #Zero to Wa lone
         "ဦ":"ဦ",           #U             
         "ဩော်":"ဪ",      #Aww
         "ိီ":"ီ",          #Debatable
         "ုူ":"ူ",          #Debatable
         "စျ":"ဈ"           #Debatable
        }


def segment(text):    
    regex = r'([\u1000-\u102a\u104c-\u104f](\u1039[\u1000-\u1021])*[\u102b-\u103e]*)'  
    matches = map(lambda x: x.group(),re.finditer(regex,text))
    return matches

def unify(array):
    if "္" in array:
        temp_arr = list(array)
        return list(temp_arr)
##        if len(temp_arr)== 3:
##            return list(temp_arr)
##        elif len(temp_arr)== 4:
##            print(temp_arr)
##            del temp_arr[2]
##            return list(temp_arr)
##        elif len(array) == 5:
##            print(temp_arr)
##            del temp_arr[3]
##            return list(temp_arr)
    else:
        return list(set(array))

def replacerules(txtStr):
    input = txtStr
    output = ""

    #'၀ ဝ', 'ဦ ဦ', 'ဩော် ဪ', 'ိီ ီ', 'ုူ ူ', 'စျ ဈ'
    for i in rules.keys():
        if i in input:
            print("this is rules key")
            temp = input.split(i)
            output = temp[0]+rules[i]+temp[1]

    #virama space
    if "္" in i:
        if " " in i:
            #print("this is virama")
            t = i.split()
            output = reduce(lambda x,y: x+y, t)
    else: output= txtStr
            
    return output

def reordering(txtStr):
    temp = list(txtStr)
    #print("this is reordering temp",temp)
    rank = {}
    result = []
    if "္" not in temp:
        #print("I am not virama")
        for t in temp:        
            if t in C:
                rank[t] = 0
            elif t in rankingMap.keys():
                rank[t] = rankingMap[t]            
            else: rank[t] = 0
        for val in sorted(rank.values()):
            for key in rank.keys():
                if val == rank[key]:
                    result.append(key)
    else:
        
        result = temp
##    print(result)
    
    r = reduce(lambda x,y: x+y, result)
    return r

def main(txtstring):
    sylls = []
    sylls.extend(segment(txtstring))
    #print(sylls)
    sylls = [unify(s) for s in sylls]
    #print("unify",sylls)
    sylls = [replacerules(s) for s in sylls]
    #print("replace",sylls)
    sylls = [reordering(s)for s in sylls]
    ##print("-------------------------------")
    #print("reordering",sylls)
    r = reduce(lambda x,y: x+y, sylls)
    #print("this is r: ",r)
    return r

def main2():
    txtstring = input("Type Any String: ")
    sylls = []
    sylls.extend(segment(txtstring))
    print(len(sylls))
    sylls = [unify(s) for s in sylls]
    print("After unifying",len(sylls))
    sylls = [replacerules(s) for s in sylls]
    print("-------------------------------")
    sylls = [reordering(s)for s in sylls]
    r = reduce(lambda x,y: x+y, sylls)
    print()
    return r

    
    
    
        
    
    


    
    
    
    
