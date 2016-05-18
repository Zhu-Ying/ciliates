from django.conf.urls import include, url, patterns
from .views import *
from django.contrib.auth import views as userViews

urlpatterns = patterns('',
    url(r'^create$', CreateView),
    url(r'^reset$', ResetView),
    url(r'^login$', userViews.login,{'template_name': 'User/login.html'}), 
    url(r'^logout$', userViews.logout), 
    url(r'^password/change$', userViews.password_change, {'template_name': 'User/password_change_form.html'}),
    url(r'^password/change/done$', userViews.password_change_done, {'template_name': 'User/password_change_done.html'}, name='password_change_done'),
    #url(r'^password/reset$', userViews.password_reset, {'template_name': 'User/password_reset_form.html'}),
    #url(r'^password/reset/done$', userViews.password_reset_done, name='password_reset_done'),
    #url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', userViews.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^password/reset/complete$', userViews.password_reset_complete, name='password_reset_complete'),
    url(r'^user$', UserView),
    url(r'^manage$', ManageView),
    url(r'^delete$', Delete),
)