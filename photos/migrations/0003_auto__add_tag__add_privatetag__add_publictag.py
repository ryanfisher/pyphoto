# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'photos_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'photos', ['Tag'])

        # Adding model 'PrivateTag'
        db.create_table(u'photos_privatetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Photo'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Tag'])),
        ))
        db.send_create_signal(u'photos', ['PrivateTag'])

        # Adding model 'PublicTag'
        db.create_table(u'photos_publictag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Photo'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Tag'])),
        ))
        db.send_create_signal(u'photos', ['PublicTag'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'photos_tag')

        # Deleting model 'PrivateTag'
        db.delete_table(u'photos_privatetag')

        # Deleting model 'PublicTag'
        db.delete_table(u'photos_publictag')


    models = {
        u'photos.album': {
            'Meta': {'object_name': 'Album'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['photos.Photo']", 'through': u"orm['photos.SortedPhoto']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.User']"})
        },
        u'photos.photo': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Photo'},
            'camera_make': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'camera_model': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'exposure_denominator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'exposure_numerator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'f_stop_denominator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'f_stop_numerator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'focal_length_denominator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'focal_length_numerator': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lens_model': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'optimized_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'optimized_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'private_tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'private_tags'", 'symmetrical': 'False', 'through': u"orm['photos.PrivateTag']", 'to': u"orm['photos.Tag']"}),
            'public_tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'public_tags'", 'symmetrical': 'False', 'through': u"orm['photos.PublicTag']", 'to': u"orm['photos.Tag']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'thumbnail_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.User']"}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'photos.privatetag': {
            'Meta': {'object_name': 'PrivateTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Photo']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Tag']"})
        },
        u'photos.publictag': {
            'Meta': {'object_name': 'PublicTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Photo']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Tag']"})
        },
        u'photos.sortedphoto': {
            'Meta': {'ordering': "('position',)", 'object_name': 'SortedPhoto'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Album']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Photo']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'photos.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'profiles.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['photos']