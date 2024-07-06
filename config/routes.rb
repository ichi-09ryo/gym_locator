Rails.application.routes.draw do
  get 'pages/about'
  get 'pages/gym_activity'
  get 'pages/magazine'
  devise_for :users, controllers: {
    omniauth_callbacks: 'users/omniauth_callbacks'
  }

  resources :users, only: [:show]
  root 'home#index'
  get 'equipments', to: 'equipments#index'
  get 'map', to: 'map#index'
  get 'search', to: 'gyms#search'
  get 'about', to: 'pages#about', as: 'about'
  get 'gym_activity', to: 'pages#gym_activity', as: 'gym_activity'
  get 'magazine', to: 'pages#magazine', as: 'magazine'

  resources :map, only: [:index]
  # 利用規約ページのルートを追加
  get 'terms', to: 'home#terms'
  # プライバシーポリシーページのルートを追加
  get 'privacy_policy', to: 'home#privacy_policy'
end