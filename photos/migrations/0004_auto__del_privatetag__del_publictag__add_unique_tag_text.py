# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PrivateTag'
        db.delete_table(u'photos_privatetag')

        # Deleting model 'PublicTag'
        db.delete_table(u'photos_publictag')

        # Adding M2M table for field public_tags on 'Photo'
        m2m_table_name = db.shorten_name(u'photos_photo_public_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm[u'photos.photo'], null=False)),
            ('tag', models.ForeignKey(orm[u'photos.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photo_id', 'tag_id'])

        # Adding M2M table for field private_tags on 'Photo'
        m2m_table_name = db.shorten_name(u'photos_photo_private_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm[u'photos.photo'], null=False)),
            ('tag', models.ForeignKey(orm[u'photos.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photo_id', 'tag_id'])

        # Adding unique constraint on 'Tag', fields ['text']
        db.create_unique(u'photos_tag', ['text'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['text']
        db.delete_unique(u'photos_tag', ['text'])

        # Adding model 'PrivateTag'
        db.create_table(u'photos_privatetag', (
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Photo'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Tag'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'photos', ['PrivateTag'])

        # Adding model 'PublicTag'
        db.create_table(u'photos_publictag', (
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Photo'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Tag'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'photos', ['PublicTag'])

        # Removing M2M table for field public_tags on 'Photo'
        db.delete_table(db.shorten_name(u'photos_photo_public_tags'))

        # Removing M2M table for field private_tags on 'Photo'
        db.delete_table(db.shorten_name(u'photos_photo_private_tags'))


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
            'private_tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'private_tags'", 'symmetrical': 'False', 'to': u"orm['photos.Tag']"}),
            'public_tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'public_tags'", 'symmetrical': 'False', 'to': u"orm['photos.Tag']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'thumbnail_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.User']"}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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