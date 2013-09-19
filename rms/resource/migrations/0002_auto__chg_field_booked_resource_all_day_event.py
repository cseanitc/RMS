# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Booked_resource.all_day_event'
        db.alter_column('resource_booked_resource', 'all_day_event', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'Booked_resource.all_day_event'
        db.alter_column('resource_booked_resource', 'all_day_event', self.gf('django.db.models.fields.BooleanField')())

    models = {
        'resource.booked_resource': {
            'Booked_by': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Event_name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'Meta': {'object_name': 'Booked_resource'},
            'Purpose_of_booking': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'all_day_event': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_id': ('django.db.models.fields.IntegerField', [], {}),
            'resource_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resource_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        'resource.priority_table': {
            'Designation': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Meta': {'object_name': 'Priority_table'},
            'Priority_num': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'resource.resource': {
            'Add_information': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'Meta': {'object_name': 'Resource'},
            'allocation_policy': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owning_dep': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['resource']