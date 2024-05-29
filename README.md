# README

This README would normally document whatever steps are necessary to get the
application up and running.

Things you may want to cover:

* Ruby version

* System dependencies

* Configuration

* Database creation

* Database initialization

* How to run the test suite

* Services (job queues, cache servers, search engines, etc.)

* Deployment instructions

* ...

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