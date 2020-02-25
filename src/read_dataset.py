import json
import re
import string

Head_Word = "Criminal"

key_words = [ "confidential informant", "informant"]

res = set()

with open('cases.json', 'r') as f:
    data = json.load(f)

for i, case in enumerate(data):
    for key in case:
        value = case[key]

        for text in value:
            for c in string.punctuation:  
                text = text.replace(c, ' ')
    
            words = text.split(' ')
            
            for w in words:
                pattern = re.compile(r'informant',re.IGNORECASE)
                
                result = pattern.findall(w)

                if result!=[]:
                    res.add(i)
                else:
                    pattern = re.compile(r'CI')
                    result = pattern.findall(w)
                    if result!=[]:
                        res.add(i)

print(len(res))