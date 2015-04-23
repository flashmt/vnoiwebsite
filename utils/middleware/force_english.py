from django.conf import settings    
from django.utils.translation import activate     
import re


class ForceInEnglish(object):

    def process_request(self, request):
        if re.match(".*admin/", request.path):
            activate("en")
        else:
            activate(settings.LANGUAGE_CODE)
