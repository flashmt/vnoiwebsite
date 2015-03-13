from collections import defaultdict
import json

VOJ_BASE_URL = 'http://vn.spoj.com/'

counter = defaultdict(int)


class GenericModel():
    def __init__(self, model):
        self.fields = {}
        self.model = model
        counter[self.model] += 1
        self.pk = counter[self.model]

    def to_json(self):
        return json.dumps(self.__dict__)


class ProblemCategory(GenericModel):
    def __init__(self, name):
        GenericModel.__init__(self, 'problems.spojproblemcategory')
        self.fields['name'] = name

    def get_url(self):
        return '%sproblems/%s/' % (VOJ_BASE_URL, self.fields['name'])


class Problem(GenericModel):
    def __init__(self, code):
        GenericModel.__init__(self, 'problems.spojproblem')
        self.fields['code'] = code

    def __unicode__(self):
        return self.fields['code']

    def __str__(self):
        return self.fields['code']

    def __repr__(self):
        return self.fields['code']

    def get_url(self):
        return '%sproblems/%s' % (VOJ_BASE_URL, self.fields['code'])