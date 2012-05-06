from django.conf.urls.defaults import patterns, url

from reminders.forms import ReminderForm_days, ReminderForm
from reminders.views import (ReminderList, ReminderAdd, ReminderEdit, ReminderExpiredList, ReminderDelete)

urlpatterns = patterns('reminders.views',
    url(r'^list/$', ReminderList.as_view(), (), 'reminder_list'),
    url(r'^list/expired/now/$', ReminderExpiredList.as_view(), (), 'expired_remider_list'),
    url(r'^list/expired/future/$', 'future_expired_remider_list', (), 'future_expired_remider_list'),
    url(r'^add/date/$', ReminderAdd.as_view(form_class=ReminderForm), (), 'reminder_add'),
    url(r'^add/days/$', ReminderAdd.as_view(form_class=ReminderForm_days), (), 'reminder_add_days'),
    url(r'^(?P<pk>\d+)/edit/date/$', ReminderEdit.as_view(form_class=ReminderForm), (), 'reminder_edit'),
    url(r'^(?P<pk>\d+)/edit/days/$', ReminderEdit.as_view(form_class=ReminderForm_days), (), 'reminder_edit_days'),
    url(r'^(?P<pk>\d+)/$', 'reminder_view', (), 'reminder_view'),
    url(r'^(?P<pk>\d+)/delete/$', ReminderDelete.as_view(), (), 'reminder_delete'),
    url(r'^multiple/delete/$', 'reminder_multiple_delete', (), 'reminder_multiple_delete'),

    url(r'^groups/list/$', 'reminder_group_list', (), 'reminder_group_list'),
)
