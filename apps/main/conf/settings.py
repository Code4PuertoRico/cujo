"""Configuration options for the main app"""

from django.utils.translation import ugettext_lazy as _
from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('main', _(u'Main'), module='main.conf.settings')

Setting(
    namespace=namespace,
    name='SIDE_BAR_SEARCH',
    global_name='MAIN_SIDE_BAR_SEARCH',
    default=False,
    description=_(u'Controls whether the search functionality is provided by a sidebar widget or by a menu entry.')
)
