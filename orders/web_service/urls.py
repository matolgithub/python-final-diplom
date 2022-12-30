from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from .views import RegisterAccount, ConfirmAccount, AccountDetails, ContactView, LoginAccount, \
    ShopView, PartnerUpdate, PartnerUpdateCelery, PartnerState, PartnerOrders, ProductInfoView, CategoryView, \
    BasketView, OrderView

app_name = 'web_service'

router = DefaultRouter()

router.register('products', ProductInfoView, basename='products')
router.register('categories', CategoryView, basename='categories')
router.register('shops', ShopView, basename='shops')

urlpatterns = [
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    path('basket', BasketView.as_view(), name='basket'),
    path('order', OrderView.as_view(), name='order'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/update_celery', PartnerUpdateCelery.as_view(), name='partner-update-celery'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('', include(router.urls)),
]

urlpatterns += router.urls
