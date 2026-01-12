class UserMailer < ApplicationMailer
  default from: 'oscessayeval@gmail.com'

  def send_otp(user)
    @user = user
    mail(to: @user.email, subject: 'Your OSC Access Code')
  end
end
