from django.conf.urls import patterns, url
from users import views
from rest_framework.urlpatterns import format_suffix_patterns




urlpatterns = patterns(
    'users.views',
    url(r'^$', 'usertable_collection'),
    url(r'^(?P<pk>[0-9]+)$', views.usertable_detail),
    url(r'^', views.TestView.as_view(), name='test-view'),
    url(r'^auth/', views.AuthView.as_view(), name='auth-view'),
    # api
    #url(r'^api/v1/usertables/$', 'usertable_collection'),
)

#urlpatterns = format_suffix_patterns(urlpatterns)
