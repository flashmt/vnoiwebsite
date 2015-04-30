require './helper.rb'

class TopicCreate
  @topic_create_form = {
      id_title: 'Chủ đề',
      id_content: 'Nội dung'
  }

  class << self
    attr_reader :topic_create_form
  end
end

module TopicCreateModule
  def create_topic(title = nil, content = nil)
    title = random_string 10 if title.nil?
    content = random_string 50 if content.nil?

    fill_form(TopicCreate.topic_create_form, {id_title: title, id_content: content})
    click_on 'OK'

    return title, content
  end
end
