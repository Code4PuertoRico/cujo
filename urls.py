from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('common.urls')),
    (r'^', include('main.urls')),
    (r'^search/', include('dynamic_search.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^settings/', include('smart_settings.urls')),
    (r'^permissions/', include('permissions.urls')),
    (r'^reminders/', include('reminders.urls')),
    (r'^user_management/', include('user_management.urls')),
    (r'^comments/', include('reminder_comments.urls')),
)

def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))

if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^%s-site_media/(?P<path>.*)$' % settings.PROJECT_NAME,
            'django.views.static.serve',
            {'document_root': 'site_media', 'show_indexes': True}),
    )

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )
