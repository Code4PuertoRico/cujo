from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('reminder_comments', _(u'Reminder comments'))

PERMISSION_COMMENT_CREATE = Permission.objects.register(namespace, 'comment_create', _(u'Create new comments'))
PERMISSION_COMMENT_DELETE = Permission.objects.register(namespace, 'comment_delete', _(u'Delete comments'))
PERMISSION_COMMENT_EDIT = Permission.objects.register(namespace, 'comment_edit', _(u'Edit comments'))
PERMISSION_COMMENT_VIEW = Permission.objects.register(namespace, 'comment_view', _(u'View comments'))
