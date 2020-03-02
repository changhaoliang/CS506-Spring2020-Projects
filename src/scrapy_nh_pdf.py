from PyPDF2 import PdfFileReader, PdfFileWriter
from selenium import webdriver
import os
import string
import pandas as pd

def extract_title(middle_index, lines):
    '''
        extract title
    '''

    title = ""

    # title start index
    left_index = middle_index - 1

    # title end index
    right_index = middle_index - 1

    while (lines[left_index].isdigit() == False):
        left_index -= 1
    left_index += 1
    while (lines[left_index] == ' '):
        left_index += 1

    while (lines[right_index] == ' '):
        right_index -= 1

    title_lines_num = right_index - left_index + 1
    for i in range(left_index, right_index + 1):
        title += lines[i]

    return title

def extract_headnote(left_index, right_index, lines):
    '''
        extract headnote
    '''

    headnote = " "

    left_index = left_index + 1
    while (lines[left_index] == ' '):
        left_index += 1

    left_index += 1 # skip date

    if (left_index >= right_index) :
        return ""
    for i in range(left_index, right_index):
        if lines[i] != ' ':
            headnote += lines[i]

    return headnote

def extract_text(left_index, lines, pdfReader):
    '''
        extract text
    '''
    right_index = len(lines) - 1

    text = ""

    for i in range(left_index, right_index + 1):
        if (lines[i] != ' '):
            text += lines[i]

    pages_num = pdfReader.numPages

    for i in range(2, pages_num):
        lines = pdfReader.getPage(i).extractText().split('\n')
        for line in lines:
            if (line != ' '):
                text += line
    return text

# website: https://www.courts.state.nh.us/supreme/opinions/2018/index.htm
def extract_case_title_text(pdfReader):
    # titile lies in 0th page
    page1 = pdfReader.getPage(0)
    page2 = pdfReader.getPage(1)
    page1_content = page1.extractText()
    page2_content = page2.extractText()

    lines = (page1_content + page2_content).split('\n')

    case_keyword_index = 0
    case_opinion_index = 0
    case_fact_index = 0

    # find index
    for i in range(len(lines)):
        if case_fact_index == 0 and case_fact_index <= case_opinion_index :
            if (lines[i].find("facts") != -1 or lines[i].find("The following") != -1 or lines[i].find("affirm.") != -1):
                case_fact_index = i

        if case_opinion_index == 0:
            if (lines[i].find("Opinion Issued") != -1):
                case_opinion_index = i
        
        if case_keyword_index == 0:
            if (lines[i].find("Argued") != -1):
                case_keyword_index = i
            elif (lines[i].find("Submitted") != -1):
                case_keyword_index = i
                
    print(case_keyword_index, case_opinion_index, case_fact_index)
   
    title = " "
    headnote = " "
    text = " "

    if (case_keyword_index != 0):
        title = extract_title(case_keyword_index, lines)
    if (case_opinion_index != 0):
        headnote = extract_headnote(case_opinion_index, case_fact_index, lines)
    if (case_fact_index == 0):
        case_fact_index = case_opinion_index
    if (case_fact_index != 0):
        text = extract_text(case_fact_index, lines, pdfReader)
    
    return title, headnote, text
    

'''
    test by one pdf
'''
# pdfFile = open("./pdf_nh_cases" + "/" + "test.pdf", 'rb')
# pdfReader = PdfFileReader(pdfFile)
# title, headnote, text = extract_case_title_text(pdfReader)
# pdfFile.close()

def read_files_allpdf(path):
    dataset_csv = pd.DataFrame(columns = ['title', 'headnote', 'text'])

    files = os.listdir(path)
    for i in range(len(files)):
        pdfFile = open(path + "/" + files[i], 'rb')

        pdfReader = PdfFileReader(pdfFile)
        title, headnote, text = extract_case_title_text(pdfReader)
        dataset_csv.loc[i] = [title,  headnote, ""]
        pdfFile.close()

    dataset_csv.to_csv("cases_nh.csv")

    return dataset_csv

res = read_files_allpdf("./pdf_nh_cases_opinion")


# selenium test
# browser = webdriver.Chrome()
# browser.get('https://www.courts.state.nh.us/supreme/opinions/2018/2018083alward.pdf')
# print(browser.page_source)





