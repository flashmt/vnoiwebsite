require './helper.rb'

class ProblemList
  @header = 'Danh sách bài tập'
  @column_titles = ['Loại bài', 'Mã bài', 'Tên bài', 'Số người giải được', 'Điểm']

  class << self
    attr_reader :header, :column_titles
  end
end

module ProblemListModule
  def verify_problem_list_page
    verify_content ProblemList.header
    verify_content ProblemList.column_titles
  end
end
