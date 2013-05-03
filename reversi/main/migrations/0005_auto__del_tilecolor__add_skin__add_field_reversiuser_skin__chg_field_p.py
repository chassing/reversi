# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TileColor'
        try:
            db.delete_table(u'main_tilecolor')
        except:
            pass

        # Adding model 'Skin'
        db.create_table(u'main_skin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('player1', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('player2', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'main', ['Skin'])

        # Adding field 'ReversiUser.skin'
        db.add_column(u'main_reversiuser', 'skin',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Skin'], null=True, blank=True),
                      keep_default=False)


        # Renaming column for 'Player.color' to match new field type.
        db.rename_column(u'main_player', 'color_id', 'color')
        # Changing field 'Player.color'
        db.alter_column(u'main_player', 'color', self.gf('django.db.models.fields.CharField')(max_length=5))
        # Removing index on 'Player', fields ['color']
        try:
            db.delete_index(u'main_player', ['color_id'])
        except:
            pass


    def backwards(self, orm):
        # Adding index on 'Player', fields ['color']
        db.create_index(u'main_player', ['color_id'])

        # Adding model 'TileColor'
        db.create_table(u'main_tilecolor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'main', ['TileColor'])

        # Deleting model 'Skin'
        db.delete_table(u'main_skin')

        # Deleting field 'ReversiUser.skin'
        db.delete_column(u'main_reversiuser', 'skin_id')


        # Renaming column for 'Player.color' to match new field type.
        db.rename_column(u'main_player', 'color', 'color_id')
        # Changing field 'Player.color'
        db.alter_column(u'main_player', 'color_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TileColor']))

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '8'})
        },
        u'main.move': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Move'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.TextField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moves'", 'to': u"orm['main.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moves'", 'null': 'True', 'to': u"orm['main.Player']"})
        },
        u'main.player': {
            'Meta': {'object_name': 'Player'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': u"orm['main.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'surrendered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ReversiUser']"})
        },
        u'main.reversiuser': {
            'Meta': {'object_name': 'ReversiUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Skin']", 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'main.skin': {
            'Meta': {'object_name': 'Skin'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'player1': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'player2': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'main.socket': {
            'Meta': {'object_name': 'Socket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sockets'", 'to': u"orm['main.Player']"}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['main']
