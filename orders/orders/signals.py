from orders.wsgi import *
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created
from web_service.models import User, ConfirmEmailToken
from orders.tasks import send_emails
from datetime import datetime

new_user_registered = Signal('user_id')
new_order = Signal('user_id')
new_price = Signal('user_id')
new_price_celery = Signal('user_id')


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    Отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    title = f'Подтверждение регистрации для {token.user.email}'
    message = f'Токен для подтверждения регистрации {token.key}'
    email = token.user.email
    send_emails.delay(title, message, email)


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    Отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    user_email, user_fn, user_ln, user_company, user_position = user.email, user.first_name, user.last_name, user.company, user.position
    title = f'Информация для {user_company}, {user_email} об изменении статуса заказа.'
    message = f'Благодарим Вас: {user_position} {user_fn} {user_ln}! Статус Вашего заказа изменён!'
    email = user.email
    send_emails.delay(title, message, email)


@receiver(new_price)
def new_price_signal(user_id, **kwargs):
    """
    Отправяем письмо при обновлении прайса
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    user_email, user_fn, user_ln, user_company, user_position = user.email, user.first_name, user.last_name, \
        user.company, user.position
    title = f'Информация для {user_company}, {user_email} - прайс обновлён!'
    message = f'Данным письмом сообщаем Вам, уважаемый {user_position} {user_fn} {user_ln}, что прайс на товары ' \
              f'изменён. {datetime.now()}!'
    email = user.email
    send_emails.delay(title, message, email)


@receiver(new_price_celery)
def new_price_celery_signal(user_id, **kwargs):
    """
    Отправяем письмо при обновлении прайса
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    user_email, user_fn, user_ln, user_company, user_position = user.email, user.first_name, user.last_name, \
        user.company, user.position
    title = f'Информация для {user_company}, {user_email} - прайс обновлён!'
    message = f'Данным письмом сообщаем Вам, уважаемый {user_position} {user_fn} {user_ln}, что прайс на товары ' \
              f'изменён. {datetime.now()}****from_Celery****!'
    email = user.email
    send_emails.delay(title, message, email)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    """
    # send an e-mail to the user
    title = f'Сброс пароля для {reset_password_token.user}'
    message = f'Токен для сброса пароля {reset_password_token.key}'
    email = reset_password_token.user
    send_emails.delay(title, message, email)
