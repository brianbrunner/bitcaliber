# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PyLintAnalysis.message'
        db.add_column(u'analysis_pylintanalysis', 'message',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'PyLintAnalysis.msg_id'
        db.add_column(u'analysis_pylintanalysis', 'msg_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=8),
                      keep_default=False)

        # Adding field 'PyLintAnalysis.file_analysis'
        db.add_column(u'analysis_pylintanalysis', 'file_analysis',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['analysis.FileAnalysis']),
                      keep_default=False)

        # Adding field 'PyLintAnalysis.module'
        db.add_column(u'analysis_pylintanalysis', 'module',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'PyLintAnalysis.method'
        db.add_column(u'analysis_pylintanalysis', 'method',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'PyLintAnalysis.line'
        db.add_column(u'analysis_pylintanalysis', 'line',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PyLintAnalysis.column'
        db.add_column(u'analysis_pylintanalysis', 'column',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PyLintAnalysis.message'
        db.delete_column(u'analysis_pylintanalysis', 'message')

        # Deleting field 'PyLintAnalysis.msg_id'
        db.delete_column(u'analysis_pylintanalysis', 'msg_id')

        # Deleting field 'PyLintAnalysis.file_analysis'
        db.delete_column(u'analysis_pylintanalysis', 'file_analysis_id')

        # Deleting field 'PyLintAnalysis.module'
        db.delete_column(u'analysis_pylintanalysis', 'module')

        # Deleting field 'PyLintAnalysis.method'
        db.delete_column(u'analysis_pylintanalysis', 'method')

        # Deleting field 'PyLintAnalysis.line'
        db.delete_column(u'analysis_pylintanalysis', 'line')

        # Deleting field 'PyLintAnalysis.column'
        db.delete_column(u'analysis_pylintanalysis', 'column')


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
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'commits'", 'symmetrical': 'False', 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Commit']", 'null': 'True'})
        },
        u'analysis.fileanalysis': {
            'Meta': {'object_name': 'FileAnalysis'},
            'commit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Commit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'column': ('django.db.models.fields.IntegerField', [], {}),
            'file_analysis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.FileAnalysis']"}),
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
        }
    }

    complete_apps = ['analysis']