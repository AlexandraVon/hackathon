from tastypie.resources import ModelResource
from cards.models import User
from tastypie.authorization import DjangoAuthorization
class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		allowed_method = ['get']
		authorization = DjangoAuthorization()
		pass
