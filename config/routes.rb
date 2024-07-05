Rails.application.routes.draw do
  devise_for :users, controllers: {
    omniauth_callbacks: 'users/omniauth_callbacks'
  }
  
  root 'home#index'
  get 'equipments', to: 'equipments#index'
  get 'map', to: 'map#index'
  get 'search', to: 'gyms#search'
  resources :map, only: [:index]
  # 利用規約ページのルートを追加
  get 'terms', to: 'home#terms'
  # プライバシーポリシーページのルートを追加
  get 'privacy_policy', to: 'home#privacy_policy'
end