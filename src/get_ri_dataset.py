import csv
import glob
import os
import re
from time import sleep

import pandas as pd

import pdftotext
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

www1 = "https://www.courts.ri.gov/Courts/SupremeCourt/Pages/Opinions%20and%20Orders%20Issued%20in%20Supreme%20Court%20Cases.aspx"

def download_pdf(browser, year_period):
    '''
        download pdf from ri website into pdf_ri_cases file
        :param: browser: chrome
        :param: year_period: eg. 2018 - 2019, str type
    '''

    browser.find_element_by_link_text(year_period).click()
    count = 0
    filename_list = []

    while(True):
        cases_num_path = "//*[@id='bottomPagingCellWPQ3']/table/tbody/tr"
        pdf_link_path = "//*[@id='onetidDoclibViewTbl0']/tbody"
        click_path = cases_num_path + "/td"
        tr_list = browser.find_elements_by_xpath(click_path)

        if (count == 0):
            cases_num_str = tr_list[0].get_attribute('textContent')
        else:
            cases_num_str = tr_list[1].get_attribute('textContent')

        cases_num_start = int(cases_num_str.split(' ')[0])
        cases_num_end =int(cases_num_str.split(' ')[2])


        '''
            For year <=2010, can use this method
        ''' 

        # element = browser.find_elements_by_xpath("//a[contains(@href, '/Courts/SupremeCourt/OpinionsOrders')]")

        # websites = []
        # for pdf in element:
        #     website = pdf.get_attribute('href')
        #     strs = website.split('/')
        #     filename = strs[-1]
        #     if (filename not in filename_list):
        #         filename_list.append(filename)

        #     if (website not in websites):
        #         websites.append(website)

        # for website in websites:
        #     browser.get(website)
        #     sleep(3)
        

        '''
            For year > 2010, use this method
        '''
        for i in range(cases_num_start, cases_num_end+1):
            pdf_path = pdf_link_path + "/tr[" + str(3*(i-cases_num_start) + 2) + "]/td[2]/a"

            filename = browser.find_element_by_xpath(pdf_path).get_attribute('textContent')

            browser.find_element_by_xpath(pdf_path).click()
            filename_list.append(filename+".pdf")
            sleep(3)

        '''
            jump to next page if exists
        '''
        if count == 0 and len(tr_list) == 2:
            count = count + 1
            tr_list[1].click()
        elif count > 0 and len(tr_list) == 3:
            count = count + 1
            tr_list[2].click()
        else:
            break;

    # save files order into a txt 
    file = open('./data/filename_list_ri.txt','w');
    for name in filename_list:
        file.write(str(name) + '\n');
    file.close();


def tag_cases(browser, year_period):
    '''
        classify cases with type(criminal / not criminal) and results(affirm / not affirm)
        :param: browser: chrome
        :param: year_period: eg. 2018 - 2019, str type
    '''

    browser.find_element_by_link_text(year_period).click()

    texts = []
    criminal_flag = []
    result = []

    count = 0
    while(True):
        
        cases_num_path = "//*[@id='bottomPagingCellWPQ3']/table/tbody/tr"
        pdf_link_path = "//*[@id='onetidDoclibViewTbl0']/tbody"
        click_path = cases_num_path + "/td"

        tr_list = browser.find_elements_by_xpath(click_path)

        cases_path = "//*[@id='onetidDoclibViewTbl0']/tbody"

        if (count == 0):
            cases_num_str = tr_list[0].get_attribute('textContent')
        else:
            cases_num_str = tr_list[1].get_attribute('textContent')

        cases_num_start = int(cases_num_str.split(' ')[0])
        cases_num_end =int(cases_num_str.split(' ')[2])


        for i in range(cases_num_start, cases_num_end+1):
            path = cases_path + "/tr[" + str((i - cases_num_start + 1)*3)  + "]/td/div"

            text = browser.find_element_by_xpath(path).get_attribute('textContent')

            # keyword
            if (text.lower().find('prosecutor') != -1 or text.lower().find('criminal') != -1):
                criminal_flag.append('criminal')
            else:
                criminal_flag.append('non-criminal')

            if (text.lower().find('affirm') != -1):
                result.append('affirm')
            else:
                result.append('not affirm')

        if count == 0 and len(tr_list) == 2:
            count = count + 1
            tr_list[1].click()
        elif count > 0 and len(tr_list) == 3:
            count = count + 1
            tr_list[2].click()
        else:
            break;

    return criminal_flag, result, texts

def get_pdfs(path):
    pdfs = []
    # f = open('./data/filename_list_ri.txt')
    # lines = f.readlines()

    # for name in lines:
    #     pdf_name = name.replace("\n", "")
    pdf_names = os.listdir(path)

    for pdf_name in pdf_names:

        if pdf_name.endswith('.pdf'):
            with open(path + "/" + pdf_name,  "rb") as f:
                pdf = pdftotext.PDF(f)
                pdfs.append([pdf_name,pdf])

    return pdfs

def get_cases(pdfs):
    cases_text = []

    for pdf in pdfs:

        case = ''.join(pdf[1])
        cases_text.append([pdf[0],case])

    return cases_text

def split(cases):

    for i, case in enumerate(cases):
        paragraphs = re.split(r'\s{2,}',case[1])
        cases[i][1] = paragraphs

    return cases

def get_data(cases):
    cases_title = []
    cases_text = []
    criminal_flag = []
    result = []

    for pdf_case in cases:
        paragraph_case_number = -1
        paragraph_submitted_argued = -1
        paragraph_opinion_issued = -1
        crimianl_type = -1
        paragraph_result = -1
        pdf_file_name = pdf_case[0]
        case = pdf_case[1]


        for i, paragraph in enumerate(case):
            if paragraph.find(')') != -1:
                paragraph_case_number = i
                break
        if paragraph_case_number == -1: print("No case number found")

        for i, paragraph in enumerate(case):   
            if paragraph.find('NOTICE:') != -1:
                paragraph_submitted_argued = i
                break
        if paragraph_submitted_argued == -1: print("No NOTICE found")

        for i, paragraph in enumerate(case):
            if paragraph.find('OPINION') != -1:
                paragraph_opinion_issued = i
                break

        for i, paragraph in enumerate(case):
            if paragraph.lower().find('affirm') != -1:
                paragraph_result = 1
                break
            if paragraph.lower().find('vacate') != -1:
                paragraph_result = 0
                break
        if paragraph_result == 1:
            result.append('reversal')
        elif paragraph_result == 0:
            result.append('non-reversal')
        else:
            result.append('undecided')
            

        title = ' '.join(case[paragraph_case_number+1:paragraph_submitted_argued])

        cases_title.append(title)
        cases_text.append(case[paragraph_opinion_issued+1:])


        '''
            for 2010-, html is different from 2010+
            hard to scrpy text from html because it has no tag
        '''

    return cases_title, cases_text, result

def combine_dataset(workpath):
    '''
        combine all csv under the workpath into one csv file
    '''
    csv_list = glob.glob(workpath + '/*.csv') #查看同文件夹下的csv文件数
    print(u'共发现%s个CSV文件'% len(csv_list))
    print(u'正在处理............')
    for i in csv_list: #循环读取同文件夹下的csv文件
        fr = open(i,'rb').read()
        with open('final_ri.csv','ab') as f: #将结果保存为result.csv
            f.write(fr)
    print(u'合并完毕！')


def scrapy(year_period):
    '''
        changhe directory to adapt to your os before run the code
    '''

    download_dir = "/home/changhao/Documents/CS506/CS506-Spring2020-Projects/pdf_ri_cases" 

    profile = {
    'download.default_directory': download_dir,
    'profile.default_content_settings.popups': 0,
    "plugins.always_open_pdf_externally": True
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(www1)


    '''
        download pdf from ri website
    '''
    download_pdf(browser, year_period)

    criminal_flag, result, texts = tag_cases(browser, year_period)

    
    path = './pdf_ri_cases'
    pdfs = get_pdfs(path)
    cases = get_cases(pdfs)
    cases = split(cases)
    cases_title, cases_text = get_data(cases)


    '''
        save result into csv file
    '''

    res = pd.DataFrame(columns = ['title', 'type', 'result', 'text'])

    for i in range(len(result)):
        res.loc[i] = [cases_title[i], criminal_flag[i], result[i], cases_text[i]]

    res.to_csv("./data/ri" + year_period + ".csv")

if __name__ == "__main__":
    path = './pdf_ri_cases'
    pdfs = get_pdfs(path)
    cases = get_cases(pdfs)
    cases = split(cases)
    cases_title, cases_text, result = get_data(cases)

    print(len(cases_title))
    print(len(cases_text))
    print(len(result))

    res = pd.DataFrame(columns = ['title', 'result', 'text'])

    for i in range(len(result)):
        res.loc[i] = [cases_title[i], result[i], cases_text[i]]

    print(result)
    res.to_csv("./data/ri_2.0.csv")
