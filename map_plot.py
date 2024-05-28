import gmplot
import pandas as pd

# 店舗データのサンプル
data = {
    'name': ['Gym 1', 'Gym 2', 'Gym 3'],
    'latitude': [35.6895, 35.6897, 35.6899],
    'longitude': [139.6917, 139.6921, 139.6923]
}

# データフレームの作成
df = pd.DataFrame(data)

# 正しいAPIキーを設定
gmap = gmplot.GoogleMapPlotter(35.6895, 139.6917, 13, apikey='AIzaSyA2ghhF-QX1JbH36JdhWghvjMXRhigddZA')

# ジムの位置をマップにプロット
gmap.scatter(df['latitude'], df['longitude'], '#FF0000', size=40, marker=False)

# マップをHTMLファイルとして保存
gmap.draw('gyms_map.html')

print("マップを作成しました。gyms_map.htmlをブラウザで開いてください。")