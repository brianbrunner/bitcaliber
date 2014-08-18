import os
import time
from cStringIO import StringIO
from urllib import quote

import pylint.lint
import radon.complexity
from pygit2 import Repository as Repo, GitError

from dictreporter import DictReporter

class Analyzer(object):

    def __init__(self, repo_obj, cache='/tmp', languages=None, branch='master'):

        # local import to avoid a circular import
        from analysis.models import Branch

        self.repo_obj = repo_obj

        if languages is None:
            languages = ["python"]

        self.languages = languages
        self.branch = branch

        repo_url = self.repo_obj.url

        repo_dir = os.path.join(cache, quote(repo_url))
        try:
            self.repo = Repo(repo_dir)
            origin = self.repo.remotes.origin

            try:
                origin.fetch('all')
                origin.pull(self.branch)
            except AssertionError as e:
                # triggers when trying to pull on a repo that is up to date already
                print e
                print "FAILED TO PULL"
                pass

        except GitError:
            self.repo = Repo.clone_from(repo_url, repo_dir)

        branch_obj = Branch.objects.filter(repository=repo_obj, name=self.branch)[:1]
        if not branch_obj:
            branch_obj = Branch(repository=repo_obj, name=self.branch)
            # TODO branch last analyzed
            branch_obj.save()
        else:
            branch_obj = branch_obj[0]

        self.branch_obj = branch_obj


    def run(self, period=60*60*24*30):
        self.do_time_scan(period)

    def do_time_scan(self, period=60*60*24*30):

        # local import to avoid a circular import
        from analysis.models import Author, Commit

        max_age = int(time.time()) - period

        commits_to_analyze = []
        for commit in self.repo.iter_commits('master'):
            if commit.authored_date > max_age:
                commits_to_analyze.insert(0, commit)
            else:
                break
       
        commits_seen = Commit.objects.filter(commit_hash__in=commits_to_analyze).only('commit_hash')

        commits_seen_set = set([commit.commit_hash for commit in commits_seen])

        full = True
        parent = None
        for commit in commits_to_analyze:
            if commit.hexsha not in commits_seen_set:
                author = commit.author
                author_email = author.email
                author_obj = Author.objects.filter(email=author_email)[:1]
                if author_obj:
                  author_obj = author_obj[0]
                else:
                  # TODO Tie author to user
                  author_obj = Author(email=author_email, name=author.name)
                  author_obj.save()
                commit_obj = Commit(commit_hash=commit.hexsha, commit_hash_short=commit.hexsha[:7],
                                    branch=self.branch_obj, authored_date=commit.authored_date, author=author_obj)
                commit_obj.save()
                if parent:
                    commit_obj.files.add(*[file for file in parent.files.all()])
                self.analyze_commit(commit, commit_obj, full)
                commit_obj.save()
                parent = commit_obj
            full = False 

    def analyze_commit(self, commit, commit_obj, full=False):

        from analysis.models import FileAnalysis, PyLintAnalysis, \
            PyClassComplexityAnalysis, PyFunctionComplexityAnalysis

        self.repo.git.checkout(commit.hexsha)
        
        file_analysis_entries = {}

        lint_paths = []

        if full:

            for root, dirs, files in os.walk(self.repo.workdir):
                for filename in files:
                    if filename[-3:] == ".py":

                        filepath = os.path.join(root, filename)
                        lint_paths.append(filepath)
                        file_obj = open(filepath)
                        file_data = file_obj.read()
                        analysis_results = radon.complexity.cc_visit(file_data, no_assert=True)

                        relative_filepath = filepath[len(self.repo.workdir)+1:]

                        file_analysis = FileAnalysis(commit=commit_obj, filename=relative_filepath)
                        file_analysis.save()
                        commit_obj.add_new_file_analysis(file_analysis)
                        file_analysis.set_file_contents(file_data)
                        file_analysis_entries[relative_filepath] = file_analysis

                        classes = [c for c in analysis_results if not hasattr(c, 'classname')]
                        for c in classes:
                            class_complexity = PyClassComplexityAnalysis(
                                file_analysis = file_analysis,
                                name = c.name,
                                line_start = c.lineno,
                                line_end = c.endline,
                                column = c.col_offset,
                                real_complexity = c.real_complexity
                            )
                            class_complexity.save()
                            
                            for func in c.methods:
                                func_complexity = PyFunctionComplexityAnalysis(
                                    pyclass = class_complexity,
                                    file_analysis = file_analysis,
                                    name = func.name,
                                    line_start = func.lineno,
                                    line_end = func.endline,
                                    column = func.col_offset,
                                    complexity = func.complexity
                                )
                                func_complexity.save()

                        functions = [f for f in analysis_results if hasattr(f, 'classname') and f.classname is None]
                        for func in functions:
                            func_complexity = PyFunctionComplexityAnalysis(
                                file_analysis = file_analysis,
                                name = func.name,
                                line_start = func.lineno,
                                line_end = func.endline,
                                column = func.col_offset,
                                complexity = func.complexity
                            )
                            func_complexity.save()

        else:

           # TODO handle deleted files, renamed files etc.

           for filename in commit.stats.files.keys():

                if filename[-3:] == '.py':
                    filepath = os.path.join(self.repo.workdir, filename)

                    try:

                        file_obj = open(filepath)
                        file_data = file_obj.read()
                        analysis_results = radon.complexity.cc_visit(file_data, no_assert=True)
                        relative_filepath = filepath[len(self.repo.workdir)+1:]

                        file_analysis = FileAnalysis(commit=commit_obj, filename=relative_filepath)
                        file_analysis.save()
                        commit_obj.add_new_file_analysis(file_analysis)
                        file_analysis.set_file_contents(file_data)
                        file_analysis_entries[relative_filepath] = file_analysis

                        classes = [c for c in analysis_results if not hasattr(c, 'classname')]
                        for c in classes:
                            class_complexity = PyClassComplexityAnalysis(
                                file_analysis = file_analysis,
                                name = c.name,
                                line_start = c.lineno,
                                line_end = c.endline,
                                column = c.col_offset,
                                real_complexity = c.real_complexity
                            )
                            class_complexity.save()
                            
                            for func in c.methods:
                                func_complexity = PyFunctionComplexityAnalysis(
                                    pyclass = class_complexity,
                                    file_analysis = file_analysis,
                                    name = func.name,
                                    line_start = func.lineno,
                                    line_end = func.endline,
                                    column = func.col_offset,
                                    complexity = func.complexity
                                )
                                func_complexity.save()

                        functions = [f for f in analysis_results if hasattr(f, 'classname') and f.classname is None]
                        for func in functions:
                            func_complexity = PyFunctionComplexityAnalysis(
                                file_analysis = file_analysis,
                                name = func.name,
                                line_start = func.lineno,
                                line_end = func.endline,
                                column = func.col_offset,
                                complexity = func.complexity
                            )
                            func_complexity.save()


                        lint_paths.append(filepath)

                    except IOError as e:
                        analysis_results = "File was deleted or renamed"
                    except SyntaxError as e:
                        analysis_results = "Could not compile. Syntax Error."


        if len(lint_paths):

            dict_reporter = DictReporter()
            dict_reporter.msgs = []
            pylint.lint.Run(lint_paths, reporter=dict_reporter, exit=False)

            for msg in dict_reporter.msgs:
              filename = msg['location']['filepath'][len(self.repo.workdir)+1:]
              analysis = PyLintAnalysis(
                file_analysis = file_analysis_entries[filename],
                message = msg['msg'],
                msg_id = msg['msg_id'],
                module = msg['location']['module'],
                method = msg['location']['method'],
                line = msg['location']['line'],
                column = msg['location']['column']
              )
              analysis.save()
