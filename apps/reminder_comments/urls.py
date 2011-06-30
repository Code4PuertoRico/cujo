from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('reminder_comments.views',
    url(r'^(?P<comment_id>\d+)/delete/$', 'comment_delete', (), 'comment_delete'),
    url(r'^multiple/delete/$', 'comment_multiple_delete', (), 'comment_multiple_delete'),
    url(r'^add_to_reminder/(?P<reminder_id>\d+)/$', 'comment_add', (), 'comment_add'),
)
