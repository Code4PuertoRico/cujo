"""Configuration options for the dynamic_search app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('dynamic_search', _(u'Search'), module='dynamic_search.conf.settings')

Setting(
    namespace=namespace,
    name='SHOW_OBJECT_TYPE',
    global_name='SEARCH_SHOW_OBJECT_TYPE',
    default=True,
    hidden=True,
)

Setting(
    namespace=namespace,
    name='LIMIT',
    global_name='SEARCH_LIMIT',
    default=100,
    description=_(u'Maximum amount search hits to fetch and display.')
)




