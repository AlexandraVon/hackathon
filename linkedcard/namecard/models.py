from django.db import models

# Create your models here.

class User(models.Model):
	user_id = models.CharField(max_length=50, primary_key=True)
	temp_id = models.ForeignKey(Template)
	qr_code_url = models.CharField(max_length=300)

class Relation(models.Model):
	user_id = models.ForeignKey(User)

class Template
	template_id = models.CharField(max_length=50, primary_key=True)
	location = models.CharField(max_length=500)
	name = models.CharField(max_length=10, null=False)
	email = models.CharField(max_length=10)
	headline = models.CharField(max_length=10)
	photo_url = models.CharField(max_length=10)
	linkedin_address = models.CharField(max_length=10)
	company = models.CharField(max_length=10)
