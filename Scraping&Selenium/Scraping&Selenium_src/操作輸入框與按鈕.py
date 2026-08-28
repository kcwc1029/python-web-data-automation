from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


### 啟動 Chrome
driver = webdriver.Chrome()
driver.maximize_window() # 將瀏覽器視窗最大化，避免 Wikipedia 將搜尋框收合


### 開啟網頁
try:
    driver.get("https://zh.wikipedia.org/wiki/臺灣")


    ### 找到所有搜尋框
    search_inputs = driver.find_elements(
        By.NAME,
        "search"
    )


    ### 找到目前畫面中可見的搜尋框
    search_input = None

    for item in search_inputs:
        if item.is_displayed():
            search_input = item
            break


    ### 確認是否找到可操作的搜尋框
    if search_input is None:
        print("找不到可見的搜尋框")

    else:
        print("搜尋框是否顯示：")
        print(search_input.is_displayed())

        print("\n搜尋框是否可以操作：")
        print(search_input.is_enabled())


        ### 清除搜尋框
        search_input.clear()


        ### 輸入搜尋文字
        search_input.send_keys("人工智慧")


        ### 查看輸入框目前的值
        print("\n搜尋框目前內容：")
        print(search_input.get_property("value"))

        ### 暫停 2 秒 -> 執行的話，又會抓不到
        # time.sleep(2) # 暫停 3 秒，方便觀察搜尋框輸入結果

        ### 按下 Enter 執行搜尋
        search_input.send_keys(Keys.ENTER)

        ### 暫停 2 秒
        time.sleep(2) # 暫停 3 秒，方便觀察搜尋框輸入結果

        ### 顯示搜尋後的標題
        result_title = driver.find_element(
            By.ID,
            "firstHeading"
        )

        print("\n搜尋結果標題：")
        print(result_title.text)


finally:
    driver.quit()