import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'  # JSONファイルのパスを設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID = '1aA46jjd1cq7BhPFipSLntuusgw7YCz-ZPh_RqCtgq5A'  # 器具用スプレッドシートIDを設定
RANGE_NAME = 'シート1!A1'

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# 店舗とURLのリスト
stores = [
    {'name': '曙橋店', 'url': 'https://www.anytimefitness.co.jp/akebonobashi/facility/'},
    # 他の店舗の情報をここに追加
]

# 全ての店舗のデータを格納するリスト
all_data = []

# 各店舗のデータを取得
for store in stores:
    response = requests.get(store['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    # 器具データの抽出
    equipment_data = []
    for item in soup.select('.machine-list li'):
        equipment_data.append(item.text.strip())

    # 店舗名と器具名のリストを作成
    for equipment in equipment_data:
        all_data.append([store['name'], equipment])

# データフレームの作成
df = pd.DataFrame(all_data, columns=['店舗名', '器具名'])

# データをスプレッドシートに書き込む
values = [df.columns.values.tolist()] + df.values.tolist()
body = {
    'values': values
}
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                               valueInputOption='RAW', body=body).execute()

print(f"{result.get('updatedCells')} cells updated.")