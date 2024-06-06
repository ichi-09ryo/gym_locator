class MapController < ApplicationController
  def index
    Rails.logger.debug "Received params: #{params.inspect}"

    @equipments = params[:equipments].is_a?(String) ? params[:equipments].split(',') : Array(params[:equipments])
    @selected_prefecture = params[:prefectures].is_a?(Array) ? params[:prefectures].first : params[:prefectures]
    search_mode = params[:search_mode] || 'any'

    Rails.logger.debug "Equipments: #{@equipments}, Selected Prefecture: #{@selected_prefecture}, Search Mode: #{search_mode}"

    equipment_ids = Equipment.where(equipment_name: @equipments).pluck(:id)

    if search_mode == 'all'
      # 全て一致の場合
      @gyms = Gym.joins(:gym_equipments)
                 .where(gym_equipments: { equipment_id: equipment_ids })
                 .group('gyms.id')
                 .having('COUNT(DISTINCT gym_equipments.equipment_id) = ?', @equipments.size)
    else
      # 一部一致の場合
      @gyms = Gym.joins(:gym_equipments)
                 .where(gym_equipments: { equipment_id: equipment_ids })
                 .distinct
    end

    @gyms = @gyms.where('address LIKE ?', "%#{@selected_prefecture}%") if @selected_prefecture.present?

    if @gyms.present?
      @map_center = { lat: @gyms.first.latitude, lng: @gyms.first.longitude }
    else
      @map_center = { lat: 35.6895, lng: 139.6917 } # デフォルトは東京
      @gyms = []
    end

    Rails.logger.debug "Gyms: #{@gyms.inspect}"
  end
end