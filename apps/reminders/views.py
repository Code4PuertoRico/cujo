from __future__ import absolute_import

import datetime

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import formats
from django.contrib.auth.models import User

from common.utils import encapsulate
from common.views import (ListView, CreateView, UpdateView, DeleteView)
from permissions.models import Permission
from acls.models import AccessEntry

from .forms import (ReminderForm, ReminderForm_view,
    ReminderForm_days, FutureDateForm)
from .models import Reminder, Group
from .permissions import (PERMISSION_REMINDER_VIEW, PERMISSION_REMINDER_CREATE,
    PERMISSION_REMINDER_EDIT, PERMISSION_REMINDER_DELETE)


class ReminderList(ListView):
    required_permissions = [PERMISSION_REMINDER_VIEW]
   
    def get_queryset(self):
        return Reminder.objects.all()

    def special_context(self):
        return {
            'title': _(u'reminders'),
            'multi_select_as_buttons': True,
            'hide_links': True
        }


class ReminderExpiredList(ReminderList):
    required_permissions = [PERMISSION_REMINDER_VIEW]
   
    def get_queryset(self):
        self.expiration_date=self.kwargs.get('expiration_date', datetime.datetime.now().date())
        return Reminder.objects.filter(datetime_expire__lt=self.expiration_date).order_by('datetime_expire')

    def special_context(self):
        return {
            'title': _(u'expired reminders to the date: %(date)s') % {
                'date': formats.date_format(self.expiration_date, u'DATE_FORMAT'),
                },
            'multi_select_as_buttons': True,
            'hide_links': True,
            'extra_columns': [
                {
                    'name': _('days expired'),
                    'attribute': encapsulate(lambda x: (self.expiration_date - x.datetime_expire).days)
                }
            ]
        }


class ReminderAdd(CreateView):
    required_permissions = [PERMISSION_REMINDER_CREATE]

    def get_success_url(self):
        return reverse('reminder_list')

    def special_context(self):
        return {
            'title': _(u'create reminder (%s)') % (_(u'calendar') if self.form_class == ReminderForm else _(u'days')),
        }

    def form_valid(self, form):
        if self.form_class == ReminderForm_days:
            reminder = form.save(commit=False)
            reminder.datetime_expire = reminder.datetime_created + datetime.timedelta(days=int(form.cleaned_data['days']))
            reminder.save()
        else:
            reminder = form.save()

        messages.success(self.request, _(u'Reminder "%s" created successfully.') % reminder)
                    
        return super(ReminderAdd, self).form_valid(form)


class ReminderEdit(UpdateView):
    required_permissions = [PERMISSION_REMINDER_EDIT]
    model = Reminder

    def get_success_url(self):
        return reverse('reminder_list')

    def special_context(self):
        expired = (datetime.datetime.now().date() - reminder.datetime_expire).days
        expired_template = _(u'(expired %s days)') % expired
        return {
            'title': _(u'Edit reminder "%(reminder)s" %(expired)s') % {
                'reminder': reminder, 'expired': expired_template if expired > 0 else u''
            },
            'object': reminder,                
        }

    def form_valid(self, form):
        if self.form_class == ReminderForm_days:
            reminder = form.save(commit=False)
            reminder.datetime_expire = reminder.datetime_created + datetime.timedelta(days=int(form.cleaned_data['days']))
            reminder.save()
        else:
            reminder = form.save()
        messages.success(self.request, _(u'Reminder "%s" edited successfully.') % reminder)
                    
        return super(ReminderEdit, self).form_valid(form)
        

class ReminderDelete(DeleteView):
    required_permissions = [PERMISSION_REMINDER_DELETE]
    model = Reminder

    def get_success_url(self):
        return reverse('reminder_list')
        
    def special_context(self):
        context = {
            'object_name': _(u'reminder'),
            'delete_view': True,
            'previous': self.request.POST.get('previous', self.request.GET.get('previous', self.request.META.get('HTTP_REFERER', reverse('reminder_list')))),
            'form_icon': u'hourglass_delete.png',
        }
        #if len(reminders) == 1:
        #    context['object'] = reminders[0]
        context['object'] = self.object
        context['title'] = _(u'Are you sure you wish to delete the reminder "%s"?') % self.object
        #elif len(reminders) > 1:
        #    context['title'] = _(u'Are you sure you wish to delete the reminders: %s?') % ', '.join([unicode(d) for d in reminders])        
        return context

    def delete(self, request, *args, **kwargs):
        try:
            response = super(ReminderDelete, self).delete(request, *args, **kwargs)
        except Exception, e:
            messages.error(request, _(u'Error deleting reminder "%(reminder)s"; %(error)s') % {
                'reminder': self.object, 'error': e
            })
        else:
            messages.success(request, _(u'Reminder "%s" deleted successfully.') % self.object)
            
        return response

