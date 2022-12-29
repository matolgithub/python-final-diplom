from django.http import JsonResponse
from django.core.mail.message import EmailMultiAlternatives
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .celery_conf import app
from requests import get
from yaml import load as load_yaml, Loader
from web_service.models import Shop, Category, Product, Parameter, ProductParameter, ProductInfo
from orders.settings import DEFAULT_EMAIL_ADMIN, EMAIL_HOST_USER

from celery.utils.log import get_task_logger

from django.db import connection
import celery

logger = get_task_logger(__name__)


class FaultTolerantTask(celery.Task):
    """ Implements after return hook to close the invalid connection.
    This way, django is forced to serve a new connection for the next
    task.
    """
    abstract = True

    def after_return(self, *args, **kwargs):
        connection.close()


@app.task(base=FaultTolerantTask, name='send_email_task')
def send_emails(title, message, email, *args, **kwargs):
    emails = [DEFAULT_EMAIL_ADMIN]
    emails.append(email)
    try:
        msg = EmailMultiAlternatives(subject=title, body=message, from_email=EMAIL_HOST_USER, to=emails)
        msg.send()
        return f'Title: {msg.subject}, Message:{msg.body}'
    except Exception as ex:
        raise ex


@app.task(base=FaultTolerantTask, name='import_shop_task')
def import_shop_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

    if request.user.type != 'shop':
        return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

    url = request.data.get('url')
    if url:
        validate_url = URLValidator()
        try:
            validate_url(url)
        except ValidationError as ex:
            return JsonResponse({'Status': False, 'Error': str(ex)})
        else:
            stream = get(url).content

            data = load_yaml(stream, Loader=Loader)

            shop, _ = Shop.objects.get_or_create(
                name=data['shop'], user_id=request.user.id)
            for category in data['categories']:
                category_object, _ = Category.objects.get_or_create(
                    id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()
            ProductInfo.objects.filter(shop_id=shop.id).delete()
            for item in data['goods']:
                product, _ = Product.objects.get_or_create(
                    name=item['name'], category_id=item['category'])

                product_info = ProductInfo.objects.create(product_id=product.id,
                                                          external_id=item['id'],
                                                          model=item['model'],
                                                          price=item['price'],
                                                          price_rrc=item['price_rrc'],
                                                          quantity=item['quantity'],
                                                          shop_id=shop.id)
                for name, value in item['parameters'].items():
                    parameter_object, _ = Parameter.objects.get_or_create(
                        name=name)
                    ProductParameter.objects.create(product_info_id=product_info.id,
                                                    parameter_id=parameter_object.id,
                                                    value=value)

            return JsonResponse({'Status': True})

    return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
