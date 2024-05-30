class EquipmentsController < ApplicationController
  def index
    @equipments = Equipment.all
    respond_to do |format|
      format.html
      format.json { render json: @equipments }
    end
  end
end