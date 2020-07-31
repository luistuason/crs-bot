#!/usr/local/bin/python3

# import time, sched
import os
import lxml.html as lh
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def input_credentials(browser, username_str, password_str):
    userfield = browser.find_element_by_id('txt_login')
    passfield = browser.find_element_by_id('pwd_password')

    userfield.send_keys(username_str)
    passfield.send_keys(password_str)
    passfield.submit()


def get_subject_df(browser, subject, print_friendly = False):
    subjectfield = browser.find_element_by_id('input_subject')
    subjectfield.clear()
    subjectfield.send_keys(subject)
    subjectfield.submit()

    '''
    3 cases come out of a subject search
    1) Subject list comes out

    2) No Result; Wala pang classes for it 

    3) 1 subject result so print agad section list
    thead empty
    '''
    doc = lh.fromstring(browser.page_source)
    thead = doc.xpath("//table[@id='tbl_subject-list']/thead/tr") #type: list
    tr_elements = doc.xpath("//table[@id='tbl_subject-list']/tbody/tr") #type: list

    if not thead:
        ## CASE 3
        tr_elements = doc.xpath("//table[@id='tbl-search']/tbody/tr")
        td = tr_elements[0][1].text_content().split()
        lone_subject = td[0]+' '+td[1]

        print(subject+" only has 1 course: " + lone_subject + "\n")
    else:
        if len(tr_elements) == 1:
            ## CASE 2
            print("No available courses under " + subject + " yet.\n")
        else:

            ## CASE 1
            col = []
            i = 0
            for t in thead[0]:
                i += 1
                name = t.text_content()
                col.append((name, []))

            for i in range(len(tr_elements)):
                for j in range(4):
                    t = tr_elements
                    if (j == 3):
                        col[j][1].append(t[i].xpath('td/a/@href')[0])
                    else:
                        data = t[i][j].text_content()
                        try:
                            data = int(data)
                        except:
                            pass
                        col[j][1].append(data)

            df = pd.DataFrame({title:column for (title, column) in col})
            if print_friendly:
                df = df[['Subject', 'Total Classes']]
            else:
                df = df[['Subject', 'Total Classes', 'Action']]

            return df

def check_new_subject(df, subject):
    if (subject in df.Subject.values):
        print('MERON NANG '+subject)
    else:
        print('WALA PANG '+subject)

def main():
    print("\nCRS Pre-enlistment Bot Prototype\n--------------------------------\n")

    #Input courses to be checked here
    subjects = ['EEE', 'PE 2', 'ES']
    subjects.sort()

    username = ''
    password = ''

    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    browser.get(('https://crs.upd.edu.ph/'))
    input_credentials(browser, username, password)

    browser.get('https://crs.upd.edu.ph/preenlistment')
    ## Headers: 'Subject', 'Subject Title', 'Total Classes', 'Action'

    for s in subjects:
        main_df = get_subject_df(browser, s, True)
        # eee = eee[eee.Subject != 'EEE 13']
        if main_df is not None:
            print(str(main_df.shape[0]) + " courses under " + s +".")
            print()

    browser.quit()
    print("\n")

if __name__ == '__main__':
    main()
    