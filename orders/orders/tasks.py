import yaml
from orders.settings import EMAIL_HOST_USER
from django.core.mail.message import EmailMultiAlternatives
from .celery_conf import app
from web_service.models import Shop, Category, Product, Parameter, ProductParameter, ProductInfo


@app.task()
def send_email(title, message, email, *args, **kwargs):
    email_list = []
    email_list.append(email)
    try:
        msg = EmailMultiAlternatives(subject=title, body=message, from_email=EMAIL_HOST_USER, to=email_list)
        msg.send()
        return f'Title: {msg.subject}, Message:{msg.body}'
    except Exception as ex:
        raise ex


def open_file(shop):
    with open(shop.get_file(), 'r') as file:
        data = yaml.safe_load(file)
    return data


@app.task()
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
