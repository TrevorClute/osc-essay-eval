class UserMailer < ApplicationMailer
  default from: 'no-reply@osc.edu'

  def send_otp(user)
    @user = user
    mail(to: @user.email, subject: 'Your OSC Access Code')
  end
end
