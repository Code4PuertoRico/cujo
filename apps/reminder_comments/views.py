from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from permissions.api import check_permissions
from reminders.models import Reminder

from reminder_comments import PERMISSION_COMMENT_DELETE, PERMISSION_COMMENT_CREATE
from reminder_comments.forms import CommentForm


def comment_delete(request, comment_id=None, comment_id_list=None):
    #check_permissions(request.user, [PERMISSION_COMMENT_DELETE])
    post_action_redirect = None

    if comment_id:
        comments = [get_object_or_404(Comment, pk=comment_id)]
    elif comment_id_list:
        comments = [get_object_or_404(Comment, pk=comment_id) for comment_id in comment_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one comment.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for comment in comments:
            try:
                comment.delete()
                messages.success(request, _(u'Comment "%s" deleted successfully.') % comment)
            except Exception, e:
                messages.error(request, _(u'Error deleting comment "%(comment)s": %(error)s') % {
                    'comment': comment, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'comment'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'comment_delete.png',
    }
    if len(comments) == 1:
        context['object'] = comments[0].content_object
        context['title'] = _(u'Are you sure you wish to delete the comment: %s?') % ', '.join([unicode(d) for d in comments])
    elif len(comments) > 1:
        context['title'] = _(u'Are you sure you wish to delete the comments: %s?') % ', '.join([unicode(d) for d in comments])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def comment_multiple_delete(request):
    return comment_delete(
        request, comment_id_list=request.GET.get('id_list', [])
    )


def comment_add(request, reminder_id):
    #check_permissions(request.user, [PERMISSION_COMMENT_CREATE])

    reminder = get_object_or_404(Reminder, pk=reminder_id)
    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = ContentType.objects.get_for_model(reminder)
            comment.object_pk = reminder.pk
            comment.site = Site.objects.get_current()
            comment.save()

            messages.success(request, _(u'Comment added successfully.'))
            return HttpResponseRedirect(next)
    else:
        form = CommentForm()

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Add comment to reminder: %s') % reminder,
        'next': next,
        'object': reminder,
    }, context_instance=RequestContext(request))
