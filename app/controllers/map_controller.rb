class MapController < ApplicationController
  def index
    if params[:equipments].present? && params[:prefectures].present?
      equipment_names = params[:equipments].split(',')
      prefecture_names = params[:prefectures].split(',')

      equipment_ids = Equipment.where(equipment_name: equipment_names).pluck(:id)
      @gyms = Gym.joins(:gym_equipments)
                 .where(gym_equipments: { equipment_id: equipment_ids })
                 .where('address LIKE ?', "%#{prefecture_names.join('%')}%")
                 .distinct
    else
      @gyms = Gym.all
    end
  end
end