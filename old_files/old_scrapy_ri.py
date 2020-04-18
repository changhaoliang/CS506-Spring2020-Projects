from PyPDF2 import PdfFileReader, PdfFileWriter
# from selenium import webdriver
import os
import string
import pandas as pd

def extract_title(left_index, right_index, lines):
    '''
        extract title
    '''

    title = ""

    # title start index
    left_index += 1
    while lines[left_index] == ' ':
        left_index += 1

    right_index -= 1
    while lines[right_index] == ' ':
        right_index -= 1

    for i in range(left_index, right_index + 1):
        title += lines[i]
    title = title.replace(':', '')
    title = title.replace('   ', '')

    return title

def extract_headnote(left_index, right_index, lines):
    '''
        extract headnote
    '''

    headnote = " "

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
    
    text = ""

    for i in range(left_index, len(lines)):
        if (lines[i] != ' '):
            text += lines[i]

    pages_num = pdfReader.numPages

    for i in range(3, pages_num):
        lines = pdfReader.getPage(i).extractText().split('\n')
        for line in lines:
            if (line != ' '):
                text += line
    return text

def extract_title_headnote_text(pdfReader):
    page = pdfReader.getPage(0)
    page_content = page.extractText()

    lines = (page_content).split('\n')

    case_keyword_index1 = 0
    case_keyword_index2 = 0

    for i in range(len(lines)):
        if (lines[i].find(')')!= -1):
            case_keyword_index1 = i
        if (lines[i].find('NOTICE') != -1):
            case_keyword_index2 = i
    title = extract_title(case_keyword_index1, case_keyword_index2, lines)
    
    page = pdfReader.getPage(1)
    page_ = pdfReader.getPage(2)
    page_content = page.extractText() + page_.extractText()
    lines = (page_content).split('\n')

    case_opinion_index = 0
    case_text_index = 0
    for i in range(len(lines)):
        if (lines[i].find('O P I N I O N') != -1):
            case_opinion_index = i
            case_text_index = case_opinion_index + 1
        if (lines[i].find('Facts and Travel') != -1):
            case_text_index = i

    headnotes = extract_headnote(case_opinion_index, case_text_index, lines)
    text = extract_text(case_text_index, lines, pdfReader)

    return title, headnotes, text

def read_files_allpdf(path):
    dataset_csv = pd.DataFrame(columns = ['title', 'headnote', 'text'])

    files = os.listdir(path)
    for i in range(len(files)):
        pdfFile = open(path + "/" + files[i], 'rb')

        pdfReader = PdfFileReader(pdfFile)
        title, headnote, text = extract_title_headnote_text(pdfReader)
        dataset_csv.loc[i] = [title, headnote, text]
        pdfFile.close()

    dataset_csv.to_csv("cases_ri.csv")

    return dataset_csv

res = read_files_allpdf("./pdf_ri_cases")