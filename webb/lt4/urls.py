"""lt4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    #path(r'', include('service.urls')),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('',include('IO.urls')),
    path('accounts/',include('accounts.urls')),
    path('history/',include('history.urls', namespace=' src')),
    path('chart/', include('chart.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    ## 테스트용 url
                
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

