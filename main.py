
from app import create_app
import os

app = create_app()

print(os.environ)
print(app.config.get('UPLOAD_FOLDER'))