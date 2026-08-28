# Selenium 爬蟲：從動態網頁到 BeautifulSoup

## 🔴先決定是否需要 Selenium

三條爬蟲路線

### 🟡路線 A：Requests + JSON

若 JavaScript 只是呼叫 API 取得 JSON，通常直接使用 API 更快、更省記憶體，也較容易檢查欄位。但「在 Network 看得到」不等於自動獲得使用授權；仍要確認服務條款、驗證方式、資料授權和頻率限制。

```python
response = requests.get("https://example.com/api/jobs", timeout=10)
response.raise_for_status()
data = response.json()
```

> 範例：之前交的API都是~

### 🟡路線 B：Requests + BeautifulSoup

適合資料直接存在網站回傳的 HTML：新聞列表、文章內文、Wikipedia、HTML 表格、排行榜、一般分頁、標題、作者、日期、價格與連結。

```python
import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://example.com/news",
    headers={"User-Agent": "TrainingCrawler/1.0"},
    timeout=10,
)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")
news_list = soup.select(".news-item")
```

> 範例：BeautifulSoup~

### 🟡路線 C：Selenium

適合必須完成瀏覽器行為後資料才出現：

- 點擊「載入更多」或無限捲動。
- 切換頁籤、選擇縣市或日期後才載入。
- 點開對話框後才顯示。
- 經一般登入流程才能看，而且自動化被明確允許。
- 頁面內容必須執行 JavaScript 才建立。
- Requests 回傳 HTML 裡沒有目標資料，也沒有合適的可用 API。

Selenium 真的啟動瀏覽器，因此慢、耗記憶體，並容易受動畫、彈窗與載入時序影響。它是必要時使用的工具，不是預設答案。

## 🔴[第一支Selenium](./Scraping&Selenium_src/第一支Selenium.py)

## 🔴[ChromeOptions 與 Headless 模式(有頭與無頭模式)](./Scraping&Selenium_src/無頭模式.py)

Selenium 啟動 Chrome 時，可以透過 `ChromeOptions()` 設定瀏覽器的啟動方式。

```python
options = webdriver.ChromeOptions()
options.add_argument("--headless=new") # 使用無頭模式，不顯示 Chrome 視窗
options.add_argument("--window-size=1280,900") # 固定瀏覽器視窗尺寸
driver = webdriver.Chrome(options=options) # Selenium 就會按照這些設定啟動 Chrome。
```

流程會變成：

```
Python
  ↓
Selenium
  ↓
Chrome 在背景執行
  ↓
沒有瀏覽器視窗顯示
```

## 🔴定位與操作元素

### 🟡[find_element 與 find_elements](./Scraping&Selenium_src/find_element.py)

| 方法            | 找到              | 找不到                        |
| --------------- | ----------------- | ----------------------------- |
| `find_element`  | 第一個 WebElement | 拋出 `NoSuchElementException` |
| `find_elements` | WebElement 清單   | 空清單                        |

Selenium 的 WebElement 是瀏覽器中「活的元素參照」；BeautifulSoup 的 Tag 是某份 HTML 快照裡的節點。JavaScript 改掉 DOM 後，舊 WebElement 可能失效，產生 `StaleElementReferenceException`。

```python
### 定位方式
driver.find_element(By.ID, "search")
driver.find_element(By.NAME, "keyword")
driver.find_element(By.CSS_SELECTOR, ".job-card .detail-button")
driver.find_element(By.XPATH, "//button[contains(., '載入更多')]")
```

使用方式沿用 BeautifulSoup 的 CSS Selector，因為一套知識可同時用在兩邊。穩定性通常優先考慮語意清楚的 `id`、`name`、`data-*` 或 class；避免依賴第幾個 div、視覺位置、隨機產生的 class。

### 🟡讀取與操作

```python
element.text                       # 畫面可見文字
element.get_attribute("href")      # 屬性值
element.get_property("value")     # DOM property
element.is_displayed()             # 是否顯示
element.is_enabled()               # 是否可操作
element.click()                    # 點擊
element.send_keys("Python")        # 輸入
element.clear()                    # 清除欄位
```

下拉選單使用 `Select` 更能表達目的：

```python
from selenium.webdriver.support.ui import Select

Select(driver.find_element(By.ID, "city")).select_by_visible_text("臺中市")
```

- [範例：讀取元素資料](./Scraping&Selenium_src/讀取元素資料.py)
- [範例：操作輸入框與按鈕](./Scraping&Selenium_src/操作輸入框與按鈕.py)
- [範例：操作下拉選單：操作中華郵政縣市下拉選單為例](./Scraping&Selenium_src/操作下拉選單.py)

## 🔴等待是 Selenium 的核心

### 🟡為什麼 `driver.get()` 完成還不夠

瀏覽器完成初始頁面載入，不代表後續 JavaScript 已取得資料。程式與網站像兩位跑者：有時網站先到，有時程式先到，便形成 race condition。這就是「昨天能跑、今天偶爾壞」的常見根源。

### 🟡(不推薦)第一種：用固定sleep當主要等待

```python
import time
time.sleep(5)
```

如果網頁只花 0.5 秒就載入完成，程式還是會停滿 5 秒，白白浪費 4.5 秒。反過來，若網頁需要 6 秒才完成，等待 5 秒後仍然可能找不到元素。

### 🟡[第二種：隱含等待implicitly_wait](./Scraping&Selenium_src/隱含等待implicitly_wait.py)

隱含等待會告訴 Selenium：找不到元素時，最多再等幾秒。

設定一次後，後面的 find_element() 與 find_elements() 都會受到影響。

```py
driver.implicitly_wait(10)
```

這不是每次都固定停 10 秒。若元素在第 2 秒出現，Selenium 就會立刻繼續；只有一直找不到時，才會等到接近 10 秒。

它的優點是寫法簡單，但只能處理「元素是否找得到」，不能精確表達更多條件，例如：

- 元素已經顯示
- 按鈕已經可以點擊
- 指定文字已經出現
- Loading 遮罩已經消失
- 舊的搜尋結果已經更新

### 🟡[(推薦)第三種：明確等待WebDriverWait](./Scraping&Selenium_src/明確等待WebDriverWait.py)

明確等待可以指定「要等哪一個元素」和「元素要達成什麼狀態」。

```py
wait = WebDriverWait(driver, 10)
# 意思不是固定等待 10 秒，而是最多等待 10 秒。條件一成立，程式就立刻往下執行。
```

### 🟢[範例：基於selenium對104爬蟲](./Scraping&Selenium_src/基於selenium對104爬蟲.py)

### 🟢[範例：Quotes_to_Scrape延遲載入頁面](./Scraping&Selenium_src/Quotes_to_Scrape延遲載入頁面.py)

爬取網站：https://quotes.toscrape.com/js-delayed/ (用專門提供爬蟲練習的)

它會透過 JavaScript 延遲產生 10 筆名言，剛好能清楚示範 WebDriverWait。

## 🔵作業

- [基於Selenium對AJAX奧斯卡電影資料爬蟲](./Scraping&Selenium_src/基於Selenium對AJAX奧斯卡電影資料爬蟲.md)
- [基於Selenium做Dynamic Loading](./Scraping&Selenium_src/基於Selenium做Dynamic_Loading.md)
- [基於Selenium做Dynamic Controls](./Scraping&Selenium_src/基於Selenium做Dynamic_Controls.md)
- [基於Selenium對Web Scraper Test Sites爬蟲](./Scraping&Selenium_src/基於Selenium對Web_Scraper_Test_Sites爬蟲.md)
