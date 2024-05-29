import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'  # JSONファイルのパスを設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID = '1NgI3RpS8Nzd6-fkXJBLtsp6DTOaSZ5SFwl0g6CjgSKs'  # 正しいスプレッドシートIDを設定
RANGE_NAME = 'シート1!A1'

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# 店舗データのサンプル
data = {
    '店舗名': [
        'エニタイムフィットネス新宿西口店', 'エニタイムフィットネス新宿南口店', 'エニタイムフィットネス高田馬場店',
        'エニタイムフィットネス新宿御苑前店', 'エニタイムフィットネス新宿河田町店', 'エニタイムフィットネス新宿中井店',
        'エニタイムフィットネス曙橋店', 'エニタイムフィットネス飯田橋店', 'エニタイムフィットネス市ヶ谷店',
        'エニタイムフィットネス東新宿店', 'エニタイムフィットネス神楽坂店', 'エニタイムフィットネス早稲田店',
        'エニタイムフィットネス四谷三丁目店', 'エニタイムフィットネス大久保店', 'エニタイムフィットネス西新宿7丁目店',
        'エニタイムフィットネス新宿歌舞伎町店', 'エニタイムフィットネス新宿曙橋店'
    ],
    '住所': [
        '東京都新宿区西新宿7-8-11', '東京都新宿区新宿4-3-15 レイフラット新宿 B1F', '東京都新宿区高田馬場4-11-10',
        '東京都新宿区新宿1-24-3 新宿1丁目ビル B1F', '東京都新宿区河田町3-52', '東京都新宿区上落合3-2-4 東京トラフィック開発中井ビル',
        '東京都新宿区住吉町8-14 メゾンドK 1F-B1', '東京都新宿区下宮比町2-1 第一勧銀稲垣ビル B1', '東京都新宿区市谷田町2-17 八重洲市谷ビル B1',
        '東京都新宿区大久保1-3-15 アクロス東新宿 2F', '東京都新宿区榎町43-1 ユニゾ神楽坂ビル 1F', '東京都新宿区西早稲田3-21-5',
        '東京都新宿区四谷3-12 フォーキャスト四谷 2F', '東京都新宿区百人町1-24-4 加藤ビル 2F', '東京都新宿区西新宿7-10-19 西新宿ビル 1F',
        '東京都新宿区歌舞伎町1-1-19 コメサプラザ 3F', '東京都新宿区住吉町1-13 サンプラザ住吉 2F'
    ]
}

# データフレームの作成
df = pd.DataFrame(data)

# 住所から緯度・経度を取得する関数
def get_lat_long(api_key, address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            location = results[0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# APIキーを設定
API_KEY = "AIzaSyA2ghhF-QX1JbH36JdhWghvjMXRhigddZA"  # ここを自身のAPIキーに置き換える

# 住所から緯度・経度を取得
lat_long_data = [get_lat_long(API_KEY, address) for address in df['住所']]
df['緯度'], df['経度'] = zip(*lat_long_data)

# データをスプレッドシートに書き込む
values = [df.columns.values.tolist()] + df.values.tolist()
body = {
    'values': values
}
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                               valueInputOption='RAW', body=body).execute()

print(f"{result.get('updatedCells')} cells updated.")