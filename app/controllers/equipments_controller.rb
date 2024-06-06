class EquipmentsController < ApplicationController
  require 'google/apis/sheets_v4'
  require 'googleauth'

  def index
    service = Google::Apis::SheetsV4::SheetsService.new
    service.client_options.application_name = 'Gym Locator'
    service.authorization = Google::Auth::ServiceAccountCredentials.make_creds(
      json_key_io: File.open('keen-dispatch-424708-v5-53a1436f17bd.json'),
      scope: Google::Apis::SheetsV4::AUTH_SPREADSHEETS_READONLY
    )

    spreadsheet_id = '1aA46jjd1cq7BhPFipSLntuusgw7YCz-ZPh_RqCtgq5A'
    range = 'シート1!B2:B1000'
    response = service.get_spreadsheet_values(spreadsheet_id, range)
    
    @equipments = response.values.flatten if response.values

    respond_to do |format|
      format.html
      format.json { render json: @equipments }
    end
  end
  def search
    # パラメータを取得
    selected_equipments = params[:equipments].split(',')
    selected_prefecture = params[:prefectures].first

    # ジムを検索
    @gyms = Gym.joins(:equipments)
               .where(equipments: { equipment_name: selected_equipments })
               .where(prefecture: selected_prefecture)
               .distinct

    # 結果をビューに渡す
    respond_to do |format|
      format.html { render :search_results } # 検索結果を表示するためのビューを指定
      format.json { render json: @gyms }
    end
  end
end