import json
import logging
logging.basicConfig(level=logging.DEBUG)
import os
import shutil
from urllib import quote

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

import radon.complexity
from git import Repo

from analysis.tasks import analyze_repo
from analysis.models import Repository, Commit
from analyzer import Analyzer

from bitcaliber.celery import app

def index(request):
    print request.user
    return render_to_response('analysis/index.html')

def signout(request):
    logout(request)
    return redirect("index")
    
# API Methods

@login_required
def github_repos(request):

    repos = request.user.get_repositories()

    return HttpResponse(json.dumps({
      "repos": [{
        "name": repo.full_name,
        "id": repo.id
      } for repo in repos]
    }), content_type="application/json")

@login_required
def add_github_repository(request, owner, name):

    if request.method == 'POST':

        url = "https://github.com/%s/%s" % (owner, name)
        print url

        repo_info = request.user.setup_repo(owner, name)
        
        print repo_info

        # repo = Repository(url=url, organization=request.user.organization)
        # repo.save()

        return HttpResponse(json.dumps({
          "url": url,
          "owner": owner,
          "name": name
        }), content_type="application/json")

    else:

        return HttpResponse(json.dumps({
          "error": "This method only accepts post requests"
        }), content_type="application/json", status=405)

@login_required
def repos(request):

    print request.user.organizations.all()

    repos = Repository.objects.filter(organization__in=request.user.organizations.all())

    print repos.count()

    return HttpResponse(json.dumps({
      "repos": [repo.dict() for repo in repos]
    }), content_type="application/json")

@login_required
def analyze_repository(request, repo_id):

    repo = Repository.objects.get(id=repo_id, organization__in=user.organizations)

    res = analyze_repo.delay(repo)

    return HttpResponse(json.dumps({
      "analysis_id": res.id
    }), content_type="application/json")

@login_required
def get_analysis_status(request, analysis_id):

    res = app.AsyncResult(analysis_id, timeout)
    analysis_res = res.get(timeout=5)
    
    return HttpResponse(json.dumps({
      "complete": True
    }), content_type="application/json")

@login_required
def commit_analysis(request, repo_id, commit):

    repo = Repository.objects.get(id=repo_id, organization__in=request.user.organizations)

    if commit == "latest":
      commit = repo.latest_commit()
    elif len(commit) == 7:
      commit = Commit.objects.get(commit_hash_short=commit, branch__repository=repo)
    else:
      commit = Commit.objects.get(commit_hash=commit, branch__repository=self)

    return HttpResponse(json.dumps({
        "commit": commit.commit_hash,
        "branch": commit.branch.name,
        "file_stats": [file.dict(stats=('pylint','pycomplexity')) for file in commit.files.all()]
    }), content_type="application/json")

@login_required
def file_analysis(request, commit, filename):

    if len(commit) == 7:
      commit = Commit.objects.get(commit_hash_short=commit)
    else:
      commit = Commit.objects.get(commit_hash=commit)
    file_obj = commit.files.get(filename=filename)

    return HttpResponse(json.dumps({
        "raw_contents": file_obj.get_file_contents(),
        "pylint_analysis": [analysis.dict() for analysis in file_obj.pylint_analysis.all()]
    }), content_type="application/json")
