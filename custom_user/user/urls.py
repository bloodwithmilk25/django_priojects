from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import views
from .forms import UserAuthenticationForm


urlpatterns = [
    re_path(r"^sign-up/$", views.SignUp.as_view(), name="sign_up"),

    re_path(r"^login/$", auth_views.LoginView.as_view(
        authentication_form=UserAuthenticationForm, template_name='user/registration/login.html'), name="login"),

    re_path(r"^update/$", views.update_user, name="update_user"),

    re_path('^$', TemplateView.as_view(template_name='user/profile.html'), name='profile'),

    re_path(r'^confirm/$', views.confirm, name='confirm'),

    re_path(r'^resent-email/$', views.resent_email, name='resent_email'),

    re_path(r'^verify/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.verify, name='verify'),

    re_path(r"^logout/$", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    re_path(r"^password-change/$", auth_views.PasswordChangeView.as_view(
        template_name="user/registration/password_change_form.html"), name='password_change'),

    re_path(r"^password-change/done/$", auth_views.PasswordChangeDoneView.as_view(
        template_name="user/registration/password_change_done.html"), name='password_change_done'),

    re_path(r"^password-reset/$", auth_views.PasswordResetView.as_view(
        template_name="user/registration/password_reset_form.html"), name="password_reset"),

    re_path(r"^password-reset/done/$", auth_views.PasswordResetDoneView.as_view(
        template_name="user/registration/password_reset_done.html"), name="password_reset_done"),

    re_path(r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="user/registration/password_reset_confirm.html"),
            name="password_reset_confirm"),

    re_path(r"^reset/done/$", auth_views.PasswordResetCompleteView.as_view(
        template_name="user/registration/password_reset_complete.html"), name="password_reset_complete"),

]
