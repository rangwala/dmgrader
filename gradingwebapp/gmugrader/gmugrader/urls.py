"""gmugrader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from fileuploader import views as fileuploader_views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^users$', fileuploader_views.indexUser, name ='users'),
    url(r'^users.html$', fileuploader_views.indexUser, name ='users'),
    url(r'^users\/(?P<user_id>.*)\/?$', fileuploader_views.editUser, name='editUser'),
    url(r'^user\/(?P<user_id>.*)\/?$', fileuploader_views.updateUser, name='updateUser'),

    url(r'^polls/', include('polls.urls')),
    url(r'^fileuploader/', include('fileuploader.urls', namespace='fileuploader')),
    url(r'^$', fileuploader_views.login, name="login"),
    url(r'^tinymce/', include('tinymce.urls')),
    # ************************************ #
    # here's to updating some passwords... #
    # ************************************ #
    url(r'^password_reset/$', auth_views.PasswordResetView, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

