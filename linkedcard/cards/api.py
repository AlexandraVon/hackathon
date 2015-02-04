from tastypie.resources import ModelResource
from cards.models import User

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		allowed_method = ['get']
		pass
