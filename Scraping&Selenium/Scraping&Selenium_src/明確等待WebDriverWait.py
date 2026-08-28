from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


### 啟動 Chrome
driver = webdriver.Chrome()


### 開啟網頁
try:
    driver.get("https://zh.wikipedia.org/wiki/臺灣")


    ### 建立明確等待
    wait = WebDriverWait(driver, 10)


    ### 等待文章標題出現並顯示
    title = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "firstHeading")
        )
    )

    print("文章標題：")
    print(title.text)


    ### 等待文章第一段出現在 DOM
    paragraph = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".mw-content-ltr > p")
        )
    )

    print("\n第一段內容：")
    print(paragraph.text)


finally:
    driver.quit()