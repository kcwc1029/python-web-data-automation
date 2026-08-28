from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


### 啟動 Chrome
driver = webdriver.Chrome()
driver.maximize_window()


### 開啟中華郵政網頁
try:
    driver.get("https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=208")


    ### 暫停 2 秒
    time.sleep(2) # 暫停 2 秒，方便觀察網頁


    ### 找到縣市下拉選單
    city_element = driver.find_element(
        By.ID,
        "city_zip6"
    )


    ### 建立 Select 物件
    city_select = Select(city_element)


    ### 選擇臺南市
    city_select.select_by_visible_text("臺南市")


    ### 顯示目前選擇的縣市
    print("目前選擇：")
    print(city_select.first_selected_option.text)


    ### 暫停 3 秒
    time.sleep(3) # 暫停 3 秒，方便觀察選擇結果


finally:
    driver.quit()