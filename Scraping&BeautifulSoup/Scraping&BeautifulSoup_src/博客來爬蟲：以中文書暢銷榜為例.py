import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


### 設定網址
url = "https://www.books.com.tw/web/sys_saletopb/books"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/152.0.0.0 Safari/537.36",
    "Referer": "https://www.books.com.tw/"
}


### 發送 HTTP 請求
response = requests.get(
    url,
    headers=headers,
    timeout=10
) # 向博客來排行榜頁面發送 GET 請求

response.raise_for_status() # 如果發生 4xx 或 5xx，直接拋出例外

print("狀態碼：", response.status_code)


### 建立 BeautifulSoup
soup = BeautifulSoup(
    response.text,
    "lxml"
) # 將取得的 HTML 原始碼交給 BeautifulSoup 解析


### 找出排行榜商品
book_list = []

items = soup.select("li.item") # 找出排行榜中的每一筆商品


for item in items:

    ### 抓取書名與網址
    title_tag = item.select_one("h4 a")

    if title_tag:
        title = title_tag.get_text(" ", strip=True)

        book_url = urljoin(
            url,
            title_tag.get("href", "")
        )

    else:
        title = ""
        book_url = ""


    ### 抓取作者
    author_tag = item.select_one(".msg a")

    if author_tag:
        author = author_tag.get_text(
            " ",
            strip=True
        )
    else:
        author = ""


    ### 抓取價格
    price_tag = item.select_one(".price")

    if price_tag:
        price = price_tag.get_text(
            " ",
            strip=True
        )
    else:
        price = ""


    ### 加入資料
    if title:

        book_list.append({
            "排名": len(book_list) + 1,
            "書名": title,
            "作者": author,
            "價格": price,
            "網址": book_url
        })


### 轉換成 DataFrame
book_df = pd.DataFrame(book_list)


### 顯示結果
print("\n博客來排行榜：")

print(book_df)


### 儲存 CSV
book_df.to_csv(
    "博客來排行榜.csv",
    index=False,
    encoding="utf-8-sig"
) # utf-8-sig 可以避免 Excel 開啟中文時出現亂碼


### 執行完成
print("\n資料抓取完成")
print("共抓到：", len(book_df), "本書")
print("已產生：博客來排行榜.csv")