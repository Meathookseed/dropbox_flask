from celery import Celery


worker = Celery('app',
                 backend='redis://localhost',
                 broker='redis://localhost:6379',
                 include=['app.api.service.email.email'])

worker.conf.update(result_expires=3600,)

if __name__ == '__main__':
    worker.start()
