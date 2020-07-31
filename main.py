import os 
from comments import *

def run(HA_ID, HA_PWD, token_v2, HA_notion):
    driver = get_board_list(HA_ID, HA_PWD)
    boards_info, driver = get_board_urls(driver)
    total_df = get_comment_urls(driver, boards_info)
    
    print('[COMPLETE] Number of boards with comments: ',total_df.shape[0])
    
    add_notion(token_v2, HA_notion, total_df)
    print('[COMPLETE] Create a table in Notion')

    return True

if __name__=='__main__':

    HA_ID = os.environ['HA_ID']
    HA_PWD = os.environ['HA_PWD']
    token_v2 = os.environ['token_v2']
    HA_notion = os.environ['HA_notion']

    run(HA_ID, HA_PWD, token_v2, HA_notion)

    