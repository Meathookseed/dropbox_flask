from celery import Celery
from app import create_app

def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery('app',
                    backend='redis://localhost',
                    broker='redis://localhost:6379',
                    include=['app.api.service.auth.__init__'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery