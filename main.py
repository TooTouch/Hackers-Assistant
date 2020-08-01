import os 
from comments import *


if __name__=='__main__':

    ha_id = os.environ['HA_ID']
    ha_pwd = os.environ['HA_PWD']
    token_v2 = os.environ['TOKEN_V2']
    ha_notion = os.environ['HA_NOTION']

    driver = get_board_list(ha_id, ha_pwd)
    boards_info, driver = get_board_urls(driver)
    new_df = get_comment_urls(driver, boards_info)
    print('[COMPLETE] Number of boards with comments: ',new_df.shape[0])
    
    add_notion(token_v2, ha_notion, new_df)
    print('[COMPLETE] Create a table in Notion')

    
