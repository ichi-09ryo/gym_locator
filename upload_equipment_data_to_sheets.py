import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID = '1aA46jjd1cq7BhPFipSLntuusgw7YCz-ZPh_RqCtgq5A'
RANGE_NAME = 'シート1!A1'

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# 店舗とURLのリスト
stores = [
    {'name': '日暮里', 'url': 'https://fitplace.jp/gyms/nippori/'},
    {'name': '東大和', 'url': 'https://fitplace.jp/gyms/higashi-yamato/'},
    {'name': '分倍河原', 'url': 'https://fitplace.jp/gyms/bubaigawara/'},
    {'name': '町屋', 'url': 'https://fitplace.jp/gyms/machiya/'},
    {'name': '池袋', 'url': 'https://fitplace.jp/gyms/ikebukuro/'},
    {'name': '新宿西口', 'url': 'https://fitplace.jp/gyms/shinjuku-nishiguchi/'},
    {'name': '水道橋', 'url': 'https://fitplace.jp/gyms/suidobashi/'},
    {'name': '上野', 'url': 'https://fitplace.jp/gyms/ueno/'},
    {'name': '大塚', 'url': 'https://fitplace.jp/gyms/otsuka/'},
    {'name': '大森', 'url': 'https://fitplace.jp/gyms/omori/'},
    {'name': '下赤塚', 'url': 'https://fitplace.jp/gyms/shimoakatsuka/'},
    {'name': '板橋', 'url': 'https://fitplace.jp/gyms/itabashi/'},
    {'name': '蓮根', 'url': 'https://fitplace.jp/gyms/hasune/'},
    {'name': '新小岩', 'url': 'https://fitplace.jp/gyms/shin-koiwa/'},
    {'name': '南阿佐ヶ谷', 'url': 'https://fitplace.jp/gyms/minamiasagaya/'},
    {'name': '神田', 'url': 'https://fitplace.jp/gyms/kanda/'},
    {'name': '三ノ輪', 'url': 'https://fitplace.jp/gyms/minowa/'},
    {'name': '武蔵小金井', 'url': 'https://fitplace.jp/gyms/musashikoganei/'},
    {'name': '金町', 'url': 'https://fitplace.jp/gyms/kanamachi/'},
    {'name': '八王子', 'url': 'https://fitplace.jp/gyms/hachioji/'},
    {'name': '成増', 'url': 'https://fitplace.jp/gyms/narimasu/'},
    {'name': '雑色', 'url': 'https://fitplace.jp/gyms/zoshiki/'},
    {'name': '多摩センター', 'url': 'https://fitplace.jp/gyms/tama-center/'},
    {'name': '綾瀬', 'url': 'https://fitplace.jp/gyms/ayase/'},
    {'name': '大山', 'url': 'https://fitplace.jp/gyms/oyama/'},
    {'name': '青物横丁', 'url': 'https://fitplace.jp/gyms/aomono-yokocho/'},
    {'name': '獨協大学前', 'url': 'https://fitplace.jp/gyms/dokkyo-daigakumae/'},
    {'name': '浦和', 'url': 'https://fitplace.jp/gyms/urawa/'},
    {'name': '本川越', 'url': 'https://fitplace.jp/gyms/urawa/'},
    {'name': '川口', 'url': 'https://fitplace.jp/gyms/kawaguchi/'},
    {'name': '所沢', 'url': 'https://fitplace.jp/gyms/tokorozawa/'},
    {'name': '越谷', 'url': 'https://fitplace.jp/gyms/koshigaya/'},
    {'name': '熊谷', 'url': 'https://fitplace.jp/gyms/kumagaya/'},
    {'name': '千葉中央', 'url': 'https://fitplace.jp/gyms/chiba-chuo/'},
    {'name': '都賀', 'url': 'https://fitplace.jp/gyms/tsuga/'},
    {'name': '行徳', 'url': 'https://fitplace.jp/gyms/gyotoku/'},
    {'name': '津田沼', 'url': 'https://fitplace.jp/gyms/tsudanuma/'},
    {'name': '新松戸', 'url': 'https://fitplace.jp/gyms/shin-matsudo/'},
    {'name': '本八幡', 'url': 'https://fitplace.jp/gyms/shin-matsudo/'},
    {'name': '相模大野', 'url': 'https://fitplace.jp/gyms/sagamiono/'},
    {'name': '弘明寺', 'url': 'https://fitplace.jp/gyms/gumyoji/'},
    {'name': '平塚', 'url': 'https://fitplace.jp/gyms/hiratsuka/'},
    {'name': '川崎', 'url': 'https://fitplace.jp/gyms/kawasaki/'},
    {'name': '大船', 'url': 'https://fitplace.jp/gyms/ofuna/'},
    {'name': 'みなとみらい', 'url': 'https://fitplace.jp/gyms/minatomirai/'},
    {'name': '関内', 'url': 'https://fitplace.jp/gyms/kannai/'},
    {'name': '佐野', 'url': 'https://fitplace.jp/gyms/sano/'},
    {'name': '長岡', 'url': 'https://fitplace.jp/gyms/nagaoka/'},
    {'name': '甲府向町', 'url': 'https://fitplace.jp/gyms/koufu-mukomachi/'},
    {'name': '静岡', 'url': 'https://fitplace.jp/gyms/shizuoka-2/'},
    {'name': '大府', 'url': 'https://fitplace.jp/gyms/obu/'},
    {'name': '三河安城', 'url': 'https://fitplace.jp/gyms/mikawa-anjou/'},
    {'name': '久屋大通', 'url': 'https://fitplace.jp/gyms/hisaya-odori/'},
    {'name': '半田', 'url': 'https://fitplace.jp/gyms/handa/'},
    {'name': '春日井', 'url': 'https://fitplace.jp/gyms/kasugai/'},
    {'name': '一宮', 'url': 'https://fitplace.jp/gyms/ichinomiya/'},
    {'name': '名四丹後通り', 'url': 'https://fitplace.jp/gyms/meiyontango-dori/'},
    {'name': '寝屋川', 'url': 'https://fitplace.jp/gyms/neyagawa/'},
    {'name': '弁天町', 'url': 'https://fitplace.jp/gyms/bentencho/'},
    {'name': '京橋', 'url': 'https://fitplace.jp/gyms/kyobashi/'},
    {'name': '喜連瓜破', 'url': 'https://fitplace.jp/gyms/kire-uriwari/'},
    {'name': '玉出', 'url': 'https://fitplace.jp/gyms/tamade/'},
    {'name': '寺田町', 'url': 'https://fitplace.jp/gyms/teradacho/'},
    {'name': '長居', 'url': 'https://fitplace.jp/gyms/nagai/'},
    {'name': '香里園', 'url': 'https://fitplace.jp/gyms/korien/'},
    {'name': '江坂', 'url': 'https://fitplace.jp/gyms/esaka/'},
    {'name': '亀岡', 'url': 'https://fitplace.jp/gyms/kameoka/'},
    {'name': '西院', 'url': 'https://fitplace.jp/gyms/saiin/'},
    {'name': '百万遍', 'url': 'https://fitplace.jp/gyms/hyakumamben/'},
    {'name': '西大路', 'url': 'https://fitplace.jp/gyms/nishi-oji/'},
    {'name': '姫路今宿', 'url': 'https://fitplace.jp/gyms/himeji-imajyuku/'},
    {'name': '六甲', 'url': 'https://fitplace.jp/gyms/rokko/'},
    {'name': '三宮', 'url': 'https://fitplace.jp/gyms/sannomiya/'},
    {'name': '大津瀬田', 'url': 'https://fitplace.jp/gyms/otsu-seta/'},
    {'name': '松江', 'url': 'https://fitplace.jp/gyms/matsue/'},
    {'name': '福岡今宿', 'url': 'https://fitplace.jp/gyms/fukuoka-imajuku/'},
    {'name': '小倉葛原', 'url': 'https://fitplace.jp/gyms/kokura-kuzuhara/'},
    {'name': '博多祇園', 'url': 'https://fitplace.jp/gyms/hakata-gion/'},
    {'name': '小倉', 'url': 'https://fitplace.jp/gyms/kokura/'},
    {'name': '大橋', 'url': 'https://fitplace.jp/gyms/ohashi/'},
    {'name': '宮崎大島', 'url': 'https://fitplace.jp/gyms/miyazaki-oshima/'}
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