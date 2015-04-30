require './helper.rb'

class ForumList
  @forum_groups = {
      contest: {
          title: 'Các kì thi online',
          forums: {
              vnoi: 'Các kỳ thi của VNOI',
              cf: 'Codeforces',
              tc: 'Topcoder',
              other: 'Các kỳ thi khác',
          }
      },
      oj: {
          title: 'Online Judge',
          forums: {
              voj: 'VOJ, SPOJ',
              other: 'Các OJ khác',
          }
      },
      voi: {
          title: 'Thi Quốc gia, Quốc tế',
          forums: {
              voi: 'Thi HSG Quốc gia',
              ioi: 'IOI, APIO',
              acm: 'ACM',
              other: 'Các kỳ thi khác',
          }
      },
      discuss: {
          title: 'Thảo luận chung',
          forums: {
              algo: 'Thuật toán',
              ml: 'Machine Learning',
          }
      },
      talk: {
          title: 'Trò chuyện',
          forums: {
          }
      },
  }

  class << self
    attr_reader :forum_groups
  end
end

module ForumListModule
  def verify_forum_list_page
    ForumList.forum_groups.each do |_, forum_group|
      within '#body-container' do
        verify_content forum_group[:title]
        verify_content forum_group[:forums]
      end
    end
  end
end
