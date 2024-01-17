
# tasks.py

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from celery import shared_task

from backend.celery import app


# test 용 함수
@shared_task
def printTime():
    print("Testtime: ", datetime.now())