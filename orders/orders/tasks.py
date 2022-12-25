from os import environ
from .celery import app
from .signals import new_user_registered_signal, new_order_signal, password_reset_token_created


@app.task
def new_user_email(user_id):
    new_user_registered_signal(user_id)


@app.task
def new_order(user_id):
    new_order_signal(user_id)


@app.task
def password_reset_token_created():
    sender = environ.get('DEFAULT_FROM_EMAIL', 'matolpydev@gmail.com')
    password_reset_token_created(sender=sender)
