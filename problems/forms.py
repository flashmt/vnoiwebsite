# -*- coding: utf-8 -*-

from django import forms
from problems.models import SpojProblemLanguage
from voj_interface.const import MAX_PENDING_SUBMISSIONS_EACH_USER, MAX_PENDING_SUBMISSIONS_ALL


class VojSubmitForm(forms.Form):
    code = forms.CharField(
        label=u'Code',
        widget=forms.Textarea,
        required=True
    )
    language = forms.ModelChoiceField(queryset=SpojProblemLanguage.objects.all())

    def clean(self):
        # First, check if user has at most 2 pending submissions
        pending_submissions_user = 0
        if pending_submissions_user > MAX_PENDING_SUBMISSIONS_EACH_USER:
            raise forms.ValidationError(u"Bạn có quá nhiều submission chưa được chấm."
                                        u"Hãy kiểm tra cẩn thận lại code của bạn rồi bình tĩnh submit lại sau")

        # Check if in total, there are at most 80 pending submissions
        # In the first phase, there can be many users who haven't linked account and do not
        # submit through VOJ --> we must set lower value for max. pending submissions
        pending_submissions_all = 0
        if pending_submissions_all > MAX_PENDING_SUBMISSIONS_ALL:
            raise forms.ValidationError(u"Hiện đang có quá nhiều submission chưa được chấm."
                                        u"Nếu submit, bạn sẽ phải chờ rất lâu mới đến lượt mình được chấm."
                                        u"Bạn hãy đọc kĩ lại code hoặc thử sức với bài khác rồi submit lại sau")
        return self.cleaned_data
