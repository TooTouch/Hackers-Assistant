from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup as BSoup

from notion.client import NotionClient
from notion.block import CollectionViewBlock
from notionist import collection_api

import time 
import pandas as pd
import datetime

def get_board_list(ID, PWD):
    login_url = 'https://www.hackers.ac/teachers/index.php'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome('chromedriver',chrome_options=options)
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

    return driver

def get_board_urls(driver):
    # select month
    select = Select(driver.find_element_by_xpath('//*[@id="changeDate"]'))
    select.select_by_value('202007')

    bs_obj = BSoup(driver.page_source, 'html.parser')
    rows = bs_obj.select_one('#thisMonthTable > table > tbody').find_all('tr')

    titles = []
    urls = []
    for row in rows:
        title = row.select_one('p > a:nth-child(1)', href=True)
        if '청강' not in title.get_text():
            titles.append(title.get_text().strip()) 
            urls.append('https://www.hackers.ac'+row.select_one('a.btn_lag.b_r.blink', href=True)['href'])
        
    df = pd.DataFrame({'title':titles, 'url':urls})    

    return df, driver

def get_is_comments(driver):
    
    bs_obj = BSoup(driver.page_source, 'html.parser')
    rows = bs_obj.select_one('#bbslist > form > table > tbody').find_all('tr')

    titles = []
    categories = []
    urls = []
    nb_comments = []
    names = []
    dates = []

    for row in rows:
        sbj = row.select_one('td.sbj')
        if sbj is not None:
            title = sbj.find_all('a', href=True)[0]
            name = row.select_one('td.name').get_text().strip()
            date = row.select_one('td.date').get_text().strip()
            if sbj.select_one('span.comment.hand'):
                titles.append(title.get_text().strip())
                categories.append('teacher' if row.select_one('td:nth-child(2) > div') is not None else 'student')
                urls.append('https://www.hackers.ac'+title['href'])
                nb_comments.append(sbj.select_one('span.comment.hand').get_text().strip()[1:-1])
                names.append(name)
                dates.append(date)
            elif '김동현' not in name:
                titles.append(title.get_text().strip())
                categories.append('teacher' if row.select_one('td:nth-child(2) > div') is not None else 'student')
                urls.append('https://www.hackers.ac'+title['href'])
                nb_comments.append('0')
                names.append(name)
                dates.append(date)

    df = pd.DataFrame({
            'title':titles,
            'url':urls,
            'nb_comment':nb_comments,
            'category':categories,
            'name':names,
            'date':dates
        })

    return df


def get_comment_urls(driver, boards_info):
    total_df = pd.DataFrame()

    for url in boards_info['url']:
        driver.get(url)
        driver.implicitly_wait(10)

        b_lst = driver.find_element_by_css_selector('#bbslist > div.info > div > ul')
        lis = b_lst.find_elements_by_tag_name('li')
        
        for li in lis:
            if ('LC' in li.text) or ('L/C' in li.text):
                li.click()
                time.sleep(2)
                df = get_is_comments(driver)
                break  

        if len(df) > 0:
            df['class_name'] = boards_info[boards_info['url']==url]['title'].values[0]
            
            total_df = pd.concat([total_df,df], axis=0)

            total_df.index = range(total_df.shape[0])

    # remove duplicated comments        
    total_df_drop = total_df[['title','category','date','name','nb_comment']].drop_duplicates()
    total_df = pd.merge(total_df_drop.reset_index(), total_df[['class_name','url']].reset_index(), how='left', on='index')
    total_df = total_df.drop('index', axis=1)

    return total_df
    
def add_notion(token_v2, url, df):
    # update comments
    try:
        print(['[NOTION] Update comments table'])
        df = update_comments_table(df)
    except:
        print('[NOTION] Create new comments table')
        # add check box property
        df['check'] = False

    df = df.sort_values(['check','date'],ascending=[False,False])

    client = NotionClient(token_v2=token_v2)
    page = client.get_block(url)

    # clean page
    if len(page.children) > 0:
        for i in range(len(page.children)):
            del page.children[i]

    child = page.children.add_new(CollectionViewBlock)
    child.collection = client.get_collection(
        client.create_record(
            "collection", parent=child, schema=get_schema_comments(df.columns)
        )
    )

    # set korea time
    kor_time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    child.title = kor_time
    child.views.add_new(view_type='table')

    for i in range(len(df)):  
        row = child.collection.add_row()
        row.set_property('title', str(i))
        for col in df.iloc[i].index:
            if col == 'check':
                row.set_property(col, df.iloc[i][col])
            else:
                row.set_property(col, str(df.iloc[i][col]))
    

def get_schema_comments(cols):
    table_attr = {
        "title": {"name": "INDEX", "type": "title"}
    }

    for col in cols:
        if col=='url':
            table_attr[col] = {'name':col, 'type':'url'}
        elif col=='category':
            table_attr[col] = {
                'name':col,
                'type': 'select',
                'options': [
                    {'id': 'd91302e8-2e91-4911-81c9-042c32e106d3',
                    'color': 'purple',
                    'value': 'teacher'},
                    {'id': '9bcf09c0-d1e9-4195-a59c-8304e0b235c0',
                    'color': 'green',
                    'value': 'student'}
                ]
            }
        elif col=='check':
            table_attr[col] = {'name':col, 'type':'checkbox'}         
        else:
            table_attr[col] = {'name':col, 'type':'text'}

    return table_attr

def update_comments_table(token_v2, url, new_df):
    # extract old comments table
    CE = collection_api.CollectionExtract(token_v2)
    old_df = CE.table_extract(url)

    # update comments table
    update_df = pd.concat([old_df.drop('check',axis=1), new_df], axis=0).drop_duplicates()
    update_df['nb_comment'] = update_df['nb_comment'].astype(int)

    col = new_df.columns.tolist().remove('nb_comment')
    update_df = update_df.groupby(col).max().reset_index()
    update_df = update_df.astype(str)

    update_df = pd.merge(old_df, update_df, on=update_df.columns.tolist(), how='right')
    # fill NA to False in 'check' feature
    update_df['check'] = update_df['check'].fillna(False)

    return update_df