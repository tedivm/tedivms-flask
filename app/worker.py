from app import celery, create_app
import app.tasks.edits

app = create_app()

with app.app_context():
    celery.start()
