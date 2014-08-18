import datetime
from threading import Thread

from boto.s3.connection import S3Connection
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Count, Min, Sum, Avg
from jsonfield import JSONField
from github3 import login as gh_login

from analyzer import Analyzer

# User Model

class GithubUserManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        email = email['email']
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

class GithubUser(AbstractUser):

    objects = GithubUserManager()

    @property
    def gh_session(self):
        return gh_login(token=self.social_auth.all()[0].extra_data['access_token'])

    def get_repositories(self, languages=None):

        if not languages:
            languages = set(["Python"])

        all_repos = []
        for team in self.gh_session.iter_user_teams():
            for repo in team.iter_repos():
                all_repos.append(repo)

        for team in self.gh_session.iter_repos():
            all_repos.append(repo)

        repos = []
        for repo in all_repos: 
            for language in repo.iter_languages():
                if language[0] == 'Python':
                    repos.append(repo)

        return repos

    KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDzrF1SemnjLnve7qrWVIShh5npjFHSOIufHH4S/OQglbwXYOwc+/qiSx1lyDHD9wkoXJektB3KIa073AlB6BZEkP5/idfxSJu5rmUxZUtGE8cuFIBOe4K3d7FCJGnJJboQltFkxWSZmRcXKifYek/bRjP2mao496rd2a6htaZX5xyWPiqwiFFl1OB6OFP68c+Ty4OYpMRhy26D1Ju0tZIGgVnrH4ON310JJ95pvt6n6prVCR+/O3CrQe1IOfg/rt/KBOf3KUKLlKpPnNBMD57b6MN8rLgdKWGjP9gaE48G7TO1eMlJnTKdx9rs7mLaZ14cZLqXWxsWAdR2C+Ij3hGp bot@bitcaliber.com'

    def setup_repo(self, owner, name):
        # TODO don't use the fucking default key
        key = self.KEY
        repository = self.gh_session.repository(owner, name)
        repository.create_key('Bit Caliber', key)
        repository.create_hook(name="web",
                               config={ "url": "http://api.bitcaliber.com/hook", "content_type": "json" }, 
                               events=['push', 'pull_request'])

# Organization

class Organization(models.Model):

    name = models.CharField(max_length=40, unique=True)
    users = models.ManyToManyField('GithubUser', related_name='organizations')
    rotation = JSONField()
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.name

# Analysis

class Repository(models.Model):

    url = models.CharField(max_length=400)
    description = models.CharField(max_length=400)
    organization = models.ForeignKey('Organization')
    last_analyzed = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def analyze(self):
        analyzer = Analyzer(self)
        analyzer.run()
        self.last_analyzed = datetime.datetime.now()
        self.save()
        return analyzer.run()

    def latest_commit(self, branch='master'):
        branch = Branch.objects.get(repository=self, name=branch)
        return branch.latest_commit()

    def __str__(self):
        return self.url

    def dict(self):
      return {
        "url": self.url,
        "organization": self.organization.name,
        "description": self.description,
        #"last_analyzed": last_analyzed
      }

# Task

class Task(models.Model):

    repository = models.ForeignKey('Repository')
    commit = models.ForeignKey('Commit')
    creator = models.ForeignKey('GithubUser', related_name='created_tasks')
    assigned_to = models.ForeignKey('GithubUser', related_name='assigned_tasks')
    text = models.CharField(max_length=400)
    line_number = models.IntegerField()
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)

class Branch(models.Model):
    
    repository = models.ForeignKey('Repository')
    name = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def latest_commit(self):
        commit = commit.objects.filter(branch=self).order_by('-authored_at')[0]

class Author(models.Model):
  
    user = models.ForeignKey("GithubUser", null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

class Commit(models.Model):

    parent = models.ForeignKey("self", null=True)
    branch = models.ForeignKey('Branch')
    commit_hash = models.CharField(max_length=40)
    commit_hash_short = models.CharField(max_length=7)
    authored_date = models.BigIntegerField()    
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)
    files = models.ManyToManyField('FileAnalysis', related_name='commits')
    author = models.ForeignKey('Author')

    def add_new_file_analysis(self, file_analysis):
        existing_file = self.files.filter(filename=file_analysis.filename)[:1]
        if existing_file:
            self.files.remove(existing_file[0])
        self.files.add(file_analysis) 

    def __str__(self):
        return "%s[%s]: %s" % (
            self.branch.repository.url, 
            self.branch.name,
            self.commit_hash
        )

class FileAnalysis(models.Model):

    class Meta:
        index_together = [
            ['filename', 'commit']
        ]

    filename = models.CharField(max_length=200)
    commit = models.ForeignKey('Commit')
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)
    
    def __str__(self):
        return "%s[%s][%s]: %s" % (
            self.commit.branch.repository.url, 
            self.commit.branch.name,
            self.commit.commit_hash,
            self.filename
        )

    def _get_key(self):
        s3Conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3Conn.get_bucket(settings.S3_BUCKET, validate=False)
        return bucket.get_key("%s/%s/%s/%s" % (self.commit.branch.repository.id, self.commit.branch.name, self.commit.commit_hash, self.filename), validate=False)

    def set_file_contents(self, contents, async=True):

        def _set_contents():
          self._get_key().set_contents_from_string(contents)

        if async:
            t = Thread(target=_set_contents)
            t.start()
        else:
            _set_contents()

    def get_file_contents(self):
        return self._get_key().get_contents_as_string()

    def delete(self):
        self._get_key().delete()

    def dict(self, stats=None):

        if not stats:
            stats = set()

        file_dict = {
            'filename': self.filename,
        }

        if 'pylint' in stats:
            file_dict['pylint'] = self.pylint_analysis.count()

        if 'pycomplexity' in stats:
            file_dict['complexity'] = self.pyfunction_complexity.aggregate(Sum('complexity'))['complexity__sum'] or 0

        return file_dict

class PyLintAnalysis(models.Model):

    message = models.CharField(max_length=200) 
    msg_id = models.CharField(max_length=8)
    file_analysis = models.ForeignKey('FileAnalysis', related_name='pylint_analysis')
    module = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    line = models.IntegerField()
    column = models.IntegerField()

    def __str__(self):
        return "[%s:%s:%s][%s:%s]: %s (%s)" % (
            self.file_analysis.filename,
            self.line,
            self.column,
            self.module,
            self.method,
            self.message,
            self.msg_id
        )

    def dict(self):
        return {
            "message": self.message,
            "msg_id": self.msg_id,
            "module": self.module,
            "method": self.method,
            "line": self.line,
            "column": self.column
        }

class PyFlakesAnalysis(models.Model):
    pass

class Pep8Analysis(models.Model):
    pass

class PyClassComplexityAnalysis(models.Model):

    file_analysis = models.ForeignKey('FileAnalysis', related_name='pyclass_complexity')
    name = models.CharField(max_length=100)
    line_start = models.IntegerField()
    line_end = models.IntegerField()
    column = models.IntegerField()
    real_complexity = models.IntegerField()

class PyFunctionComplexityAnalysis(models.Model):

    pyclass = models.ForeignKey('PyClassComplexityAnalysis', related_name='methods', null=True)
    file_analysis = models.ForeignKey('FileAnalysis', related_name='pyfunction_complexity')
    name = models.CharField(max_length=100)
    line_start = models.IntegerField()
    line_end = models.IntegerField()
    column = models.IntegerField()
    complexity = models.IntegerField()
