from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth.views import login,logout
from django.conf.urls.static import static
import WebSite.settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': WebSite.settings.STATIC_DIR}),
    (r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': WebSite.settings.MEDIA_ROOT}),
    (r'^jbrowse/(?P<path>.*)', 'django.views.static.serve', {'document_root': WebSite.settings.JBROWSE_DIR}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^database/', include('Database.urls')),
    url(r'^blast/', include('Blast.urls')),
)

