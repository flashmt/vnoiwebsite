# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


def verify_voj_account(username, password):
    url = 'http://vn.spoj.com'
    data = {
        'login_user': username,
        'password': password,
        'autologin': '1',
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        return {
            'success': False,
            'message': 'Không kết nối được với server VOJ. Xin vui lòng thử lại sau',
        }
    else:
        header_text = BeautifulSoup(response.text).find('div', attrs={'class': 'menucmd'}).text
        if username in header_text:
            return {
                'success': True,
                'message': '',
            }
        else:
            return {
                'success': False,
                'message': 'Tài khoản hoặc mật khẩu không đúng',
            }

if __name__ == "__main__":
    print verify_voj_account('mrtrung', 'test123')
