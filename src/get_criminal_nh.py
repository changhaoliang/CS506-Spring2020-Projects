# from selenium import webdriver
import os
import re 
import csv
import json
import pandas as pd
import pprint
import pdftotext # sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev && pip3 install pdftotext

path = './pdf_nh_cases'


# website: https://www.courts.state.nh.us/supreme/opinions/2018/index.htm
# selenium test
# browser = webdriver.Chrome()
# browser.get('https://www.courts.state.nh.us/supreme/opinions/2018/2018083alward.pdf')
# print(browser.page_source)

def get_pdfs(path):
    pdfs = []
    # read pdf file names
    pdf_names = os.listdir(path)
    #print(pdf_names)
    # load pdf files
    for pdf_name in pdf_names:
        # excluding non-pdf files
        if pdf_name.endswith('.pdf'):
            with open(path + "/" + pdf_name,  "rb") as f:
                pdf = pdftotext.PDF(f)
                pdfs.append([pdf_name,pdf])
    # return pdf files in a list of [filename, pdf object]
    return pdfs

def get_cases(pdfs):
    cases_text = []
    # extract texts of cases from pdfs
    for pdf in pdfs:
        # join all pages into one string
        case = ''.join(pdf[1])
        cases_text.append([pdf[0],case])
    # return texts of cases in a list of [filename, case text]
    return cases_text

def split(cases):
    # split each case into paragraphs
    for i, case in enumerate(cases):
        paragraphs = re.split(r'\s{2,}',case[1])
        paragraphs = [paragraph.replace('\n', ' ') if paragraph and i != 2 
        else paragraph for i, paragraph in enumerate(paragraphs)]
        cases[i][1] = paragraphs
    # return cases with paragraphs [filename, splitted case]
    return cases

def get_data(cases):
    cases_data = []
    for pdf_case in cases:
        case_info = {}
        paragraph_case_number = -1
        paragraph_submitted_argued = -1
        paragraph_opinion_issued = -1
        pdf_file_name = pdf_case[0]
        case = pdf_case[1]

        # find case number
        for i, paragraph in enumerate(case):
            if paragraph.find('No. ') != -1:
                paragraph_case_number = i
                break
        if paragraph_case_number == -1: print("No case number found")

        # find Submitted or Argued date
        for i, paragraph in enumerate(case):   
            if paragraph.find('Submitted: ') != -1 or paragraph.find('Argued: ') != -1:
                paragraph_submitted_argued = i
                break
        if paragraph_submitted_argued == -1: print("No Submitted or Argued date found")

        # find Opinion Issued date
        for i, paragraph in enumerate(case):   
            if paragraph.find('Opinion Issued: ') != -1:
                paragraph_opinion_issued = i
                break
        if paragraph_opinion_issued == -1: print("No Opinion Issued date found")

        case_info['file name'] = pdf_file_name

        # get case number
        case_number = case[paragraph_case_number].split('\n')[-1].replace('No. ','')
        case_info['No.'] = case_number
        cases_data.append(case_info)

        # get case title
        case_title = ' '.join(case[paragraph_case_number+1:paragraph_submitted_argued])
        case_info['title'] = case_title

        # get case type
        case_info['type'] = 'Non-criminal'
        # according to RSA document in NH https://www.gencourt.state.nh.us/rsa/html/nhtoc.htm
        # CRIMINAL CODE is included in TITLE LXII including chapter 625 - 651-f
        headnotes = case[paragraph_opinion_issued+3].split(' ')
        for i, word in enumerate(headnotes):
            if word == 'RSA':
                rsa_num = int(headnotes[i+1][:3])
                if rsa_num >= 625 and rsa_num <652:
                    case_info['type'] = 'Criminal'
        
        # get case text that is everything after Opinion Issued date
        case_info['text'] = case[paragraph_opinion_issued+1:]
        '''     
        if case_title.find('THE STATE OF NEW HAMPSHIRE') == 0:
            # print(case_title.find('THE STATE OF NEW HAMPSHIRE'))
            case_info['type'] = 'Criminal'
        else:
            case_info['type'] = 'Non-criminal'
        '''
    return cases_data

pdfs = get_pdfs(path)
cases = get_cases(pdfs)
cases = split(cases)
cases_data = get_data(cases)

# print case data 
df = pd.DataFrame([case['No.'], case['type'], case['file name'], case['title'], case['text']] for case in cases_data)
df.columns=['No.', 'type', 'file name','title','text']
print(df)

'''
# write to a json file
with open('cases_nh.json', 'w') as fout:
    json.dump(cases_data , fout)
'''


# write to a csv file
keys = cases_data[0].keys()
with open('cases_nh.csv', 'w') as fout:
    dict_writer = csv.DictWriter(fout, keys)
    dict_writer.writeheader()
    dict_writer.writerows(cases_data)