# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table('resource_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('owning_dep', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('availability', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Add_information', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('allocation_policy', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('resource', ['Resource'])

        # Adding model 'Booked_resource'
        db.create_table('resource_booked_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Booked_by', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Event_name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('Purpose_of_booking', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('all_day_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('resource_id', self.gf('django.db.models.fields.IntegerField')()),
            ('resource_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('resource_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('resource', ['Booked_resource'])

        # Adding model 'Priority_table'
        db.create_table('resource_priority_table', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Designation', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Priority_num', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('resource', ['Priority_table'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table('resource_resource')

        # Deleting model 'Booked_resource'
        db.delete_table('resource_booked_resource')

        # Deleting model 'Priority_table'
        db.delete_table('resource_priority_table')


    models = {
        'resource.booked_resource': {
            'Booked_by': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Event_name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'Meta': {'object_name': 'Booked_resource'},
            'Purpose_of_booking': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'all_day_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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