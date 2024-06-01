class MapController < ApplicationController
  def index
    if params[:equipments].present?
      equipment_names = params[:equipments].split(',')
      equipment_ids = Equipment.where(equipment_name: equipment_names).pluck(:id)
      @gyms = Gym.joins(:gym_equipments).where(gym_equipments: { equipment_id: equipment_ids }).distinct
    else
      @gyms = Gym.all
    end

    respond_to do |format|
      format.html
    end
  end
end