"""
def reminder_delete(request, reminder_id=None, reminder_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_DELETE])
    post_action_redirect = None

    if reminder_id:
        try:
            #Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_DELETE_ALL])
            reminders = [get_object_or_404(Reminder, pk=reminder_id)]
        except PermissionDenied:
            Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_DELETE])
            try:
                reminders = [get_object_or_404(Reminder, pk=self.kwargs['reminder_id'])]
            except Http404:
                raise PermissionDenied

        post_action_redirect = reverse('reminder_list')
    elif reminder_id_list:
        # TODO: Improve to display PermissionDenied instead of 404 on unauthorized id's
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_DELETE_ALL])
            reminders = [get_object_or_404(Reminder, pk=reminder_id) for reminder_id in reminder_id_list.split(',')]
        except PermissionDenied:
            Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_DELETE])
            reminders = [get_object_or_404(Reminder, pk=reminder_id) for reminder_id in reminder_id_list.split(u',')]
    else:
        messages.error(request, _(u'Must provide at least one reminder.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', u'/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for reminder in reminders:
            try:
                reminder.delete()
                messages.success(request, _(u'Reminder "%s" deleted successfully.') % reminder)
            except Exception, e:
                messages.error(request, _(u'Error deleting reminder "%(reminder)s"; %(error)s') % {
                    'reminder': reminder, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'reminder'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'hourglass_delete.png',
    }
    if len(reminders) == 1:
        context['object'] = reminders[0]
        context['title'] = _(u'Are you sure you wish to delete the reminder "%s"?') % ', '.join([unicode(d) for d in reminders])
    elif len(reminders) > 1:
        context['title'] = _(u'Are you sure you wish to delete the reminders: %s?') % ', '.join([unicode(d) for d in reminders])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
"""
def reminder_multiple_delete(request):
    return reminder_delete(
        request, reminder_id_list=request.GET.get('id_list', [])
    )


def reminder_view(request, pk):
    try:
        #Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_VIEW_ALL])
        reminder = get_object_or_404(Reminder, pk=pk)
    except PermissionDenied:
        Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_VIEW])
        try:
            reminder = get_object_or_404(Reminder, pk=pk)
        except Http404:
            raise PermissionDenied

    expired = (datetime.datetime.now().date() - reminder.datetime_expire).days
    expired_template = _(u' (expired %s days)') % expired

    form = ReminderForm_view(instance=reminder, extra_fields=[
        {'label': _(u'Days'), 'field': lambda x: (x.datetime_expire - x.datetime_created).days},
    ])

    subtemplates_list = [
        {
            'name': 'generic_detail_subtemplate.html',
            'context': {
            'title': _(u'Detail for reminder "%(reminder)s"%(expired)s') % {
                'reminder': reminder, 'expired': expired_template if expired > 0 else u''},
                    'form': form,
            }
        },
    ]

    return render_to_response('generic_detail.html', {
        'subtemplates_list': subtemplates_list,
        'object': reminder,
        'object_name': _(u'reminder'),
        'reminder': reminder
    },
    context_instance=RequestContext(request))


def future_expired_remider_list(request, view_all=False):
    Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_VIEW, PERMISSION_REMINDER_VIEW_ALL])

    #next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', u'/')))

    if request.method == 'POST':
        form = FutureDateForm(request.POST)
        if form.is_valid():
            return expired_remider_list(request, expiration_date=form.cleaned_data['future_date'], view_all=view_all)
    else:
        form = FutureDateForm()

    return render_to_response('generic_form.html', {
        'title': _(u'Future expired reminders'),
        'form': form,
        #'next': next,
    },
    context_instance=RequestContext(request))


def reminder_group_list(request):
    #try:
    #    Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_VIEW_ALL])
    #    reminder = get_object_or_404(Reminder, pk=reminder_id)
    #except PermissionDenied:
    #    Permission.objects.check_permissions(request.user, [PERMISSION_REMINDER_VIEW])
    #    try:
    #        reminder = get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR, PARTICIPANT_ROLE_WATCHER]).distinct(), pk=reminder_id)
    #    except Http404:
    #    raise PermissionDenied

    return render_to_response('generic_list.html', {
        'object_list': Group.objects.all(),
        'title': _(u'groups'),
        #'object': reminder,
        #'object_name': _(u'reminder'),
        #'hide_link': True,
        #'hide_object': True,
    },
    context_instance=RequestContext(request))
