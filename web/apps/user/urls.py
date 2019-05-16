# _*_coding:utf-8_*_

from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from apps.user import views

urlpatterns = [
    url(r'^$', views.info, name='user_index'),

    url(r'^register/?$', views.register, name='user_register'),
    # url(r'^register/invate_code/(.+)$',views.register',name='invate_code'),
    url(r'^register/success/?$', TemplateView.as_view(template_name="user/register_success.html"), name='user_success'),
    url(r'^email_auth/?$', views.email_auth, name='user_email_auth'),
    url(r'^activate/auth/(.+)$', views.activate, name='user_activate'),

    url(r'^find_pwd/?$', views.find_pwd, name='user_find_pwd'),
    url(r'^reset_pwd/verify/(.+)$', views.reset_pwd, name='user_reset_pwd'),
    url(r'^re_pwd/?$', views.re_pwd, name='user_re_pwd'),
    url(r'^change_pwd/?$', views.chpasswd, name='user_change_pwd'),

    url(r'^info/?$', views.info, name='user_info'),
    url(r'^online/?$', views.online_users, name='user_online'),

    # url(r'^go_designer/?$',views.go_designer',name='user_go_designer'),

]
