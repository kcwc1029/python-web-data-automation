from selenium import webdriver

# `driver` 是這次瀏覽器工作階段的控制器。
driver = webdriver.Chrome() 
try:
    driver.get("https://www.youtube.com/") # `get()` 導航到網址。
    print(driver.title)
finally:
    driver.quit() # 關閉整個工作階段與所有視窗。


# `close()` 關閉目前視窗；
# `quit()` 結束整個 session。
# 爬蟲通常在工作結束使用 `quit()`。
