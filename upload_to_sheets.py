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
    'https://fitplace.jp/gyms/nippori/',
    'https://fitplace.jp/gyms/higashi-yamato/',
    'https://fitplace.jp/gyms/bubaigawara/',
    'https://fitplace.jp/gyms/machiya/',
    'https://fitplace.jp/gyms/ikebukuro/',
    'https://fitplace.jp/gyms/shinjuku-nishiguchi/',
    'https://fitplace.jp/gyms/suidobashi/',
    'https://fitplace.jp/gyms/ueno/',
    'https://fitplace.jp/gyms/otsuka/',
    'https://fitplace.jp/gyms/omori/',
    'https://fitplace.jp/gyms/shimoakatsuka/',
    'https://fitplace.jp/gyms/itabashi/',
    'https://fitplace.jp/gyms/hasune/',
    'https://fitplace.jp/gyms/shin-koiwa/',
    'https://fitplace.jp/gyms/minamiasagaya/',
    'https://fitplace.jp/gyms/kanda/',
    'https://fitplace.jp/gyms/minowa/',
    'https://fitplace.jp/gyms/musashikoganei/',
    'https://fitplace.jp/gyms/kanamachi/',
    'https://fitplace.jp/gyms/hachioji/',
    'https://fitplace.jp/gyms/narimasu/',
    'https://fitplace.jp/gyms/zoshiki/',
    'https://fitplace.jp/gyms/tama-center/',
    'https://fitplace.jp/gyms/ayase/',
    'https://fitplace.jp/gyms/oyama/',
    'https://fitplace.jp/gyms/aomono-yokocho/',
    'https://fitplace.jp/gyms/dokkyo-daigakumae/',
    'https://fitplace.jp/gyms/urawa/',
    'https://fitplace.jp/gyms/honkawagoe/',
    'https://fitplace.jp/gyms/kawaguchi/',
    'https://fitplace.jp/gyms/tokorozawa/',
    'https://fitplace.jp/gyms/koshigaya/',
    'https://fitplace.jp/gyms/kumagaya/',
    'https://fitplace.jp/gyms/chiba-chuo/',
    'https://fitplace.jp/gyms/tsuga/',
    'https://fitplace.jp/gyms/gyotoku/',
    'https://fitplace.jp/gyms/tsudanuma/',
    'https://fitplace.jp/gyms/shin-matsudo/',
    'https://fitplace.jp/gyms/motoyawata/',
    'https://fitplace.jp/gyms/sagamiono/',
    'https://fitplace.jp/gyms/gumyoji/',
    'https://fitplace.jp/gyms/hiratsuka/',
    'https://fitplace.jp/gyms/kawasaki/',
    'https://fitplace.jp/gyms/ofuna/',
    'https://fitplace.jp/gyms/minatomirai/',
    'https://fitplace.jp/gyms/kannai/',
    'https://fitplace.jp/gyms/sano/',
    'https://fitplace.jp/gyms/nagaoka/',
    'https://fitplace.jp/gyms/koufu-mukomachi/',
    'https://fitplace.jp/gyms/shizuoka-2/',
    'https://fitplace.jp/gyms/obu/',
    'https://fitplace.jp/gyms/mikawa-anjou/',
    'https://fitplace.jp/gyms/hisaya-odori/',
    'https://fitplace.jp/gyms/handa/',
    'https://fitplace.jp/gyms/kasugai/',
    'https://fitplace.jp/gyms/ichinomiya/',
    'https://fitplace.jp/gyms/meiyontango-dori/',
    'https://fitplace.jp/gyms/neyagawa/',
    'https://fitplace.jp/gyms/bentencho/',
    'https://fitplace.jp/gyms/kyobashi/',
    'https://fitplace.jp/gyms/kire-uriwari/',
    'https://fitplace.jp/gyms/tamade/',
    'https://fitplace.jp/gyms/teradacho/',
    'https://fitplace.jp/gyms/nagai/',
    'https://fitplace.jp/gyms/korien/',
    'https://fitplace.jp/gyms/esaka/',
    'https://fitplace.jp/gyms/kameoka/',
    'https://fitplace.jp/gyms/saiin/',
    'https://fitplace.jp/gyms/hyakumamben/',
    'https://fitplace.jp/gyms/nishi-oji/',
    'https://fitplace.jp/gyms/himeji-imajyuku/',
    'https://fitplace.jp/gyms/rokko/',
    'https://fitplace.jp/gyms/sannomiya/',
    'https://fitplace.jp/gyms/otsu-seta/',
    'https://fitplace.jp/gyms/matsue/',
    'https://fitplace.jp/gyms/fukuoka-imajuku/',
    'https://fitplace.jp/gyms/kokura-kuzuhara/',
    'https://fitplace.jp/gyms/hakata-gion/',
    'https://fitplace.jp/gyms/kokura/',
    'https://fitplace.jp/gyms/ohashi/',
    'https://fitplace.jp/gyms/miyazaki-oshima/'

]

data = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 店舗名の抽出
    name_tag = soup.find('h1', class_='page-fv__tit')
    name = name_tag.get_text().strip() if name_tag else None
    
    # 住所の抽出
    address_tag = soup.find('p', class_='single-store-common__txt single-store-address__txt')
    address = address_tag.get_text().strip() if address_tag else None
    
    if name and address:
        data.append({'店舗名': name, '住所': address})

# データフレームの作成
df = pd.DataFrame(data)

# データフレームを表示して確認
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