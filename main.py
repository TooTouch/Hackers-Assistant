import os 
from comments import *

def run(ha_id, ha_pwd, token_v2, ha_notion):
    driver = get_board_list(ha_id, ha_pwd)
    boards_info, driver = get_board_urls(driver)
    total_df = get_comment_urls(driver, boards_info)
    
    print('[COMPLETE] Number of boards with comments: ',total_df.shape[0])
    
    add_notion(token_v2, ha_notion, total_df)
    print('[COMPLETE] Create a table in Notion')

    return True

if __name__=='__main__':

    ha_id = os.environ['HA_ID']
    ha_pwd = os.environ['HA_PWD']
    token_v2 = os.environ['TOKEN_V2']
    ha_notion = os.environ['HA_NOTION']

    run(ha_id, ha_pwd, token_v2, ha_notion)

    