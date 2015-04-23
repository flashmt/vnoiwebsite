from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class HumanizeConfig(AppConfig):
    name = 'utils.humanize'
    verbose_name = _("Humanize")
