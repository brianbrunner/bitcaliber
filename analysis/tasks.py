from __future__ import absolute_import

from celery import shared_task

@shared_task
def analyze_repo(repo):
    repo.analyze()
