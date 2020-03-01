import json
import re
import pprint

Head_Word = "Criminal"
Words = [ "confidential informant", "informant"]
res = set([])

filteredCases = []
with open('./src/cases.json', 'r') as f:
    cases = json.load(f)
'''
    cases is a list[]
    each element cases[i] is a dict
        keys: case, headnote, text
            @ case: [' ', 'COMMONWEALTH vs. ADMILSON RESENDE']
            @ 
'''
print(cases[0]['headnote'])
# with open('cases_appeals.json', 'r') as f:
#     cases_appeals = json.load(f)

# for i, case in enumerate(cases):
#     for key in case:
#         if key == "headnote" :
#             for headnote in case[key]:
#                 if Head_Word in headnote:
#                     filteredCases.append(cases[i])

# for i, case in enumerate(cases_appeals):
#     for key in case:
#         if key == "headnote" :
#             for headnote in case[key]:
#                 if Head_Word in headnote:
#                     filteredCases.append(cases_appeals[i])

# for i, case in enumerate(filteredCases):
#     for key in case:
#         for text in case[key]:
#             words = text.split(' ')
#             for word in words:
#                 pattern = re.compile(r'informant',re.IGNORECASE)
#                 result = pattern.findall(word)
#                 if result!=[]:
#                     res.add(i)
#                 else:
#                     pattern = re.compile(r'CI')
#                     result = pattern.findall(word)
#                     if result!=[]:
#                         res.add(i)

# print(len(res))
