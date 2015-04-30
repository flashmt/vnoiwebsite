class TopicShow
  @reply = 'Trả lời'
  @edit = 'Chỉnh sửa'
  @delete = 'Xóa'
  @pin = 'Ghim'
  @unpin = 'Bỏ ghim'

  class << self
    attr_reader :reply, :edit, :delete, :pin, :unpin
  end
end

module TopicShowModule
end
