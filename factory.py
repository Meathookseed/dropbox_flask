import os

from celery import Celery

from app import create_app


def create_celery_app(app=None):
    app, socket = app or create_app()

    if os.environ.get('FLASK_ENV') == 'docker':
        backend_uri = 'redis://redis'
        broker_uri = 'redis://redis:6379'

    else:
        backend_uri = 'redis://localhost'
        broker_uri = 'redis://localhost:6379'

    celery = Celery('app',
                    backend=f'{backend_uri}',
                    broker=f'{broker_uri}',
                    include=['app.api.service.auth.__init__'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
