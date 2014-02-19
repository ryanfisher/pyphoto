# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.camera_make'
        db.add_column(u'photos_photo', 'camera_make',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True),
                      keep_default=False)

        # Adding field 'Photo.camera_model'
        db.add_column(u'photos_photo', 'camera_model',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)

        # Adding field 'Photo.lens_model'
        db.add_column(u'photos_photo', 'lens_model',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)

        # Adding field 'Photo.f_stop_denominator'
        db.add_column(u'photos_photo', 'f_stop_denominator',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Photo.f_stop_numerator'
        db.add_column(u'photos_photo', 'f_stop_numerator',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Photo.focal_length_denominator'
        db.add_column(u'photos_photo', 'focal_length_denominator',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Photo.focal_length_numerator'
        db.add_column(u'photos_photo', 'focal_length_numerator',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


        # Changing field 'Photo.iso'
        db.alter_column(u'photos_photo', 'iso', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Photo.camera_make'
        db.delete_column(u'photos_photo', 'camera_make')

        # Deleting field 'Photo.camera_model'
        db.delete_column(u'photos_photo', 'camera_model')

        # Deleting field 'Photo.lens_model'
        db.delete_column(u'photos_photo', 'lens_model')

        # Deleting field 'Photo.f_stop_denominator'
        db.delete_column(u'photos_photo', 'f_stop_denominator')

        # Deleting field 'Photo.f_stop_numerator'
        db.delete_column(u'photos_photo', 'f_stop_numerator')

        # Deleting field 'Photo.focal_length_denominator'
        db.delete_column(u'photos_photo', 'focal_length_denominator')

        # Deleting field 'Photo.focal_length_numerator'
        db.delete_column(u'photos_photo', 'focal_length_numerator')


        # Changing field 'Photo.iso'
        db.alter_column(u'photos_photo', 'iso', self.gf('django.db.models.fields.IntegerField')(default=100))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'camera_make': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'camera_model': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'f_stop_denominator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'f_stop_numerator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'focal_length_denominator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'focal_length_numerator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'lens_model': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['photos']