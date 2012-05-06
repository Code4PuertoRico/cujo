# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Participant', fields ['reminder', 'user', 'role']
        db.delete_unique('reminders_participant', ['reminder_id', 'user_id', 'role'])

        # Deleting model 'Participant'
        db.delete_table('reminders_participant')

        # Deleting field 'Notification.participant'
        db.delete_column('reminders_notification', 'participant_id')

    def backwards(self, orm):
        # Adding model 'Participant'
        db.create_table('reminders_participant', (
            ('reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reminders.Reminder'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('reminders', ['Participant'])

        # Adding unique constraint on 'Participant', fields ['reminder', 'user', 'role']
        db.create_unique('reminders_participant', ['reminder_id', 'user_id', 'role'])


        # User chose to not deal with backwards NULL issues for 'Notification.participant'
        raise RuntimeError("Cannot reverse this migration. 'Notification.participant' and its values cannot be restored.")
    models = {
        'reminders.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'reminders.groupmember': {
            'Meta': {'object_name': 'GroupMember'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reminders.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reminders.Reminder']"})
        },
        'reminders.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preemptive': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reminders.Reminder']"})
        },
        'reminders.reminder': {
            'Meta': {'ordering': "('-datetime_created',)", 'object_name': 'Reminder'},
            'datetime_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 6, 0, 0)', 'blank': 'True'}),
            'datetime_expire': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['reminders']