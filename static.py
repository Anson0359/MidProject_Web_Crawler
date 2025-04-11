# 安裝套件
#pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.yzu.edu.tw/index.php/tw/news-tw/msg-tw"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.encoding = "utf-8"  # 確保中文顯示正常

# 篩選所需資料
soup = BeautifulSoup(response.text, "html.parser")
content = soup.find('div',class_="com-content-article__body")
datas = content.find_all('a')

#from google.colab import files
news_data = []
for data in datas:
    data_text = data.get_text()
    link = data['href']
    news_data.append([data_text,link])

# 存入 DataFrame
df = pd.DataFrame(news_data, columns=['標題', '鏈結'])

print(f"\n✅ 成功取得 {len(df)} 公告的資料")

# --- Step 4: 寫入 CSV 並提供下載 ---
csv_filename = 'static.csv'
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
print(f"\n📁 資料已寫入 CSV 檔案：{csv_filename}")

# 提供下載連結
#files.download(csv_filename)