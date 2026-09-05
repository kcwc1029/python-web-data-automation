import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


### 設定網址
url = "https://www.ey.gov.tw/Page/6485009ABEC1CB9C"

headers = {
    "User-Agent": "Mozilla/5.0"
}


### 發送 HTTP 請求
response = requests.get(
    url,
    headers=headers,
    timeout=10
) # 向行政院本院新聞頁面發送 GET 請求

response.raise_for_status() # 如果請求失敗 (4xx、5xx)，直接拋出例外

print("列表頁狀態碼：", response.status_code)


### 建立 BeautifulSoup
soup = BeautifulSoup(
    response.text,
    "lxml"
) # 將列表頁 HTML 交給 BeautifulSoup 解析


### 找出新聞詳細頁連結
news_links = []

links = soup.select(
    'a[href*="/Page/9277F759E41CCD91/"]'
) # 找出一般新聞的詳細頁連結


for link in links:

    title = link.get_text(
        " ",
        strip=True
    ) # 取得連結文字

    href = link.get(
        "href"
    ) # 取得 href

    news_url = urljoin(
        url,
        href
    ) # 將相對網址轉換成完整網址


    ### 排除重複網址
    if news_url not in news_links:
        news_links.append(news_url)


### 顯示找到的新聞數量
print("找到新聞數量：", len(news_links))


### 建立新聞資料
news_list = []


### 逐篇進入新聞詳細頁
for index, news_url in enumerate(news_links, start=1):

    print(
        f"\n正在抓取第 {index} 篇：",
        news_url
    )


    ### 發送詳細頁 HTTP 請求
    news_response = requests.get(
        news_url,
        headers=headers,
        timeout=10
    )

    news_response.raise_for_status()


    ### 建立詳細頁 BeautifulSoup
    news_soup = BeautifulSoup(
        news_response.text,
        "lxml"
    )


    ### 抓取新聞標題
    title_tag = news_soup.select_one(
        "h2"
    )

    if title_tag:
        title = title_tag.get_text(
            " ",
            strip=True
        )
    else:
        title = ""


    ### 抓取日期
    date = ""

    text = news_soup.get_text(
        "\n",
        strip=True
    )

    for line in text.split("\n"):

        if line.startswith("日期："):
            date = line.replace(
                "日期：",
                ""
            ).strip()

            break


    ### 抓取資料來源
    source = ""

    for line in text.split("\n"):

        if line.startswith("資料來源："):
            source = line.replace(
                "資料來源：",
                ""
            ).strip()

            break


    ### 找出新聞主要內容區域
    content_tag = news_soup.select_one(
        ".news_content"
    )


    ### 如果找不到指定 class，改用主要內容區塊
    if content_tag is None:
        content_tag = news_soup.select_one(
            "main"
        )


    ### 抓取完整內文
    content = ""

    if content_tag:

        paragraphs = content_tag.select(
            "p"
        ) # 找出內文中的所有段落

        paragraph_list = []

        for paragraph in paragraphs:

            paragraph_text = paragraph.get_text(
                " ",
                strip=True
            )

            if paragraph_text:
                paragraph_list.append(
                    paragraph_text
                )


        content = "\n".join(
            paragraph_list
        )


    ### 加入資料
    news_list.append({
        "標題": title,
        "日期": date,
        "資料來源": source,
        "內文": content,
        "網址": news_url
    })


### 轉換成 DataFrame
news_df = pd.DataFrame(
    news_list
)


### 顯示結果
print("\n新聞資料：")

print(
    news_df[
        [
            "標題",
            "日期",
            "資料來源"
        ]
    ]
)


### 儲存 CSV
news_df.to_csv(
    "行政院本院新聞_完整內文.csv",
    index=False,
    encoding="utf-8-sig"
) # 使用 utf-8-sig，避免 Excel 開啟中文 CSV 時出現亂碼


### 執行完成
print("\n資料抓取完成")
print("共抓到：", len(news_df), "篇新聞")
print("已產生：行政院本院新聞_完整內文.csv")