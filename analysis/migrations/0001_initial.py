# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'analysis_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['Organization'])

        # Adding model 'Repository'
        db.create_table(u'analysis_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Organization'])),
            ('last_analyzed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['Repository'])

        # Adding model 'Branch'
        db.create_table(u'analysis_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Repository'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['Branch'])

        # Adding model 'Commit'
        db.create_table(u'analysis_commit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Branch'])),
            ('commit_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('authored_date', self.gf('django.db.models.fields.BigIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['Commit'])

        # Adding model 'FileAnalysis'
        db.create_table(u'analysis_fileanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('commit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Commit'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['FileAnalysis'])

        # Adding model 'PyLintAnalysis'
        db.create_table(u'analysis_pylintanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'analysis', ['PyLintAnalysis'])

        # Adding model 'PyFlakesAnalysis'
        db.create_table(u'analysis_pyflakesanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'analysis', ['PyFlakesAnalysis'])

        # Adding model 'Pep8Analysis'
        db.create_table(u'analysis_pep8analysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'analysis', ['Pep8Analysis'])

        # Adding model 'ClassAnalysis'
        db.create_table(u'analysis_classanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'analysis', ['ClassAnalysis'])

        # Adding model 'FunctionAnalysis'
        db.create_table(u'analysis_functionanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'analysis', ['FunctionAnalysis'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table(u'analysis_organization')

        # Deleting model 'Repository'
        db.delete_table(u'analysis_repository')

        # Deleting model 'Branch'
        db.delete_table(u'analysis_branch')

        # Deleting model 'Commit'
        db.delete_table(u'analysis_commit')

        # Deleting model 'FileAnalysis'
        db.delete_table(u'analysis_fileanalysis')

        # Deleting model 'PyLintAnalysis'
        db.delete_table(u'analysis_pylintanalysis')

        # Deleting model 'PyFlakesAnalysis'
        db.delete_table(u'analysis_pyflakesanalysis')

        # Deleting model 'Pep8Analysis'
        db.delete_table(u'analysis_pep8analysis')

        # Deleting model 'ClassAnalysis'
        db.delete_table(u'analysis_classanalysis')

        # Deleting model 'FunctionAnalysis'
        db.delete_table(u'analysis_functionanalysis')


    models = {
        u'analysis.branch': {
            'Meta': {'object_name': 'Branch'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Repository']"})
        },
        u'analysis.classanalysis': {
            'Meta': {'object_name': 'ClassAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.commit': {
            'Meta': {'object_name': 'Commit'},
            'authored_date': ('django.db.models.fields.BigIntegerField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Branch']"}),
            'commit_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.fileanalysis': {
            'Meta': {'object_name': 'FileAnalysis'},
            'commit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Commit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.functionanalysis': {
            'Meta': {'object_name': 'FunctionAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'analysis.pyflakesanalysis': {
            'Meta': {'object_name': 'PyFlakesAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.pylintanalysis': {
            'Meta': {'object_name': 'PyLintAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.repository': {
            'Meta': {'object_name': 'Repository'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Organization']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['analysis']