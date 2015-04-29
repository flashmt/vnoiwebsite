class Breadcrumbs

  # Problems
  @problem_list = 'Danh sách bài tập'
  @problem_submit = 'Nộp bài'
  @problem_status = 'Danh sách bài nộp'
  @problem_rank = 'Xếp hạng'
  @problem_discuss = 'Thảo luận'

  # Forum
  @forum = 'Diễn đàn'
  @forum_cf = 'Codeforces'
  @forum_cf_topic_1 = 'CF Round 294'
  @forum_create_topic = 'Tạo chủ đề mới'

  # Library
  @library = 'Thư viện'
  @library_ds = 'Cấu trúc dữ liệu'
  @library_create_topic = 'Tạo chủ đề mới'
  @library_persistent_ds = 'Persistent Data Structures'

  class << self
    attr_reader :problem_list, :problem_status, :problem_rank, :problem_submit, :problem_discuss,
                :forum, :forum_cf, :forum_cf_topic_1, :forum_create_topic,
                :library, :library_ds, :library_create_topic, :library_persistent_ds
  end
end

module BreadcrumbsModule

  def verify_breadcrumbs_texts(texts)
    within '#breadcrumbs' do
      texts.each do |text|
        puts "Checking breadcrumbs: #{text}"
        expect(page).to have_content(text)
      end
    end
  end

  def verify_breadcrumbs_hidden
    puts 'Breadcrumbs should not be displayed'

    # There are 2 cases here:
    # - Breadcrumbs is not printed (the view is good and sent the hide_breadcrumbs var
    #   to template)
    # - Breadcrumbs is printed and then hidden using CSS, using the default value of
    #   breadcrumbs, which adds CSS to hide itself
    element = first('#breadcrumbs', maximum: 1)
    unless element.nil?
      expect(element).to_not be_visible
    end
  end

  def verify_breadcrumbs
    puts "Verifying breadcrumbs for #{current_path}"
    case current_path

    # Home page
    when %r{^/?$}
      verify_breadcrumbs_hidden

    # Problems
    when %r{^/problems/list/?$}
      verify_breadcrumbs_hidden
    when %r{^/problems/show/([A-Z]+)/?$}
      verify_breadcrumbs_texts [Breadcrumbs.problem_list, $1]
    when %r{^/problems/submit/([A-Z]+)/?$}
      verify_breadcrumbs_texts [Breadcrumbs.problem_list, $1, Breadcrumbs.problem_submit]
    when %r{^/problems/status/([A-Z]+)/?$}
      verify_breadcrumbs_texts [Breadcrumbs.problem_list, $1, Breadcrumbs.problem_status]
    when %r{^/problems/rank/([A-Z]+)/?$}
      verify_breadcrumbs_texts [Breadcrumbs.problem_list, $1, Breadcrumbs.problem_rank]
    when %r{^/problems/discuss/([A-Z]+)/?$}
      verify_breadcrumbs_texts [Breadcrumbs.problem_list, $1, Breadcrumbs.problem_discuss]

    # Forum
    when %r{^/forum/?$}
      verify_breadcrumbs_hidden
    when %r{^/forum/1/?$}
      verify_breadcrumbs_texts [Breadcrumbs.forum, Breadcrumbs.forum_cf]
    when %r{^/forum/1/1/?$}
      verify_breadcrumbs_texts [Breadcrumbs.forum, Breadcrumbs.forum_cf, Breadcrumbs.forum_cf_topic_1]
    when %r{^/forum/1/topic_create/?$}
      verify_breadcrumbs_texts [Breadcrumbs.forum, Breadcrumbs.forum_cf, Breadcrumbs.forum_create_topic]

    # Library
    when %r{^/library/8/?$}
      verify_breadcrumbs_texts [Breadcrumbs.library, Breadcrumbs.library_ds]
    when %r{^/forum/8/topic_create/?$}
      verify_breadcrumbs_texts [Breadcrumbs.library, Breadcrumbs.library_ds, Breadcrumbs.library_create_topic]
    when %r{^/library/8/3/?$}
      verify_breadcrumbs_texts [Breadcrumbs.library, Breadcrumbs.library_ds, Breadcrumbs.library_persistent_ds]

    else
      puts "I don't know about #{current_path}"
      exit 1
    end
  end
end
