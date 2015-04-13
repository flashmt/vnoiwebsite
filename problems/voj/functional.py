import time
import re
import requests
import html5lib
import dateutil.parser
import copy

from requests_toolbelt import MultipartEncoder

VOJ_BASE_URL = 'http://vn.spoj.com/'
# this url is used to submit problem
VOJ_SUBMIT_URL = "http://vn.spoj.com/submit/complete"


# attempt to login, return cookies if success
def login(login_user, password):
    formdata = {
        "login_user": login_user,
        "password": password,
        "submit": "Send"
    }
    response = requests.post(VOJ_BASE_URL, data=formdata)
    # check if the login box exists
    if "<input name=\"login_user\" type=\"text\" style=\"width: 85px;\" class=\"form\">" in response:
        # fail
        return None
    # success
    return response.headers["set-cookie"]


# submit source code
def submit(problemcode, source, lang, cookies):
    formdata = MultipartEncoder(fields={
        "file": source,
        "lang": lang,
        "subm_file": ("filename", None, "text/plain"),
        "problemcode": problemcode,
        "submit": "Send"
    })
    requests.post(VOJ_SUBMIT_URL, data=formdata, cookies=cookies, headers={"Content-Type": formdata.content_type})
