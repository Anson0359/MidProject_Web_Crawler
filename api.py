# 安裝必要套件
#!pip install --upgrade google-api-python-client

from googleapiclient.discovery import build
import pandas as pd
#from google.colab import files

# API KEY
API_KEY = 'AIzaSyDGekS2xl101BlQF6v6Os2YKEI0kJd6Uho'

# 播放清單 ID
playlist_id = 'PLPv8cjlOsZJOeUIOnKWvO1UsWP-2Bu0R1'

# 建立 API 客戶端
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 取得播放清單中的所有影片 ID
video_ids = []
next_page_token = None

print("📥 正在取得播放清單中的影片 ID...")

while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )
    pl_response = pl_request.execute()

    video_ids += [item['contentDetails']['videoId'] for item in pl_response['items']]
    next_page_token = pl_response.get('nextPageToken')
    
    if not next_page_token:
        break

print(f"✅ 播放清單中共有 {len(video_ids)} 部影片")

# 批次取得影片資訊
video_data = []
not_found_ids = []

for i in range(0, len(video_ids), 50):
    batch_ids = video_ids[i:i+50]

    video_request = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(batch_ids)
    )
    video_response = video_request.execute()

    found_ids = [item['id'] for item in video_response['items']]
    missing_ids = set(batch_ids) - set(found_ids)
    not_found_ids.extend(missing_ids)

    for item in video_response['items']:
        title = item['snippet'].get('title', 'N/A')
        published_at = item['snippet'].get('publishedAt', 'N/A')
        channel_title = item['snippet'].get('channelTitle', 'N/A')
        views = item['statistics'].get('viewCount', 'N/A')
        likes = item['statistics'].get('likeCount', 'N/A')
        comments = item['statistics'].get('commentCount', 'N/A')
        video_id = item['id']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        video_data.append([
            title, published_at, channel_title, views, likes, comments, video_id, video_url
        ])

# 存入 DataFrame
df = pd.DataFrame(video_data, columns=[
    '標題', '發布時間', '頻道名稱', '觀看次數', '按讚數', '留言數', '影片ID', '影片連結'
])

print(f"\n✅ 成功取得 {len(df)} 部影片的資料")
if not_found_ids:
    print(f"\n⚠️ 有 {len(not_found_ids)} 部影片無法取得（可能是私人、刪除、受限）：")
    for vid in not_found_ids:
        print(f"https://www.youtube.com/watch?v={vid}")

# 寫入 CSV
csv_filename = 'api.csv'
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
print(f"\n📁 資料已寫入 CSV 檔案：{csv_filename}")

# 提供下載連結
#files.download(csv_filename)