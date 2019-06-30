from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    re_path(r"login/$", auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    re_path(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    re_path(r"register/$", views.Register.as_view(), name="register"),
    re_path(r"activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.activate, name='activate'),
    re_path(r"search/", views.SearchListView.as_view(), name="search"),
    re_path(r"yourplace/(?P<username>[-\w]+)/$", views.YourPlaceView.as_view(), name="yourplace"),
    re_path(r'add_to_cart/$',views.add_to_cart_view,name="add_to_cart"),
    re_path(r'remove_from_cart/$', views.remove_from_cart_view,name="remove_from_cart"),
    re_path(r'change_item_quantity/$',views.change_item_quantity,name="change_item_quantity"),
    re_path(r'cart/$',views.CartView.as_view(),name="cart"),
    re_path(r'checkout/(?P<id>[-\w]+)/$',views.CheckOutView.as_view(),name="checkout"),
    re_path(r'thankyou/(?P<id>[-\w]+)/$',views.ThankYouView.as_view(),name='thankyou'),
    re_path(r"(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$",views.ProductDetailView.as_view(),name="product"),
    re_path(r"(?P<slug>[-\w]+)/$",views.CategoryDetailView.as_view(),name="category"),
    re_path(r'^$',views.HomePageView.as_view(),name='home'),
]


# re_path(r'add_to_cart/(?P<slug>[-\w]+)/$',views.add_to_cart_view,name="add_to_cart")
# re_path(r'remove_from_cart/(?P<slug>[-\w]+)/$', views.remove_from_cart_view,name="remove_from_cart"),
