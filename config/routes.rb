Rails.application.routes.draw do
  root 'home#index'
  get 'equipments', to: 'equipments#index'
  get 'map', to: 'map#index'
  get 'search', to: 'gyms#search'
  resources :map, only: [:index]
end