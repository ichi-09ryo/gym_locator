import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gmplot

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'  # JSONファイルのパスを設定
SCOPES = ['https://docs.google.com/spreadsheets/d/1NgI3RpS8Nzd6-fkXJBLtsp6DTOaSZ5SFwl0g6CjgSKs/edit?usp=drive_link']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID = 'your_spreadsheet_id'
RANGE_NAME = 'シート1!A1:D100'  # 範囲は必要に応じて調整

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# スプレッドシートのデータを取得
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

# データフレームの作成
df = pd.DataFrame(values[1:], columns=values[0])

# 緯度と経度を取得
latitudes = df['緯度'].astype(float).tolist()
longitudes = df['経度'].astype(float).tolist()

# Googleマップにプロット
gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 13, apikey='YOUR_GOOGLE_MAPS_API_KEY')
gmap.scatter(latitudes, longitudes, '#FF0000', size=40, marker=False)
gmap.draw('gyms_map.html')

print("マップを作成しました。gyms_map.htmlをブラウザで開いてください。")