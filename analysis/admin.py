from django.contrib import admin
from models import *

from analysis.tasks import analyze_repo

# Github User

admin.site.register(GithubUser)

# Organization

admin.site.register(Organization)

# Repository Stuff

def analyze_repo_model(modeladmin, request, queryset):
    for repo in queryset:
        print analyze_repo
        res = analyze_repo.delay(repo)
        print "RES ID: %s" % res.id
analyze_repo_model.short_description = "Run analysis on a repository and generate data"

class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['url', 'last_analyzed']
    ordering = ('url',)
    actions = [analyze_repo_model]

admin.site.register(Repository, RepositoryAdmin)

# Branch Stuff

admin.site.register(Branch)

# Author Stuff

admin.site.register(Author)

# Commit Stuff

class CommitAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'authored_date']
    ordering = ('authored_date',)

admin.site.register(Commit, CommitAdmin)

# File Analysis

class FileAnalysisAdmin(admin.ModelAdmin):
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(FileAnalysisAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 file analysis was"
        else:
            message_bit = "%s file analysis were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

admin.site.register(FileAnalysis, FileAnalysisAdmin)

# PyLint Analysis

admin.site.register(PyLintAnalysis)

# PyLint Analysis

admin.site.register(PyFunctionComplexityAnalysis)

