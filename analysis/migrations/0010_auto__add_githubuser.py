# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GithubUser'
        db.create_table(u'analysis_githubuser', (
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
        ))
        db.send_create_signal(u'analysis', ['GithubUser'])

        # Adding M2M table for field groups on 'GithubUser'
        m2m_table_name = db.shorten_name(u'analysis_githubuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('githubuser', models.ForeignKey(orm[u'analysis.githubuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['githubuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'GithubUser'
        m2m_table_name = db.shorten_name(u'analysis_githubuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('githubuser', models.ForeignKey(orm[u'analysis.githubuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['githubuser_id', 'permission_id'])


    def backwards(self, orm):
        # Deleting model 'GithubUser'
        db.delete_table(u'analysis_githubuser')

        # Removing M2M table for field groups on 'GithubUser'
        db.delete_table(db.shorten_name(u'analysis_githubuser_groups'))

        # Removing M2M table for field user_permissions on 'GithubUser'
        db.delete_table(db.shorten_name(u'analysis_githubuser_user_permissions'))


    models = {
        u'analysis.branch': {
            'Meta': {'object_name': 'Branch'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Repository']"})
        },
        u'analysis.commit': {
            'Meta': {'object_name': 'Commit'},
            'authored_date': ('django.db.models.fields.BigIntegerField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Branch']"}),
            'commit_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'commit_hash_short': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'commits'", 'symmetrical': 'False', 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Commit']", 'null': 'True'})
        },
        u'analysis.fileanalysis': {
            'Meta': {'object_name': 'FileAnalysis', 'index_together': "[['filename', 'commit']]"},
            'commit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Commit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.githubuser': {
            'Meta': {'object_name': 'GithubUser'},
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
        u'analysis.organization': {
            'Meta': {'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'analysis.pep8analysis': {
            'Meta': {'object_name': 'Pep8Analysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.pyclasscomplexityanalysis': {
            'Meta': {'object_name': 'PyClassComplexityAnalysis'},
            'column': ('django.db.models.fields.IntegerField', [], {}),
            'file_analysis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pyclass_complexity'", 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_end': ('django.db.models.fields.IntegerField', [], {}),
            'line_start': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'real_complexity': ('django.db.models.fields.IntegerField', [], {})
        },
        u'analysis.pyflakesanalysis': {
            'Meta': {'object_name': 'PyFlakesAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.pyfunctioncomplexityanalysis': {
            'Meta': {'object_name': 'PyFunctionComplexityAnalysis'},
            'column': ('django.db.models.fields.IntegerField', [], {}),
            'complexity': ('django.db.models.fields.IntegerField', [], {}),
            'file_analysis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pyfunction_complexity'", 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_end': ('django.db.models.fields.IntegerField', [], {}),
            'line_start': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pyclass': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'methods'", 'null': 'True', 'to': u"orm['analysis.PyClassComplexityAnalysis']"})
        },
        u'analysis.pylintanalysis': {
            'Meta': {'object_name': 'PyLintAnalysis'},
            'column': ('django.db.models.fields.IntegerField', [], {}),
            'file_analysis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pylint_analysis'", 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'msg_id': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'analysis.repository': {
            'Meta': {'object_name': 'Repository'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Organization']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
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
        }
    }

    complete_apps = ['analysis']