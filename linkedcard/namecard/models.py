from django.db import models

# Create your models here.

class User(models.Model):
	user_id = models.CharField(max_length=50, primary_key=True)
	temp_id = models.CharField(max_length=50)
	qr_code_url = models.CharField(max_length=300)

class Relation(models.Model):
	user_id = models.ForeignKey(User)
	follow_id = models.ForeignKey(User)
