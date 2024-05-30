class Gym < ApplicationRecord
  has_many :gym_equipments
  has_many :equipments, through: :gym_equipments
end