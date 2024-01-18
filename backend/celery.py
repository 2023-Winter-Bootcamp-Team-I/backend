# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# 기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'printTime': { # 스케줄링 이름
        'task': 'book.tasks.printTime',
        'schedule': crontab(), # 인자 없으면 매 분마다 실행
    }
}
#등록된 장고 앱 설정에서 task 불러오기
app.autodiscover_tasks()