from orders.wsgi import *
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created
from web_service.models import User, ConfirmEmailToken
from orders.tasks import send_emails

# new_user_registered = Signal(providing_args=['user_id'])
# new_order = Signal(providing_args=['user_id'])

new_user_registered = Signal('user_id')
new_order = Signal('user_id')


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    """
    # send an e-mail to the user
    title = f'Сброс пароля для {reset_password_token.user}'
    message = f'Токен для сброса пароля {reset_password_token.key}'
    email = reset_password_token.user
    send_emails(title, message, email)


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
    send_emails(title, message, email)


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    Отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    title = 'Обновление статуса заказа'
    message = 'Заказ сформирован'
    email = user.email
    send_emails.apply_async((title, message, email), countdown=5 * 60)
