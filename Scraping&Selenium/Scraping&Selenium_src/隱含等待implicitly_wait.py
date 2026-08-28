from selenium import webdriver
from selenium.webdriver.common.by import By


### 啟動 Chrome
driver = webdriver.Chrome()

driver.implicitly_wait(10) # 找不到元素時，最多等待 10 秒


### 開啟網頁
try:
    driver.get("https://zh.wikipedia.org/wiki/臺灣")


    ### 取得文章標題
    title = driver.find_element(
        By.ID,
        "firstHeading"
    )

    print("文章標題：")
    print(title.text)


    ### 取得文章段落
    paragraph = driver.find_element(
        By.CSS_SELECTOR,
        ".mw-content-ltr > p"
    )

    print("\n第一段內容：")
    print(paragraph.text)


finally:
    driver.quit()