class Users::OmniauthCallbacksController < Devise::OmniauthCallbacksController
  def twitter
    handle_auth "Twitter"
  end

  def line
    handle_auth "LINE"
  end

  def instagram
    handle_auth "Instagram"
  end

  def handle_auth(kind)
    @user = User.from_omniauth(request.env['omniauth.auth'])

    if @user.persisted?
      if kind == "LINE"
        @user.update(profile_image_url: request.env["omniauth.auth"].info.image) # プロフィール画像のURLを更新
      end
      flash[:notice] = I18n.t 'devise.omniauth_callbacks.success', kind: kind
      sign_in_and_redirect @user, event: :authentication
    else
      session['devise.omniauth_data'] = request.env['omniauth.auth'].except(:extra)
      redirect_to new_user_registration_url, alert: @user.errors.full_messages.join("\n")
    end
  end
end