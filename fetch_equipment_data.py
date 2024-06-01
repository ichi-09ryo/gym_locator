import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mysql.connector
from datetime import datetime

# サービスアカウントキーのJSONファイルパス
SERVICE_ACCOUNT_FILE = 'keen-dispatch-424708-v5-53a1436f17bd.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# スプレッドシートIDと範囲を設定
SPREADSHEET_ID1 = '1NgI3RpS8Nzd6-fkXJBLtsp6DTOaSZ5SFwl0g6CjgSKs'  # 店舗名、住所、緯度、経度のスプレッドシートID
RANGE_NAME1 = 'シート1!A1:D100'
SPREADSHEET_ID2 = '1aA46jjd1cq7BhPFipSLntuusgw7YCz-ZPh_RqCtgq5A'  # 店舗名、器具名のスプレッドシートID
RANGE_NAME2 = 'シート1!A1:B100'

# サービスアカウントの認証情報を設定
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets APIのサービスを作成
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# スプレッドシート1のデータを取得
result1 = sheet.values().get(spreadsheetId=SPREADSHEET_ID1, range=RANGE_NAME1).execute()
values1 = result1.get('values', [])

# スプレッドシート2のデータを取得
result2 = sheet.values().get(spreadsheetId=SPREADSHEET_ID2, range=RANGE_NAME2).execute()
values2 = result2.get('values', [])

# データフレームの作成
df1 = pd.DataFrame(values1[1:], columns=values1[0])
df2 = pd.DataFrame(values2[1:], columns=values2[0])

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
cursor.execute('DELETE FROM equipments')
cursor.execute('DELETE FROM gyms')

# スプレッドシート1のデータをジムテーブルに挿入
for index, row in df1.iterrows():
    cursor.execute('''
    INSERT INTO gyms (gym_name, address, latitude, longitude, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', (row['店舗名'], row['住所'], row['緯度'], row['経度'], datetime.now(), datetime.now()))

# スプレッドシート2のデータを器具テーブルに挿入
for index, row in df2.iterrows():
    cursor.execute('''
    INSERT INTO equipments (equipment_name, created_at, updated_at)
    VALUES (%s, %s, %s)
    ''', (row['器具名'], datetime.now(), datetime.now()))

# gym_equipmentsテーブルにデータを挿入
for index, row in df2.iterrows():
    cursor.execute('SELECT id FROM gyms WHERE gym_name = %s', (row['店舗名'],))
    gym_id = cursor.fetchone()
    cursor.execute('SELECT id FROM equipments WHERE equipment_name = %s', (row['器具名'],))
    equipment_id = cursor.fetchone()
    if gym_id and equipment_id:
        cursor.execute('''
        INSERT INTO gym_equipments (gym_id, equipment_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        ''', (gym_id[0], equipment_id[0], datetime.now(), datetime.now()))
    else:
        print(f"Gym or Equipment not found for entry: {row}")

# コミットして接続を閉じる
conn.commit()
cursor.close()
conn.close()