from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, register_links
from permissions import role_list, permission_views
from user_management import user_list, group_list, user_management_views

from main.conf.settings import SIDE_BAR_SEARCH

def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table'}
diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill'}
tools_menu = {'text': _(u'tools'), 'view': 'tools_menu', 'famfam': 'wrench'}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'condition': is_superuser}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'condition': is_superuser}


register_top_menu('home', link={'text': _(u'home'), 'view': 'home', 'famfam': 'house'}, position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link={'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}, children_path_regex=[r'^search/'])

register_top_menu('about', link={'text': _(u'about'), 'view': 'about', 'famfam': 'information'}, position=-1)

__version_info__ = {
    'major': 0,
    'minor': 3,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 1
}


def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()
