import os
import csv
import json
from pprint import pprint


def search_keywords(state, keywords):
    """
    :param: state: ma, nh, ri
    :param: keywords: a list of keywords to be searched

    cases_ma is a list of dictionary each of which represents a case
        keys: case, headnote, text

    cases_nh is a list of dictionary each of which represents a case
        keys: file name, title, type, text
    """
    cases = load_cases(state)
    criminal_cases = get_criminal_cases(state, cases)

    case_pool = set([])
    cases_keywords = []
    for i, case in enumerate(criminal_cases):
        for key in case:
            for text in case[key]:
                words = text.split(" ")
                for word in words:
                    for keyword in keywords:
                        if keyword in word.lower():
                            if i not in case_pool:
                                cases_keywords.append(case)
                            case_pool.add(i)
                    if "CI" in word:
                        if i not in case_pool:
                            cases_keywords.append(case)
                        #print(word)
                        case_pool.add(i)

    print(str(len(case_pool))+" cases contain keywords")
    return cases_keywords


def load_cases(state):

    path_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"
    if state == "ma":
        path = [path_data + "/cases.json", path_data + "/cases_appeals.json"]
    elif state == "nh":
        path = [path_data + "/cases_nh.json"]

    cases = []
    for file in path:
        with open(file, 'r') as f:
            cases += json.load(f)

    print(str(len(cases))+" cases loaded")
    return cases


def get_criminal_cases(state, cases):
    criminal_cases = []
    for i, case in enumerate(cases):
        for key in case:

            if state == "ma" and key == "headnote":
                for headnote in case[key]:
                    if "Criminal" in headnote:
                        criminal_cases.append(cases[i])

            elif state == "nh" and key == "type":
                if case[key] == "Criminal":
                    criminal_cases.append(cases[i])

    print(str(len(criminal_cases))+" criminal cases found")
    return criminal_cases


def save_result(path, fmt, cases):
    if fmt == "json":
        # write to a json file
        with open(path + '.json', 'w') as fout:
            json.dump(cases, fout)
    elif fmt == "csv":
        # write to a csv file
        keys = cases[0].keys()
        with open(path + '.csv', 'w') as fout:
            dict_writer = csv.DictWriter(fout, keys)
            dict_writer.writeheader()
            dict_writer.writerows(cases)
    else:
        print("Invalid format")


if __name__ == "__main__":

    # enter "ma", "nh" or "ri"
    state = "nh"
    keywords = ["informant"]

    result = search_keywords(state, keywords)

    # save to ../data
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/result/cases_" + state + "_result"
    # save as json or csv
    save_result(save_path, "json", result)



