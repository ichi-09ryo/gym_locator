class Equipment < ApplicationRecord
  self.table_name = "equipments"
  has_many :gym_equipments
  has_many :gyms, through: :gym_equipments
end