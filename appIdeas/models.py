from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from projectIdeas.settings import MEDIA_ROOT
from datetime import date, time


TYPE_VOTE = (
	('positive', 'positive'),
	('negative', 'negative'),
)


class Categorie(models.Model):
	unique_name = models.CharField(
		max_length=20, blank=False, null=False, unique=True, primary_key=True)
	name = models.CharField(max_length=20, blank=False, null=False)

	def __str__(self):
		return self.name

	def natural_key(self):
		return self.name


class Idea(models.Model):
	author = models.ForeignKey(
		User, on_delete=models.SET_NULL, blank=True, null=True)
	description = models.TextField(max_length=200, blank=False, null=False)
	category = models.ForeignKey(
		Categorie, on_delete=models.SET_NULL, blank=True, null=True)
	publication_date = models.DateTimeField(
		editable=True, blank=False, null=False)
	anonimus = models.BooleanField(default=False)
	approved = models.BooleanField(default=False)
	discarded = models.BooleanField(default=False)
	quantity_positive_votes = models.IntegerField(blank=True, null=True)
	quantity_negative_votes = models.IntegerField(blank=True, null=True)
	photo = models.ImageField(upload_to='media/photo/',
		default='media/photo/user.png', blank=True, null=True)

	def __str__(self):
		return str(self.description)


class Votes_Realized(models.Model):
	id_user = models.ForeignKey(
		User, on_delete=models.SET_NULL, blank=True, null=True)
	id_idea = models.ForeignKey(
		Idea, on_delete=models.SET_NULL, blank=True, null=True)
	type = models.CharField(
		max_length=10, blank=False, null=False, choices=TYPE_VOTE)

	def __str__(self):
		return str(self.id_user)


class Permission(models.Model):
	class Meta:
		permissions = (
			("can_validate_idea", "Puede Validar Ideas"),
		)
