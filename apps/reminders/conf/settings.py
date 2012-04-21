"""Configuration options for the reminders app"""

from django.utils.translation import ugettext_lazy as _
from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('remiders', _(u'Reminders'), module='remiders.conf.settings')

Setting(
    namespace=namespace,
    name='CHECK_PROCESSING_INTERVAL',
    global_name='REMINDERS_CHECK_PROCESSING_INTERVAL',
    default=60,
    description=_(u'Interval in seconds to wait before checking for expired reminders.')
)
