#Apartado para poner a laburar a celery 
import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery = Celery('core')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

@celery.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 