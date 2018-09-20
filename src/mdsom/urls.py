from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
import ajax_select.urls
import profiles.urls
import accounts.urls
from . import views
from inmediag.myadmin import admin_site
# Personalized admin site settings like title and header
admin_site.site_title = 'Mdsom Site Admin'
admin_site.site_header = 'Mdsom Administration'

urlpatterns = [
    path('', include(accounts.urls)),
    path('home/', views.HomePage.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('users/', include(profiles.urls)),


    path('chaining/', include('smart_selects.urls')),
    path('adminactions/', include('adminactions.urls')),
    #url(r'^ajax-upload/', include('ajax_upload.urls')),
    # place it at whatever base url you like
    path('ajax_select/', include(ajax_select.urls)),
    path('tinymce/', include('tinymce.urls')),
    path('inmediag/', include('inmediag.urls')),
    path('admin/', admin_site.urls),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
