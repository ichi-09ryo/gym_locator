class MapController < ApplicationController
  def index
    Rails.logger.debug "Received params: #{params.inspect}"

    @equipments = params[:equipments].is_a?(String) ? params[:equipments].split(',') : Array(params[:equipments])
    @selected_prefecture = params[:prefectures].is_a?(Array) ? params[:prefectures].first : params[:prefectures]

    Rails.logger.debug "Equipments: #{@equipments}, Selected Prefecture: #{@selected_prefecture}"

    equipment_ids = Equipment.where(equipment_name: @equipments).pluck(:id)

    @gyms = Gym.joins(:gym_equipments)
               .where(gym_equipments: { equipment_id: equipment_ids })
               .distinct

    @gyms = @gyms.where('address LIKE ?', "%#{@selected_prefecture}%") if @selected_prefecture.present?

    if @gyms.present?
      @map_center = { lat: @gyms.first.latitude, lng: @gyms.first.longitude }
    else
      @map_center = { lat: 35.6895, lng: 139.6917 } # デフォルトは東京
      @gyms = []
    end

    Rails.logger.debug "Gyms: #{@gyms.inspect}"

    # 定義された器具と地域を設定
    @available_equipments = Equipment.select(:equipment_name).distinct.pluck(:equipment_name)
    @regions = {
      "北海道・東北" => ["北海道", "青森", "岩手", "宮城", "秋田", "山形", "福島"],
      "関東" => ["茨城", "栃木", "群馬", "埼玉", "千葉", "東京", "神奈川"],
      "中部" => ["新潟", "富山", "石川", "福井", "山梨", "長野", "岐阜", "静岡", "愛知"],
      "近畿" => ["三重", "滋賀", "京都", "大阪", "兵庫", "奈良", "和歌山"],
      "中国" => ["鳥取", "島根", "岡山", "広島", "山口"],
      "四国" => ["徳島", "香川", "愛媛", "高知"],
      "九州・沖縄" => ["福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄"]
    }
  end
end