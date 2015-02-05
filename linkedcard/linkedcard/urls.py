from django.conf.urls import patterns, include, url
from django.contrib import admin
from cards.views import MyView
from cards.api import UserResource,TemplateResource
from tastypie.api import Api

v1_api= Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(TemplateResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'linkedcard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^myview/',MyView.as_view()),	
#    url(r'^api/',include(UserResource().urls)),
#    url(r'^api/',include(TemplateResource().urls)),
    (r'^api/',include(v1_api.urls)),
	(r'^api-auth',include('rest_framework.urls', namespace='rest_framework')),
)
