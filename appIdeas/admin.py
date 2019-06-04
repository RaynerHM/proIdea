from django.contrib import admin

# Register your models here.
from appIdeas.models import Idea, Categorie, Votes_Realized


class Admin_Idea(admin.ModelAdmin):
	list_display = [
		'id', 'author', 'description', 'category', 'quantity_positive_votes',
		'quantity_negative_votes', 'publication_date', 'approved',
		'discarded', 'anonimus', 'photo'
	]
	ordering = ['-id']

	class Meta:
		model = Idea

admin.site.register(Idea, Admin_Idea)


class Admin_Categorie(admin.ModelAdmin):
	list_display = ['unique_name', 'name']
	ordering = ['unique_name']

	class Meta:
		model = Categorie

admin.site.register(Categorie, Admin_Categorie)


class Admin_Votes_Realized(admin.ModelAdmin):
	list_display = ['id', 'id_idea', 'id_user', 'type']
	ordering = ['id']

	class Meta:
		model = Votes_Realized

admin.site.register(Votes_Realized, Admin_Votes_Realized)
