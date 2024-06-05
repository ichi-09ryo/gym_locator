class MapController < ApplicationController
  def index
    @equipments = params[:equipments]
    @selected_prefecture = params[:prefectures].first # 都道府県の選択を取得
    equipment_ids = Equipment.where(equipment_name: @equipments).pluck(:id)
    @gyms = Gym.joins(:gym_equipments).where(gym_equipments: { equipment_id: equipment_ids }).distinct
    @gyms = @gyms.where('address LIKE ?', "%#{@selected_prefecture}%") if @selected_prefecture.present?

    if @gyms.present?
      @map_center = { lat: @gyms.first.latitude, lng: @gyms.first.longitude }
    else
      @map_center = { lat: 35.6895, lng: 139.6917 } # デフォルトは東京
    end
  end
end