"""ureed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
# from django.contrib.staticfiles.urls import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

# from Ureedtranslate.views import  Index ,  Ureed

from translation.views import Index, mt_translation_view, create_new_user, \
    TranslationDetailView, translation_star_toggle  # , Login
from django.contrib.auth import views as auth_views

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    url(r'^manage/', include('translation.urls')),
    url(r'^mt/', include('translation.urls')),
    path('admin/', admin.site.urls, name='admin'),
    # url(r'^index/$', Index, name='index'),
    url(r'^translate/(?P<slug>[\w-]+)/$', mt_translation_view, name='translate'),
    url(r'^translate/(?P<pk>\d+)/$', TranslationDetailView.as_view(), name='translation_detail'),
    url(r'^translation-history/(?P<pk>\d+)/toggle-star/$', translation_star_toggle, name='translation_star_toggle'),
    # url(r'^translate/$', Ureed1, name='ureed'),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^$', Index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', create_new_user, name='signup'),
    # url(r'^select2/', include('django_select2.urls')),
    # url(r'^technical-support/send-email$', technical_support_send_email_view, name='technical_support'),
    # url(r'^admin/$', include(('translation.urls', 'customers'), namespace='customers')),
    # url(r'^reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
]
if settings.DEBUG:
    urlpatterns += static(settings.CUSTOM_STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.CUSTOM_MEDIA_URL, document_root=settings.MEDIA_ROOT)