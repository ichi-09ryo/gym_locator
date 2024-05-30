class MapController < ApplicationController
  def index
    @gyms = Gym.includes(:gym_equipments).all
  end
end