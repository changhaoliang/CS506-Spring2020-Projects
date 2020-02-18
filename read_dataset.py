import json

Head_Word = "Criminal"
Words = ["CI", "confidental informat", "informat"]

with open('cases_appeals.json', 'r') as f:
    data = json.load(f)

def loop(data):
    for key in data.keys():
        for ele in data[key]:
            for word in Words:
                # if(ele.find(Head_Word) and (not ele.find("civil"))):
                if (Head_Word.lower() in ele.lower()):
                    if (word.lower() in ele.lower()):
                        return True
    return False

A = []
for i in range(len(data)):
    A.append(loop(data[i]))
n = 0
List = []
for i in range(len(A)):
    List.append(data[i])
    if(A[i] == True):
        n += 1
# print("Total number of cases: ")
# print(len(A))
# print("Positive: ")
# print(n)
#print(List)
# with open("cases_appeals_result.json","w") as f:
#      json.dump(List, f)
