from django.conf.urls import include, url
from django.contrib import admin
from api.views import login
urlpatterns = [
    # Examples:
    # url(r'^$', 'psa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login, name='login'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
