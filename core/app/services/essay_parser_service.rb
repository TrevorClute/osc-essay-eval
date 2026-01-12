class EssayParserService
  def self.parse(text_input, file_upload)
    return text_input if text_input.present?

    if file_upload.present?
      ext = File.extname(file_upload.original_filename).downcase

      if ext == ".pdf"
        reader = PDF::Reader.new(file_upload.tempfile.path)
        return reader.pages.map(&:text).join("\n")

      elsif ext == ".txt"
        return file_upload.read
      end
    end

    nil
  end
end
