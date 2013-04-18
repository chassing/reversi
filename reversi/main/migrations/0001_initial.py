# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReversiUser'
        db.create_table(u'main_reversiuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'main', ['ReversiUser'])

        # Adding M2M table for field groups on 'ReversiUser'
        db.create_table(u'main_reversiuser_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reversiuser', models.ForeignKey(orm[u'main.reversiuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'main_reversiuser_groups', ['reversiuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'ReversiUser'
        db.create_table(u'main_reversiuser_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reversiuser', models.ForeignKey(orm[u'main.reversiuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'main_reversiuser_user_permissions', ['reversiuser_id', 'permission_id'])

        # Adding model 'TileColor'
        db.create_table(u'main_tilecolor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'main', ['TileColor'])

        # Adding model 'Game'
        db.create_table(u'main_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=8)),
        ))
        db.send_create_signal(u'main', ['Game'])

        # Adding model 'Player'
        db.create_table(u'main_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ReversiUser'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', to=orm['main.Game'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TileColor'])),
        ))
        db.send_create_signal(u'main', ['Player'])

        # Adding model 'Move'
        db.create_table(u'main_move', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.TextField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='moves', to=orm['main.Player'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Game'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Move'])

        # Adding model 'Socket'
        db.create_table(u'main_socket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sockets', to=orm['main.Player'])),
        ))
        db.send_create_signal(u'main', ['Socket'])


    def backwards(self, orm):
        # Deleting model 'ReversiUser'
        db.delete_table(u'main_reversiuser')

        # Removing M2M table for field groups on 'ReversiUser'
        db.delete_table('main_reversiuser_groups')

        # Removing M2M table for field user_permissions on 'ReversiUser'
        db.delete_table('main_reversiuser_user_permissions')

        # Deleting model 'TileColor'
        db.delete_table(u'main_tilecolor')

        # Deleting model 'Game'
        db.delete_table(u'main_game')

        # Deleting model 'Player'
        db.delete_table(u'main_player')

        # Deleting model 'Move'
        db.delete_table(u'main_move')

        # Deleting model 'Socket'
        db.delete_table(u'main_socket')


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
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moves'", 'to': u"orm['main.Player']"})
        },
        u'main.player': {
            'Meta': {'object_name': 'Player'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TileColor']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': u"orm['main.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'main.socket': {
            'Meta': {'object_name': 'Socket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sockets'", 'to': u"orm['main.Player']"}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'main.tilecolor': {
            'Meta': {'object_name': 'TileColor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['main']