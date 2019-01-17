from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserAuthenticationForm

urlpatterns = [
    re_path(r"^sign-up/$", views.SignUp.as_view(), name="sign_up"),

    re_path(r"^login/$", auth_views.LoginView.as_view(
        authentication_form=UserAuthenticationForm), name="login"),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),

    re_path(r"^logout/$", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    re_path(r"^password-change/$", auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change_form.html"), name='password_change'),

    re_path(r"^password-change/done/$", auth_views.PasswordChangeDoneView.as_view(
        template_name="registration/password_change_done.html"), name='password_change_done'),

    re_path(r"^password-reset/$", auth_views.PasswordResetView.as_view(
        template_name="password_reset/password_reset_form.html"), name="password_reset"),

    re_path(r"^password-reset/done/$", auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset/password_reset_done.html"), name="password_reset_done"),

    re_path(r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="password_reset/password_reset_confirm.html"),
            name="password_reset_confirm"),

    re_path(r"^reset/done/$", auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset/password_reset_complete.html"), name="password_reset_complete"),

]
