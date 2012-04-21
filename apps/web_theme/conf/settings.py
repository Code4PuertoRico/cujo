"""Configuration options for the web_theme app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('web_theme', _(u'Web themes'), module='web_theme.conf.settings')

Setting(
    namespace=namespace,
    name='THEME',
    global_name='WEB_THEME_THEME',
    default=u'default',
    description=_(u'CSS theme to apply, options are: amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse.')
)

Setting(
    namespace=namespace,
    name='ENABLE_SCROLL_JS',
    global_name='WEB_THEME_ENABLE_SCROLL_JS',
    default=True,
    hidden=True
)
