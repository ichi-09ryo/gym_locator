class HomeController < ApplicationController
  def index
    @equipments = Equipment.all
  end
end