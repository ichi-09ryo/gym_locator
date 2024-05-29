import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

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
    '店舗名': ['エニタイム渋谷店', 'エニタイム新宿店', 'エニタイム池袋店'],
    '住所': ['東京都渋谷区道玄坂1丁目', '東京都新宿区西新宿1丁目', '東京都豊島区西池袋1丁目'],
    '緯度': [35.6581, 35.6895, 35.7284],
    '経度': [139.7017, 139.6917, 139.7156]
}

# データフレームの作成
df = pd.DataFrame(data)

# データをスプレッドシートに書き込む
values = [df.columns.values.tolist()] + df.values.tolist()
body = {
    'values': values
}
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                               valueInputOption='RAW', body=body).execute()

print(f"{result.get('updatedCells')} cells updated.")