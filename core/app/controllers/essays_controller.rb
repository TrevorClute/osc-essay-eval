class EssaysController < ApplicationController
  # before_action :authenticate_user! # Forces Login

  def new
    # Renders the input form
  end

  def create
    prompt = params[:prompt]
    
    begin
      clean_text = EssayParserService.parse(params[:essay_text], params[:essay_file])

      if clean_text.blank?
        flash[:alert] = "Please provide text or upload a PDF."
        return render :new, status: :unprocessable_entity
      end

      @result = FlaskEvaluateService.evaluate(clean_text, prompt)

      render :show

    rescue StandardError => e
      flash[:alert] = "Error: #{e.message}"
      render :new, status: :unprocessable_entity
    end
  end
end
