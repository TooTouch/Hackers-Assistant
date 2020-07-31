from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.alert import Alert

import pandas as pd

import time 
import datetime
import argparse


def students_check(ID, PWD):
    login_url = 'https://www.hackers.ac/teachers/index.php'

    driver = webdriver.Chrome()
    driver.get(login_url)
    driver.implicitly_wait(10)

    # LOGIN
    select = Select(driver.find_element_by_xpath('//*[@id="level"]'))
    select.select_by_value('6')

    driver.find_element_by_xpath('//*[@id="login_table"]/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[2]/input').send_keys(ID)
    driver.find_element_by_xpath('//*[@id="login_table"]/tbody/tr[1]/td[1]/table/tbody/tr[3]/td[2]/input').send_keys(PWD)

    driver.find_element_by_xpath('//*[@id="login_table"]/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr/td').click()

    aa = Alert(driver)
    aa.accept()

    # page 

    driver.find_element_by_xpath('//*[@id="main_roll"]/div[2]/div/ul[1]/li[1]/a').click()
    driver.implicitly_wait(10)

    driver.find_element_by_xpath('//*[@id="sub_wrap"]/div[5]/div[1]/ul[1]/li[1]/a').click()
    time.sleep(4)

    # check

    class_dict = {
        '오전 HACKERS 1교시':'월~금\n10:00~10:50',
        'Pre-Hackers':'월~금\n12:00~12:50',
        '오전중급반 AB 4교시':'월~금\n13:00~13:50',
        '오후 실전반 4교시':'월~금\n17:00~17:50',
        '저녁 정규반A':'월,수,금(10회)\n20:10~21:00',
        '저녁 정규반C (12회)':'월,수,금(12회)\n21:20~22:00',
        '아침실전반 1교시':'화,목,금(10회)\n08:00~08:50',
        '오후정규반 B':'화,목,금(10회)\n14:50~15:40',
        '주말오전중급 1교시':'토\n10:00~11:50'
    }

    tb = driver.find_element_by_xpath('//*[@id="thisMonthTable"]/table/tbody')
    trs = tb.find_elements_by_tag_name('tr')

    name_lst = []
    title_lst = []
    time_lst = []
    ss_lst = []
    onoff_lst = []

    for tr in trs:
        name = tr.find_element_by_css_selector('td:nth-child(4) > p > a:nth-child(1)').text.strip()
        t = tr.find_element_by_css_selector('td:nth-child(5)').text.strip()
        ss = int(tr.find_element_by_css_selector('td:nth-child(7)').text.strip().replace('명',''))
        onoff = 'on-line' if '온라인' in name else 'off-line'
    
        if t == '월,화,수,목(16회)\n17:00~17:50':
            t = '월~금\n17:00~17:50' 
        elif t == '토,일\n10:00~11:50':
            t = '토\n10:00~11:50'
        elif t == '월~금[전반]\n17:00~17:50':
            t = '월~금\n17:00~17:50'
        elif t == '월~금\n08:00~08:50':
            t = '화,목,금(10회)\n08:00~08:50'

        for k,v in class_dict.items():
            if (t==v) and (onoff=='off-line'):
                title = k
            elif (t==v) and (onoff=='on-line'):
                if t == '월~금\n10:00~10:50':
                    title = '(온라인)오전 HACKERS 1교시'
                elif t == '월~금\n13:00~13:50':
                    title = '(온라인)오후 정규종합반 4교시'

        name_lst.append(name)
        title_lst.append(title)
        time_lst.append(t)
        ss_lst.append(ss)
        onoff_lst.append(onoff)

    df = pd.DataFrame({'title':title_lst,'name':name_lst,'class_time':time_lst,'onoff':onoff_lst,'nb_students':ss_lst})
    
    return df 



if __name__=='__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('--id',type=str,help='ID')
    parse.add_argument('--pwd',type=str,help='PASSWORD')
    args = parse.parse_args()
    
    df = students_check(args.id, args.pwd)    
    groupby = df.groupby(['title','class_time'])['nb_students'].sum()

    df.to_csv('./data/students {}.csv'.format(datetime.datetime.now()).replace(':','.'), index=False, encoding='cp949')
    groupby.to_csv('./data/students_stats {}.csv'.format(datetime.datetime.now()).replace(':','.'), encoding='cp949')



