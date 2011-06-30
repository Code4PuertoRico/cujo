from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from permissions.api import check_permissions

from main.api import diagnostics, tools


def home(request):
    return render_to_response('home.html', {},
    context_instance=RequestContext(request))


def tools_menu(request):
    user_tools = {}
    for namespace, values in tools.items():
        for link in values['links']:
            try:
                permissions = link.get('permissions', [])
                check_permissions(request.user, permissions)
                user_tools[namespace] = {
                    'title': values['title']
                    }
                user_tools[namespace].setdefault('links', [])
                user_tools[namespace]['links'].append(link)
            except PermissionDenied:
                pass

    return render_to_response('tools.html', {
        'blocks': user_tools,
        'title': _(u'tools menu')
    },
    context_instance=RequestContext(request))


def statistics(request):
    blocks = []

    return render_to_response('statistics.html', {
        'blocks': blocks,
        'title': _(u'Statistics')
    },
    context_instance=RequestContext(request))


def diagnostics_view(request):
    return render_to_response('diagnostics.html', {
        'blocks': diagnostics,
        'title': _(u'Diagnostics')
    },
    context_instance=RequestContext(request))
