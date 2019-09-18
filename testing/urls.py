from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from testing import views


app_name = 'testing'

urlpatterns = [
    url(r'^$', views.DepartamentListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.TestNameView.as_view(), name='test_list'),
    url(r'^test/(?P<pk>\d+)/', views.TestBaseView.as_view(), name='test_base'),

    url(r'^login/(?P<pk>\d+)/', views.Login.as_view(), name='login'),
    url(r'^auth/(?P<pk>\d+)/$', views.AuthTestListView.as_view(), name='auth_test_list'),
    url(r'^auth/test/(?P<pk>\d+)/', views.TestBaseView.as_view(), name='logged_test_base'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
