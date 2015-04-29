class Header
  @home = 'Trang chủ'
  @problems = 'Đề bài'
  @contests = 'Kỳ thi'
  @forum = 'Diễn đàn'
  @library = 'Thư viện'

  @login = 'Đăng nhập'
  @logout = 'Đăng xuất'
  @register = 'Đăng ký'
  @login_form = {
      username: 'Tài khoản',
      password: 'Mật khẩu',
  }

  class << self
    attr_reader :home, :problems, :contests, :forum, :library,
                :login, :logout, :register, :login_form
  end
end

module HeaderModule
end
