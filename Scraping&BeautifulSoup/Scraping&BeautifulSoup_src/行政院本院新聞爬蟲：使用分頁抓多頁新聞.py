# 行政院本院新聞爬蟲：使用分頁抓多頁新聞

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


### 設定網址
base_url = "https://www.ey.gov.tw/Page/6485009ABEC1CB9C"

headers = {
    "User-Agent": "Mozilla/5.0"
}


### 建立新聞資料
news_list = []


### 抓取前 5 頁
for page in range(1, 6):

    print(f"\n正在抓取第 {page} 頁")


    ### 設定分頁網址
    url = f"{base_url}?PS=15&page={page}"

    print("網址：", url)


    ### 發送 HTTP 請求
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    ) # 向行政院新聞列表頁發送 GET 請求

    response.raise_for_status()

    print("狀態碼：", response.status_code)


    ### 建立 BeautifulSoup
    soup = BeautifulSoup(
        response.text,
        "lxml"
    )


    ### 找出新聞詳細頁連結
    links = soup.select(
        'a[href*="/Page/9277F759E41CCD91/"]'
    ) # 找出一般新聞詳細頁連結


    ### 處理這一頁的新聞
    page_count = 0

    for link in links:

        title = link.get_text(
            " ",
            strip=True
        ) # 取得新聞標題


        href = link.get(
            "href"
        ) # 取得新聞連結


        if not href:
            continue


        ### 建立完整網址
        news_url = urljoin(
            base_url,
            href
        )


        ### 避免抓到重複新聞
        existing_urls = [
            item["網址"]
            for item in news_list
        ]

        if news_url in existing_urls:
            continue


        ### 加入資料
        news_list.append({
            "頁數": page,
            "標題": title,
            "網址": news_url
        })

        page_count += 1


    ### 顯示這一頁抓到幾筆
    print(
        f"第 {page} 頁抓到：",
        page_count,
        "筆"
    )


### 轉換成 DataFrame
news_df = pd.DataFrame(
    news_list
)


### 加入排名
news_df.insert(
    0,
    "排名",
    range(
        1,
        len(news_df) + 1
    )
)


### 顯示結果
print("\n新聞列表：")

print(news_df)


### 儲存 CSV
news_df.to_csv(
    "行政院本院新聞_5頁.csv",
    index=False,
    encoding="utf-8-sig"
)


### 執行完成
print("\n資料抓取完成")
print("總共抓到：", len(news_df), "筆新聞")
print("已產生：行政院本院新聞_5頁.csv")