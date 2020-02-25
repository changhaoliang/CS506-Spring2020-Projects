import json
import re
import pprint
dict = {}

Head_Word = "Criminal"
Words = [ "confidential informant", "informant"]
A=set([])
B=set([])
C=[]

filteredCases = []
with open('cases.json', 'r') as f:
    cases = json.load(f)

with open('cases_appeals.json', 'r') as f:
    cases_appeals = json.load(f)

for i, case in enumerate(cases):
    for key in case:
        if key == "headnote" :
            for headnote in case[key]:
                if "Criminal" in headnote:
                    filteredCases.append(cases[i])

for i, case in enumerate(cases_appeals):
    for key in case:
        if key == "headnote" :
            for headnote in case[key]:
                if "Criminal" in headnote:
                    filteredCases.append(cases_appeals[i])

for i, case in enumerate(filteredCases):
    for key in case:
        for text in case[key]:
            words = text.split(' ')
            for word in words:
                pattern = re.compile(r'informant',re.IGNORECASE)
                result = pattern.findall(word)
                if result!=[]:
                    A.add(i)
                else:
                    pattern = re.compile(r'CI')
                    result = pattern.findall(word)
                    if result!=[]:
                        A.add(i)


print(len(A))
