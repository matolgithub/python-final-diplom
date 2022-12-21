from django.urls import path
from rest_framework.routers import DefaultRouter
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from .views import RegisterAccount, ConfirmAccount, AccountDetails, ContactView, LoginAccount, \
    ShopViewSet, PartnerUpdateView, PartnerStateViewSet, PartnerOrdersView, ProductInfoView, CategoryView, BasketView, \
    OrderView

app_name = 'web_service'

router = DefaultRouter()

router.register('shops', ShopViewSet, basename='shops')
router.register('partner/state', PartnerStateViewSet, basename='partner-state')

urlpatterns = [
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(),
         name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm,
         name='password-reset-confirm'),

    path('products', ProductInfoView.as_view(), name='products'),
    path('categories', CategoryView.as_view(), name='categories'),

    path('partner/update', PartnerUpdateView.as_view(), name='partner-update'),
    path('partner/orders', PartnerOrdersView.as_view(), name='partner-orders'),

    path('basket', BasketView.as_view(), name='basket'),
    path('order', OrderView.as_view(), name='order'),

]
