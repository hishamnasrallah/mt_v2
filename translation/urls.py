
# from django.contrib import admin
# from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from translation.views import CustomerInfoListView, CustomerInfoCreateView, CustomerDetailView, CustomerUpdateView, \
    StaffHome, ManageFeatureCreateView, ManageFeaturesDetailView, ManageFeaturesUpdateView, CustomerActivateView, \
    ClientInfoDelete, TranslationsListView, export_translation_data, CustomerSubscriptionCreateView, \
    CustomerSubscriptionsListView, translation_star_toggle, MTTranslateAPIView, LexicalTranslationAPIView, \
    MTTranslateFileAPIView, MTTranslationFileListAPIView, MTTranslationFileCreateAPIView, \
    MTTokenRefreshView, MTTokenObtainPairView, CreateClientAPIView, MTTranslateAPIViewTMSlUse

urlpatterns = [

    # path('system/admin/', admin.site.urls),
    # url(r'^index/$', Index, name='index'),
    # url(r'^translate/$', Ureed, name='ureed'),
    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', Login, name='login'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('admin/', include('ureed_translate.urls')),

    url(r'^customers/$', CustomerInfoListView.as_view(), name='main_view'),
    url(r'^customers/create/$', CustomerInfoCreateView.as_view(), name='create_customer'),
    url(r'^customers/(?P<pk>\d+)/$', CustomerDetailView.as_view(), name='detail_customer'),
    url(r'^customers/(?P<pk>\d+)/edit/$', CustomerUpdateView.as_view(), name='edit_customer'),
    url(r'^customers/(?P<pk>\d+)/delete/$', ClientInfoDelete.as_view(), name='delete-customer'),
    # url(r'^translation-history/(?P<pk>\d+)/toggle-star/$', TranslationStarToggle.as_view(), name='translation_star_toggle'),
    # url(r'^customers/(?P<pk>\d+)/active/$', CustomerActivateView.as_view(), name='active_customer'),
    # url(r'^customers/(?P<pk>\d+)/inactive/$', CustomerUpdateView.as_view(), name='inactive_customer'),


    url(r'^customers/features/(?P<customer>\d+)/create/$', ManageFeatureCreateView.as_view(), name='features_create'),
    url(r'^customers/features/(?P<customer>\d+)/$', ManageFeaturesDetailView.as_view(), name='features_detail'),
    url(r'^customers/features/(?P<pk>\d+)/edit/$', ManageFeaturesUpdateView.as_view(), name='features_edit'),
    url(r'^translations/$', TranslationsListView.as_view(), name='translation_list'),
    url(r'^translations/export/$', export_translation_data, name='translation_export'),
    url(r'^customers/subscription/add/$', CustomerSubscriptionCreateView.as_view(), name='add_subscription'),

    url(r'^customers/subscription/list/$', CustomerSubscriptionsListView.as_view(), name='list_subscription'),
    url(r'^mt/translate/sentence/$', MTTranslateAPIView.as_view(), name='mt-sentence'),
    url(r'^translate/words/$', LexicalTranslationAPIView.as_view(), name='words-translation'),
    url(r'^translate/file/(?P<slug>[\w-]+)/$', MTTranslateFileAPIView.as_view(), name='file-translation'),
    url(r'^translate/file/(?P<slug>[\w-]+)/list/$', MTTranslationFileListAPIView.as_view(), name='list-file-translation'),
    url(r'^translate/file/(?P<slug>[\w-]+)/create/$', MTTranslationFileCreateAPIView.as_view(), name='create-file-translation'),

    # url(r'^translate/sentence/$', MTTranslateAPIViewExternalUse.as_view(), name='mt-translation'),
    url(r'^tms/translate/sentence/$', MTTranslateAPIViewTMSlUse.as_view(), name='tms-mt-translation'),

    url(r'^client/create/$', CreateClientAPIView.as_view(), name='create-client'),

    # url(r'^customers/features/(?P<pk>\d+)/$', CustomerInfoListView.as_view(), name='features_create'),

    url(r'^$', StaffHome.as_view(), name='home-staff'),

    path('refresh-token/', MTTokenRefreshView.as_view(), name='jwt_refresh'),
    path('login/', MTTokenObtainPairView.as_view(), name='jwt_login'),


]
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
#     urlpatterns += ('',
#             url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )