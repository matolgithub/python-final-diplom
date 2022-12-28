import yaml
from orders.settings import EMAIL_HOST_USER
from django.core.mail.message import EmailMultiAlternatives
from .celery_conf import app
from web_service.models import Shop, Category, Product, Parameter, ProductParameter, ProductInfo

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
    emails = []
    emails.append(email)
    try:
        msg = EmailMultiAlternatives(subject=title, body=message, from_email=EMAIL_HOST_USER, to=emails)
        msg.send()
        return f'Title: {msg.subject}, Message:{msg.body}'
    except Exception as ex:
        raise ex


def open_file(shop):
    with open(shop.get_file(), 'r') as file:
        data = yaml.safe_load(file)
    return data


@app.task(base=FaultTolerantTask, name='import_shop_task')
def import_shop_data(data, user_id):
    file = open_file(data)

    shop, _ = Shop.objects.get_or_create(user_id=user_id,
                                         defaults={'name': file['shop']})

    for category in file['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()

    ProductInfo.objects.filter(shop_id=shop.id).delete()

    for item in file['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)
