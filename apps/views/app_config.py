from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ViewsConfig(AppConfig):
    name = 'apps.views'
    verbose_name = _('Views')
