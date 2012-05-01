from django.utils.translation import ugettext_lazy as _

PARTICIPANT_ROLE_CREATOR = u'cr'
PARTICIPANT_ROLE_WATCHER = u'wa'
PARTICIPANT_ROLE_EDITOR = u'ed'

PARTICIPANT_ROLE_CHOICES = (
    (PARTICIPANT_ROLE_CREATOR, _(u'Creator')),
    (PARTICIPANT_ROLE_EDITOR, _(u'Editor')),
    (PARTICIPANT_ROLE_WATCHER, _(u'Watcher')),
)

PREEMPTIVE_CHOICES = (
    (u'48h', _(u'2 days')),
    (u'24h', _(u'1 day')),
    (u'12h', _(u'12 hours')),
    (u'6h', _(u'6 hours')),
    (u'2h', _(u'2 hours')),
    (u'1h', _(u'1 hour')),
    (u'30m', _(u'30 minutes')),
    (u'15m', _(u'15 minutes')),
)

REPETITION_CHOICES = (
    (u'24h', _(u'1 day')),
    (u'12h', _(u'12 hours')),
    (u'6h', _(u'6 hours')),
    (u'2h', _(u'2 hours')),
    (u'1h', _(u'1 hour')),
    (u'30m', _(u'30 minutes')),
    (u'15m', _(u'15 minutes')),
)
