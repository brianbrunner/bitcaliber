# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ComplexityAnalysis'
        db.delete_table(u'analysis_complexityanalysis')

        # Adding model 'PyFunctionComplexityAnalysis'
        db.create_table(u'analysis_pyfunctioncomplexityanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pyclass', self.gf('django.db.models.fields.related.ForeignKey')(related_name='methods', null=True, to=orm['analysis.PyClassComplexityAnalysis'])),
            ('file_analysis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pyfunction_complexity', to=orm['analysis.FileAnalysis'])),
            ('complexity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'analysis', ['PyFunctionComplexityAnalysis'])

        # Adding model 'PyClassComplexityAnalysis'
        db.create_table(u'analysis_pyclasscomplexityanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_analysis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pyclass_complexity', to=orm['analysis.FileAnalysis'])),
            ('real_complexity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'analysis', ['PyClassComplexityAnalysis'])


    def backwards(self, orm):
        # Adding model 'ComplexityAnalysis'
        db.create_table(u'analysis_complexityanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'analysis', ['ComplexityAnalysis'])

        # Deleting model 'PyFunctionComplexityAnalysis'
        db.delete_table(u'analysis_pyfunctioncomplexityanalysis')

        # Deleting model 'PyClassComplexityAnalysis'
        db.delete_table(u'analysis_pyclasscomplexityanalysis')


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
            'file_analysis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pyclass_complexity'", 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'real_complexity': ('django.db.models.fields.IntegerField', [], {})
        },
        u'analysis.pyflakesanalysis': {
            'Meta': {'object_name': 'PyFlakesAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'analysis.pyfunctioncomplexityanalysis': {
            'Meta': {'object_name': 'PyFunctionComplexityAnalysis'},
            'complexity': ('django.db.models.fields.IntegerField', [], {}),
            'file_analysis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pyfunction_complexity'", 'to': u"orm['analysis.FileAnalysis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        }
    }

    complete_apps = ['analysis']