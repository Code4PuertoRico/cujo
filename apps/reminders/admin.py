from __future__ import absolute_import

from django.contrib import admin

from .models import Reminder

admin.site.register(Reminder)
