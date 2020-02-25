import json
import re
import string

Head_Word = "Criminal"

key_words = [ "confidential informant", "informant"]

res = set() # avoid duplicate

with open('cases.json', 'r') as f:
    data = json.load(f)

for i, case in enumerate(data):

    for key in case:
        value = case[key]

        for text in value:
            # replace punctuation with space
            for c in string.punctuation:  
                text = text.replace(c, ' ')
            
            # split text with space
            words = text.split(' ')
            

            for w in words:
                # search keyword
                pattern = re.compile(r'informant',re.IGNORECASE)
                result = pattern.findall(w)

                if result != []:
                    res.add(i)
                    
                else:
                    pattern = re.compile(r'CI')
                    result = pattern.findall(w)
                    if result != []:
                        res.add(i)

print(len(res))