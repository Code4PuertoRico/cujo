from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('reminders', _(u'Reminders'))

PERMISSION_REMINDER_VIEW = Permission.objects.register(namespace, 'reminder_view', _(u'View reminder'))
PERMISSION_REMINDER_CREATE = Permission.objects.register(namespace, 'reminder_create', _(u'Create reminder'))
PERMISSION_REMINDER_EDIT = Permission.objects.register(namespace, 'reminder_edit', _(u'Edit reminder'))
PERMISSION_REMINDER_DELETE = Permission.objects.register(namespace, 'reminder_delete', _(u'Delete reminder'))
