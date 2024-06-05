import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mysql.connector
from datetime import datetime
import difflib
import time

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID1 = '1NgI3RpS8Nzd6-fkXJBLtsp6DTOaSZ5SFwl0g6CjgSKs'
RANGE_NAME1 = 'シート1!A1:D10000'  # 範囲を10000に拡張
SPREADSHEET_ID2 = '1aA46jjd1cq7BhPFipSLntuusgw7YCz-ZPh_RqCtgq5A'
RANGE_NAME2 = 'シート1!A1:B10000'  # 範囲を10000に拡張

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)

# リトライロジックを追加
def get_sheet_values(service, spreadsheet_id, range_name, retries=5):
    for attempt in range(retries):
        try:
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            return result.get('values', [])
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Maximum retries reached. Exiting.")
                raise

# スプレッドシート1のデータを取得
values1 = get_sheet_values(service, SPREADSHEET_ID1, RANGE_NAME1)

# スプレッドシート2のデータを取得
values2 = get_sheet_values(service, SPREADSHEET_ID2, RANGE_NAME2)

# データフレームの作成
df1 = pd.DataFrame(values1[1:], columns=values1[0])
df2 = pd.DataFrame(values2[1:], columns=values2[0])

# None値を取り除く
df2 = df2.dropna(subset=['器具名'])

# 類似名を統一する関数
def normalize_equipment_names(equipment_list):
    unique_names = list(set(filter(None, equipment_list)))
    normalized_dict = {}
    for name in equipment_list:
        match = difflib.get_close_matches(name, unique_names, n=1, cutoff=0.8)
        if match:
            normalized_dict[name] = match[0]
        else:
            normalized_dict[name] = name
    return normalized_dict

# 器具名のリストを正規化
equipment_names = df2['器具名'].tolist()
normalized_names_dict = normalize_equipment_names(equipment_names)

# 正規化された名前に基づいて器具名を更新
df2['器具名'] = df2['器具名'].map(normalized_names_dict)

# MySQLデータベースに接続
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # パスワードを空に設定
    database='gym_locator_development'
)
cursor = conn.cursor()

# テーブルが存在しない場合は作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS gyms (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    gym_name VARCHAR(255),
    address VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS equipments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipment_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS gym_equipments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    gym_id BIGINT,
    equipment_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (gym_id) REFERENCES gyms(id),
    FOREIGN KEY (equipment_id) REFERENCES equipments(id)
)
''')

# データを削除して新しいデータを挿入
cursor.execute('DELETE FROM gym_equipments')
conn.commit()
cursor.execute('DELETE FROM equipments')
conn.commit()
cursor.execute('DELETE FROM gyms')
conn.commit()

# スプレッドシート1のデータをジムテーブルに挿入
for index, row in df1.iterrows():
    cursor.execute('''
    INSERT INTO gyms (gym_name, address, latitude, longitude, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', (row['店舗名'], row['住所'], row['緯度'], row['経度'], datetime.now(), datetime.now()))
    conn.commit()

# 挿入されたジムを確認
cursor.execute('SELECT gym_name FROM gyms')
gyms_inserted = cursor.fetchall()
print(f"Gyms inserted: {gyms_inserted}")

# スプレッドシート2のデータを器具テーブルに挿入
for index, row in df2.iterrows():
    equipment_name = row['器具名']
    if equipment_name:  # equipment_nameがNULLでないか確認
        cursor.execute('''
        INSERT INTO equipments (equipment_name, created_at, updated_at)
        VALUES (%s, %s, %s)
        ''', (equipment_name, datetime.now(), datetime.now()))
        conn.commit()
    else:
        print(f"Skipped insertion: equipment_name is None for row {index}")

# 挿入された器具を確認
cursor.execute('SELECT equipment_name FROM equipments')
equipments_inserted = cursor.fetchall()
print(f"Equipments inserted: {equipments_inserted}")

# gym_equipmentsテーブルにデータを挿入
for index, row in df2.iterrows():
    cursor.execute('SELECT id FROM gyms WHERE gym_name = %s', (row['店舗名'],))
    gym_id = cursor.fetchone()
    if gym_id:
        gym_id = gym_id[0]  # 結果をタプルから抽出
    cursor.fetchall()  # 残りの結果をクリア

    cursor.execute('SELECT id FROM equipments WHERE equipment_name = %s', (row['器具名'],))
    equipment_id = cursor.fetchone()
    if equipment_id:
        equipment_id = equipment_id[0]  # 結果をタプルから抽出
    cursor.fetchall()  # 残りの結果をクリア

    if gym_id and equipment_id:
        cursor.execute('''
        INSERT INTO gym_equipments (gym_id, equipment_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        ''', (gym_id, equipment_id, datetime.now(), datetime.now()))
        conn.commit()
    else:
        print(f"Gym or Equipment not found for entry: {row['店舗名']} - {row['器具名']}")

# コミットして接続を閉じる
conn.commit()
cursor.close()
conn.close()