import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID = '1NgI3RpS8Nzd6-fkXJBLtsp6DTOaSZ5SFwl0g6CjgSKs'
RANGE_NAME = 'シート1!A1'

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# スクレイピング対象のURLリスト
urls = [
    'https://www.anytimefitness.co.jp/hokkaido/',
    'https://www.anytimefitness.co.jp/tohoku/aomori/',
    'https://www.anytimefitness.co.jp/tohoku/iwate/',
    'https://www.anytimefitness.co.jp/tohoku/miyagi/',
    'https://www.anytimefitness.co.jp/tohoku/akita/',
    'https://www.anytimefitness.co.jp/tohoku/yamagata/',
    'https://www.anytimefitness.co.jp/tohoku/fukushima/',
    'https://www.anytimefitness.co.jp/kanto/ibaraki/',
    'https://www.anytimefitness.co.jp/kanto/tochigi/',
    'https://www.anytimefitness.co.jp/kanto/gunma/',
    'https://www.anytimefitness.co.jp/kanto/saitama/',
    'https://www.anytimefitness.co.jp/kanto/chiba/',
    'https://www.anytimefitness.co.jp/kanto/tokyo/',
    'https://www.anytimefitness.co.jp/kanto/kanagawa/',
    'https://www.anytimefitness.co.jp/chubu/niigata/',
    'https://www.anytimefitness.co.jp/chubu/toyama/',
    'https://www.anytimefitness.co.jp/chubu/ishikawa/',
    'https://www.anytimefitness.co.jp/chubu/fukui/',
    'https://www.anytimefitness.co.jp/chubu/yamanashi/',
    'https://www.anytimefitness.co.jp/chubu/nagano/',
    'https://www.anytimefitness.co.jp/chubu/gifu/',
    'https://www.anytimefitness.co.jp/chubu/shizuoka/',
    'https://www.anytimefitness.co.jp/chubu/aichi/',
    'https://www.anytimefitness.co.jp/kinki/mie/',
    'https://www.anytimefitness.co.jp/kinki/shiga/',
    'https://www.anytimefitness.co.jp/kinki/kyoto/',
    'https://www.anytimefitness.co.jp/kinki/osaka/',
    'https://www.anytimefitness.co.jp/kinki/hyogo/',
    'https://www.anytimefitness.co.jp/kinki/nara/',
    'https://www.anytimefitness.co.jp/kinki/wakayama/',
    'https://www.anytimefitness.co.jp/chugoku/tottori/',
    'https://www.anytimefitness.co.jp/chugoku/shimane/',
    'https://www.anytimefitness.co.jp/chugoku/okayama/',
    'https://www.anytimefitness.co.jp/chugoku/hiroshima/',
    'https://www.anytimefitness.co.jp/chugoku/yamaguchi/',
    'https://www.anytimefitness.co.jp/shikoku/tokushima/',
    'https://www.anytimefitness.co.jp/shikoku/kagawa/',
    'https://www.anytimefitness.co.jp/shikoku/ehime/',
    'https://www.anytimefitness.co.jp/shikoku/kochi/',
    'https://www.anytimefitness.co.jp/kyushu/fukuoka/',
    'https://www.anytimefitness.co.jp/kyushu/saga/',
    'https://www.anytimefitness.co.jp/kyushu/nagasaki/',
    'https://www.anytimefitness.co.jp/kyushu/kumamoto/',
    'https://www.anytimefitness.co.jp/kyushu/oita/',
    'https://www.anytimefitness.co.jp/kyushu/miyazaki/',
    'https://www.anytimefitness.co.jp/kyushu/kagoshima/',
    'https://www.anytimefitness.co.jp/kyushu/okinawa/'
]

data = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 店舗名と住所を取得
    shops = soup.find_all('li')
    for shop in shops:
        name = shop.find('p', class_='name').get_text() if shop.find('p', class_='name') else None
        address = shop.find('p', class_='address').get_text() if shop.find('p', class_='address') else None
        if name and address:
            data.append({'店舗名': name, '住所': address})

# データフレームの作成
df = pd.DataFrame(data)

# データフレームを表示
print(df)

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
API_KEY = "AIzaSyA2ghhF-QX1JbH36JdhWghvjMXRhigddZA"

# 住所から緯度・経度を取得
if not df.empty:
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
else:
    print("No data to update in the spreadsheet.")