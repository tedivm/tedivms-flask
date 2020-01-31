from app import celery, create_app

# Make sure to import your celery tasks here!
# Otherwise the worker will not pick them up.


app = create_app()

with app.app_context():
    celery.start()
