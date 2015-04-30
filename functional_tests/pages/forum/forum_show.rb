class ForumShow
  @create_topic = 'Tạo chủ đề mới'

  class << self
    attr_reader :create_topic
  end
end

module ForumShowModule
end
