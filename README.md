## アプリケーション名
gym_locator

## アプリケーション概要
・エニタイム専用で器具からジムを検索できます。

## URL
https://gym-locator.onrender.com

## テスト用アカウント
・Basic認証パスワード:0405
・Basic認証ID:ichioka


## 利用方法
1_トップページから器具、都道府県を選択し検索できます。
2_遷移画面でも検索が可能です。


## アプリケーションを作成した背景
近年、ジムに通い出す人が増え、エニタイムの会員数が80万人ともう少しで100万にいきそうな勢いです。
ジムに通う中で、最寄りの店舗にない器具でトレーニングをしたくなる方が一定はいます。
その一定数の方に向け、開発する運びとなりました。

## 実装予定の機能
・現在は一つの器具しか選択できないようにしていますが、それを三つ選択しても検索できるようにする予定です。
・ジムのお気に入り機能を追加する予定です。

## データベース設計
[![Image from Gyazo](https://i.gyazo.com/d5adf26f08d220ac04584ab8b8ab0d01.png)](https://gyazo.com/d5adf26f08d220ac04584ab8b8ab0d01)

## 画面遷移図
[![Image from Gyazo](https://i.gyazo.com/6f29cbdc682b82b31fab91854122a5dc.png)](https://gyazo.com/6f29cbdc682b82b31fab91854122a5dc)




## gymsテーブル
| Column | Type | Options |
| ------ | ---- | ------- |
| gym_name | string | null:false |
| address | string | null:false |
| latitude | string | null:false |
| longitude | string | null:false |

### Association
- has_many :gym_equipments
- has_many :equipments, through: :gym_equipments


## equipmentsテーブル
| Column | Type | Options |
| ------ | ---- | ------- |
| machine_name | string | null:false |

### Association
- has_many :gym_equipments
- has_many :gyms, through: :gym_equipments


## gym_equipmentsテーブル
| Column | Type | Options |
| ------ | ---- | ------- |
| gym | references | null: false, foreign_key: true |
| equipment | references | null: false, foreign_key: true |

### Association
- belongs_to :gym
- belongs_to :equipment