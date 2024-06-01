Rails.application.routes.draw do
  root 'home#index'
  get 'equipments', to: 'equipments#index'
  get 'map', to: 'map#index'
  
  resources :map, only: [:index]
end