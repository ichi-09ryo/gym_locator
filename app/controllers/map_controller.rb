# app/controllers/map_controller.rb
class MapController < ApplicationController
  def index
    Rails.logger.debug "Received params: #{params.inspect}"

    # パラメータが文字列の場合、配列に変換
    @equipments = params[:equipments].is_a?(String) ? params[:equipments].split(',') : Array(params[:equipments])
    @selected_prefecture = params[:prefectures].is_a?(Array) ? params[:prefectures].first : params[:prefectures]

    Rails.logger.debug "Equipments: #{@equipments}, Selected Prefecture: #{@selected_prefecture}"

    if @equipments.present? && @selected_prefecture.present?
      equipment_ids = Equipment.where(equipment_name: @equipments).pluck(:id)

      @gyms = Gym.joins(:gym_equipments)
                 .where(gym_equipments: { equipment_id: equipment_ids })
                 .where('address LIKE ?', "%#{@selected_prefecture}%")
                 .distinct
    else
      @gyms = Gym.none
    end

    if @gyms.present?
      @map_center = { lat: @gyms.first.latitude, lng: @gyms.first.longitude }
    else
      @map_center = { lat: 35.6895, lng: 139.6917 } # 東京
      @gyms = []
    end

    Rails.logger.debug "Gyms: #{@gyms.inspect}"

    # 定義された器具と都道府県
    @available_equipments = Equipment.select(:equipment_name).distinct.pluck(:equipment_name)
    @regions = {
      "北海道・東北" => ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"],
      "関東" => ["茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県"],
      "中部" => ["新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県"],
      "近畿" => ["三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県"],
      "中国" => ["鳥取県", "島根県", "岡山県", "広島県", "山口県"],
      "四国" => ["徳島県", "香川県", "愛媛県", "高知県"],
      "九州・沖縄" => ["福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]
    }
  end
end